import csv

import matplotlib.pyplot as plt
import numpy as np

# https://matplotlib.org/devdocs/api/_as_gen/matplotlib.axes.Axes.violinplot.html
# read in the mean fitness of each generation for each run and average it.

my_data = []

# no of runs

    
directory = "vowel-05.wav Gen 5 Pop 20 Mut 0.2 Sd 0.2 hz SSD none {!s}".format(i)

column = []

#Generations
for r in range(6):
    
    for g in range()
        with open('{}/Generation{!s}/Stats.csv'.format(directory,r)) as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            #print(row[0])
            column.append(float(row[5]))

    my_data.append(column)   
#print(my_data)

print(my_data)


plt.violinplot(my_data,
               showmeans=False,
               showmedians=False)
plt.show()


# Correct
shifted = np.array(my_data)
print(shifted)

plt.violinplot(shifted,
               showmeans=False,
               showmedians=False)
plt.show()



shifted = np.transpose(shifted)
print(shifted)

plt.violinplot(shifted,
               showmeans=False,
               showmedians=False)
plt.show()

