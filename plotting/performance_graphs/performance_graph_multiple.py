import csv
import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def performance_graph_confidence_interval(rootdir, experiment, key, metric):
    """
    Makes a simple performance graph for a particular experiment with each individual run plotted.
    """
    test = []
    i = 1
    for f in glob.glob(f'{rootdir}\\{experiment}*'):
        with open(f'{f}\\Stats.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for g, row in enumerate(spamreader):
                test.append([f'run_{i}', int(g), float(row[metric]), key])
        i += 1

    data = pd.DataFrame(test, columns=['run', 'generation', 'mean_fitness', 'key'])

    return data


def simple_plot(frames, x_label, y_label, log_yaxis):

    result = pd.concat(frames, ignore_index=True)

    print(result)

    sns.set_theme()
    sns.set(font_scale=1.50)
    new = sns.lineplot(data=result, x=x_label, y=y_label, hue='key')
    if log_yaxis:
        plt.set(yscale='log')
        new.set_yscale("log")
    sns.set_style("ticks")
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.xticks(np.arange(0, 41, 4))
    # plt.ylim(0, 1)
    plt.xlim(0, 40)
    plt.show()
