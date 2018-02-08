import csv

import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.violinplot.html
# read in the mean fitness of each generation for each run and average it.

my_data = []

for i in range(5):
    
    directory = "vowel-05.wav Gen 5 Pop 20 Mut 0.2 Sd 0.2 hz SSD none {!s}".format(i)

    column = []
    
    with open('{}/Stats.csv'.format(directory)) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            print(row[0])
            column.append(float(row[0]))

    my_data.append(column)   
    print(my_data)

plt.boxplot(my_data)
plt.show()
