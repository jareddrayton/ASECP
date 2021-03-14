import csv
import json
import os
import pathlib
import random
import shutil
import subprocess
import time
from operator import itemgetter

from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np

import arguments
import fitness_functions
import genetic_operators
import praat_control
import stats
import vocal_tract_control
from individual_class import Individual_PRT, Individual_VTL


def get_target_info(target_dict):

    target_dict['target_length'] = praat_control.get_time(target_dict['file_path'])
    target_dict['target_sample_rate'] = praat_control.get_sample_rate(target_dict['file_path'])
    target_dict['target_formants'] = praat_control.write_target_formant_table(target_dict['file_path_root'], target_dict['file_name'])
    target_dict['target_intensity'] = praat_control.get_target_intensity(target_dict['file_path'])
    target_dict['target_rms'] = praat_control.get_target_RMS(target_dict['file_path'])
    target_dict['target_mfcc_average'] = praat_control.get_target_mfcc_average(target_dict['file_path'])
    target_dict['target_logfbank_average'] = praat_control.get_target_logfbank_average(target_dict['file_path'])
    target_dict['target_fbank_average'] = praat_control.get_target_fbank_average(target_dict['file_path'])
    target_dict['target_mfcc'] = praat_control.get_target_mfcc(target_dict['file_path'])
    target_dict['target_logfbank'] = praat_control.get_target_logfbank(target_dict['file_path'])


def main():

    start_time = time.time()

    args = arguments.get_user_args()
    print(vars(args))
    target_dict = vars(args).copy()
    
    #import pdb;pdb.set_trace()
    # The target sound to be matched
    target_dict['file_name'] = args.soundfile

    # Genetic operator variables
    population_size = args.population_size
    generation_size = args.generation_size
    mutation_rate = args.mutation_rate
    mutation_standard_dev = args.mutation_standard_dev
    selection_type = args.selection_type
    crossover_type = args.crossover_type
    mutation_type = args.mutation_type
    elitism = args.elitism
    elite_size = args.elite_size

    # Fitness function variables
    fitness_type = args.fitness_type
    formant_repr = args.formant_repr
    distance_metric = args.distance_metric
    filterbank_type = args.filterbank_type
    identifier = args.identifier

    # If True, the identifier variable is used as a seed for random number generation
    """
    if True:
        random.seed(2000)
    """
    # Creates the directory string
    prefix = '{}.{}.Gen{}.Pop{}.Mut{}.Sd{}.'.format(target_dict['file_name'],
                                                    target_dict['synthesiser'],
                                                    generation_size,
                                                    population_size,
                                                    mutation_rate,
                                                    mutation_standard_dev)

    parent_dir = pathlib.Path.cwd().parent

    root_data_directory = parent_dir / 'data'
    root_praat_directory = parent_dir / 'praat'
    root_vtl_directory = parent_dir / 'vocaltractlab'
    root_target_sounds_directory = parent_dir / 'target_sounds'

    if fitness_type == 'formant':
        directory = root_data_directory / '{}{}.{}.id{}'.format(prefix, formant_repr, distance_metric, identifier)
    elif fitness_type == 'filterbank':
        directory = root_data_directory / '{}{}.id{}'.format(prefix, filterbank_type, identifier)

    # Makes the directory for all subsequent files
    if directory.exists() and target_dict['overwrite']:
        shutil.rmtree(directory)
        os.mkdir(directory)
    elif directory.exists():
        raise IOError
    else:
        os.mkdir(directory)


    target_dict['file_path_root'] = root_target_sounds_directory
    target_dict['file_path'] = root_target_sounds_directory / target_dict['file_name']

    # Update target_dict with information relating to the target sound
    get_target_info(target_dict)

    # Creates a list of strings for use as keys in a dictionary
    keys = [str(x) for x in range(population_size)]

    # Create an empty dictionary for storing Individual instances
    population = {}

    average_fitness = []
    minimum_fitness = []
    voiced_percentage = []
    top_individual = []

    if target_dict['synthesiser'] == 'PRT':
        Individual = Individual_PRT
    elif target_dict['synthesiser'] == 'VTL':
        Individual = Individual_VTL
    
    for current_generation_index in tqdm(range(generation_size + 1), desc=prefix):

        # Create a directory for the current generation
        os.mkdir(directory / 'Generation{!s}'.format(current_generation_index))

        # Instantiate the Indiviudal class and associate it with a key in the population dictionary
        if current_generation_index == 0:
            for name in keys:
                population[name] = Individual(name, target_dict, directory)

        for name in keys:
            population[name].current_generation = current_generation_index

        # Create the config files that drive a paticular synthesiser
        for name in keys:
            population[name].create_synth_params()

        # Synthesise Individual sounds using the config files
        if target_dict['synthesiser'] == 'PRT':
            praat_control.synthesise_artwords_threadpool(directory, current_generation_index, population_size)
        elif target_dict['synthesiser'] == 'VTL':
            vocal_tract_control.synthesise_tracts_threadpool(directory, current_generation_index, population_size)

        # Calculate fitness scores by calling the evaluate_formants method
        for name in keys:
            population[name].evaluate_fitness(target_dict['fitness_type'])


        ###############################################################################################
        # Calculate the percentage of voiced sounds in the generation
        # Should be able to move this to stats module now that this data is written out.
        
        voiced_total = 0.0

        for name in keys:
            if population[name].voiced:
                voiced_total += 1

        voiced_percentage.append(voiced_total / population_size)

        ###############################################################################################
        # Store Elite Candidates

        elites = genetic_operators.elitism(population, keys, elite_size)

        ###############################################################################################
        # Selection Probabilities used with Roulette Wheel or Stochastic Universal Sampling
        if selection_type == 'linear':
            genetic_operators.linear_ranking(population, keys)
        elif selection_type == 'proportional':
            genetic_operators.fitness_proportional(population, keys)
        elif selection_type == 'exponential':
            genetic_operators.exponential_ranking(population, keys)


        ###############################################################################################
        # Have to write out data here to include correct selection probability.
        for name in keys:
            population[name].write_out_data()

        # do fitness statistics
        listfitness = []

        ordered = []

        for name in keys:
            listfitness.append(population[name].raw_fitness)
            ordered.append((population[name].name, population[name].raw_fitness, population[name].selection_probability))
        
        ordered = sorted(ordered, key=itemgetter(1))

        top_individual.append(ordered[0][0])

        average_fitness.append(sum(listfitness) / len(listfitness))
        minimum_fitness.append(min(listfitness))

        ###############################################################################################
        # Crossover
        if crossover_type == 'one_point':
            genetic_operators.one_point_crossover(population, keys)
        elif crossover_type == 'uniform':
            genetic_operators.uniform_crossover(population, keys)

        ##############################################################################################
        # Apply mutation to individuals
        if mutation_type == 'gaussian':
            genetic_operators.gaussian_mutation(population, keys, mutation_rate, mutation_standard_dev)
        elif mutation_type == 'uniform':
            genetic_operators.uniform_mutation(population, keys, mutation_rate)
        elif mutation_type == 'disabled':
            pass
        else:
            raise IOError

        ##############################################################################################
        # Elitism
        if elitism == True:
            for i in range(elite_size):
                population[keys[i]].values = elites[i]

    stats.performance_graph(average_fitness, minimum_fitness, generation_size, directory)
    stats.config_dump(directory, start_time, args)
    stats.statistics(average_fitness, minimum_fitness, top_individual, directory)
    stats.csv_file(average_fitness, minimum_fitness, voiced_percentage, directory)
    stats.summary(directory, top_individual)


if __name__ == '__main__':
    main()
