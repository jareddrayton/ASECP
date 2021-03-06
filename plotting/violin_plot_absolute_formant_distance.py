import csv

import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.violinplot.html
# read in the mean fitness of each generation for each run and average it.

directory = "vowel-13_22500.wav Gen 15 Pop 100 Mut 0.2 Sd 0.2 erb SSD none "

# number of generations
generations = 15 + 1

# number of runs
runs = 7 + 1

# list for holding data
my_data = []

for g in range(generations):
    
    column = []
    for r in range(runs):
        with open('{}{!s}/Generation{!s}/Stats.csv'.format(directory, r, g)) as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
            for row in spamreader:
                print(row[5])
                column.append(float(row[5]))

    my_data.append(column)   

print(my_data)

blah = np.array(my_data)
print(np.shape(my_data))


# Make a violin plot of the data and save it
plt.violinplot(my_data,
               showmeans=True,
               showmedians=False)
plt.xlabel('Generation')
plt.ylabel('Absolute difference in formant values measure in Hz')
plt.ylim(0, 30000)

plt.savefig(directory + 'Violin_std.pdf', transparent=True)
plt.show()


# Make a violin plot of the data but with a logirthmic y axis
plt.yscale('log')
plt.violinplot(my_data,
               showmeans=True,
               showmedians=False)
plt.xlabel('Generation')
plt.ylabel('Absolute difference in formant values measure in Hz')

plt.savefig(directory + 'Violin_log.pdf', transparent=True)             
plt.show()
