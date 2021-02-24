import csv
import json
import time

import matplotlib.pyplot as plt


def write_individual_to_csv(class_dict, directory, currentgeneration):
    csv_data = []
    
    csv_data.append(class_dict['name'])
    csv_data.append(class_dict['raw_fitness'])
    csv_data.append(class_dict['scaled_fitness'])
    csv_data.append(class_dict['absolute_fitness'])
    csv_data.append(class_dict['selection_probability'])
    csv_data += class_dict['formants']
    csv_data.append(class_dict['voiced'])
    csv_data.append(class_dict['mean_pitch'])
    csv_data.append(class_dict['frac_frames'])
    csv_data.append(class_dict['voice_breaks'])

    with open('{}/Generation{!s}/individual_info_table.csv'.format(directory, currentgeneration), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(csv_data)


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
