import csv
import json
import time

import matplotlib.pyplot as plt


def write_formants(name, directory, currentgeneration, individualfrequencies, fitness, voiced, absolutefitness):
    csvdata = list(individualfrequencies)
    csvdata.append(fitness)
    csvdata.append(voiced)
    csvdata.append(absolutefitness)

    with open('{}/Generation{!s}/Stats.csv'.format(directory, currentgeneration), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(csvdata)

def statistics(average_fitness, minimum_fitness, top_individual, directory):
    """ Function for plotting performance graphs and saving run data"""
    with open('{}/Mean.txt'.format(directory), 'w') as f:
        for item in average_fitness:
            f.write('{!s}\n'.format(item))

    with open('{}/Minimum.txt'.format(directory), 'w') as f:
        for item in minimum_fitness:
            f.write('{!s}\n'.format(item))
    
    with open('{}/Best.txt'.format(directory), 'w') as f:
        for item in top_individual:
            f.write('{!s}\n'.format(item))


def summary(directory, top_individual):
    with open(directory / 'summary.html', 'w') as f:
        for i, top in enumerate(top_individual):
            f.write('<audio controls>\n')
            f.write('            <source src="Generation{}\\Individual{}.wav" type="audio/wav">\n'.format(i, top))
            f.write('            Your browser does not support the audio element.\n')
            f.write('        </audio><br>\n')


def performance_graph(average_fitness, minimum_fitness, generation_size, directory):
    plt.plot(average_fitness, 'k', label='Mean Fitness')
    plt.plot(minimum_fitness, 'k--', label='Minimum Fitness')
    plt.axis([0, generation_size, 0, max(average_fitness)])
    plt.xlabel('Generation_size')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig("{}/Performance Graph".format(directory))


def csv_file(average_fitness, minimum_fitness, voiced_percentage, directory):
    with open('{}/Stats.csv'.format(directory), 'w', newline='') as csvfile:
        for i in range(len(average_fitness)):
            csvdata = (average_fitness[i], minimum_fitness[i], voiced_percentage[i])
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(csvdata)


def config_dump(directory, start_time, args):
    with open(directory / 'Runtime.txt', 'w') as run:
        run.write('--- {} seconds ---'.format(time.time() - start_time))

    with open(directory / 'arguments.json', 'w') as outfile:
        json.dump(vars(args), outfile, indent=4)
