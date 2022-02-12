import csv
import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def performance_graph_confidence_interval(rootdir, experiment, key):
    """
    Makes a simple performance graph for a particular experiment with each individual run plotted.
    """
    test = []
    i = 1
    for f in glob.glob(f'{rootdir}\\{experiment}*'):
        with open(f'{f}\\Stats.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for g, row in enumerate(spamreader):
                test.append([f'run_{i}', int(g), float(row[2]), key])

        i += 1

    data = pd.DataFrame(test, columns=['run', 'generation', 'mean_fitness', 'key'])

    return data


def simple_plot(frames):
    result = pd.concat(frames, ignore_index=True)

    print(result)

    sns.set_theme()
    sns.lineplot(data=result, x='generation', y='mean_fitness', hue='key', ci=95)
    #plt.set(yscale='log')
    sns.set_style("ticks")
    plt.xticks(np.arange(0, 21, 2))
    #plt.ylim(0, 10000)
    plt.xlim(0, 20)
    plt.show()
