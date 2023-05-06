import csv
import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def performance_graph(rootdir, experiment):
    """
    Create a performance graph for a single experiment where each individual run is plotted.

    Parameters
    ----------
    path : str
        Root filepath to the data
    experiment : str
        Unique experiment identified e.g "Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.EUC"

    Returns
    -------
    data : pd.DataFrame
        The run data as columns in a pandas dataframe.
    """
    experiment_data = {}

    for run_folder in glob.glob(f'{rootdir}\\{experiment}*'):
        run_index = run_folder.split('id')[1]
        time_series = []

        with open(f'{run_folder}\\Stats.csv', newline='') as run_csv_file:
            for row in csv.reader(run_csv_file, delimiter=' '):
                time_series.append(row[0])

        experiment_data[f'run_{run_index}'] = time_series

    data = pd.DataFrame(experiment_data, dtype=float)

    return data


def simple_plot(data, log_yaxis=False):
    """
    Should automatically set correct limits

    Parameters
    ----------
    data : pd.DataFrame
        Run time series data as columns within a pandas dataframe.

    """
    sns.set_theme()

    plot = sns.lineplot(data=data, legend=False)

    if log_yaxis:
        plot.set_yscale("log")

    plt.xticks(np.arange(0, 21, 2))
    plt.show()
