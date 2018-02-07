import csv

import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.violinplot.html
# read in the mean fitness of each generation for each run and average it.

my_data = []

# no of runs

    
directory = "vowel-05.wav Gen 5 Pop 20 Mut 0.2 Sd 0.2 hz SSD none "

column = []

#Generations
for g in range(6):
    
    column = []
    for r in range(5):
        with open('{}{!s}/Generation{!s}/Stats.csv'.format(directory, r, g)) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(row[5])
                column.append(float(row[5]))

    my_data.append(column)   

print(my_data)

blah = np.array(my_data)
print(np.shape(my_data))


plt.boxplot(my_data)
plt.show()
