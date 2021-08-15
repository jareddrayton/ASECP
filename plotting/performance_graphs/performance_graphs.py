import glob
import csv

import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt


def performance_graph(path, identifier):
    """
    PLots a simple performance graph for a particular experiment where each individual run is plotted.
    """
    test = {}
    i = 1
    for f in glob.glob(f'{path}\\{identifier}*'):
        a = []
        with open(f'{f}\\Stats.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for row in spamreader:
                a.append(row[0])
        test[f'run_{i}'] = a
        i += 1

    data = pd.DataFrame(test, dtype=float)
    
    sns.set_theme()
    sns.lineplot(data=data)
    plt.xticks(np.arange(0, 21, 2))
    plt.show()


def performance_graph_confidence_interval(path, identifier):
    """
    Makes a simple performance graph for a particular experiment with each individual run plotted.
    """
    test = []
    i = 1
    for f in glob.glob(f'{path}\\{identifier}*'):
        with open(f'{f}\\Stats.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for g, row in enumerate(spamreader):
                test.append([f'run_{i}', int(g), float(row[0])])

        i += 1

    data = pd.DataFrame(test, columns=['run', 'generation', 'mean_fitness'])

    sns.set_theme()
    sns.lineplot(data=data, x='generation', y='mean_fitness')
    
    sns.plt.xticks(np.arange(0, 21, 4))
    #g.set_xticklabels(['0','5','10','15','20'])
    plt.show()


def performance_graph_standard_deviation(path, identifier):
    """
    Makes a simple performance graph for a particular experiment with each individual run plotted.
    """
    test = []
    i = 1
    for f in glob.glob(f'{path}\\{identifier}*'):
        with open(f'{f}\\Stats.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ')
            for g, row in enumerate(spamreader):
                test.append([f'run_{i}', int(g), float(row[0])])

        i += 1

    data = pd.DataFrame(test, columns=['run', 'generation', 'mean_fitness'])

    sns.set_theme()
    sns.lineplot(data=data, x='generation', y='mean_fitness', ci='sd')
    plt.show()

performance_graph('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_distance_metrics', 'Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.EUC')

performance_graph('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_distance_metrics', 'Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.SAD')

performance_graph('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_distance_metrics', 'Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.SSD')

#performance_graph_confidence_interval('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_distance_metrics', 'Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.EUC')

#performance_graph_standard_deviation('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_distance_metrics', 'Primary1.wav.PRT.Gen20.Pop100.Mut0.15.Sd0.15.hz.EUC')


