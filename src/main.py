import csv
import json
import os
import pathlib
import random
import shutil
import subprocess
import time

import matplotlib.pyplot as plt
import numpy as np

import arguments
import fitness_functions
import genetic_operators
import praat_control
import stats
import vocal_tract_control
from CONSTANTS import PRT_PARAMETER_DEFS, VTL_PARAMETER_DEFS


class Individual_PRT:
    def __init__(self, name, target_info, directory):

        self.name = name

        # A dictionary containing information about the target sound
        self.target_info = target_info

        # Set the run directory
        self.directory = directory

        # Initialise fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.selection_probability = 0

        self.current_generation = 0

        # List for holding the real valued genotype values
        self.values = []

        # Load parameter definition from the CONSTANTS module
        self.parameters = PRT_PARAMETER_DEFS['ALL']

        # Initialise the genotype with random values for the first generation
        if self.current_generation == 0:
            self.values = [round(random.uniform(-1, 1), 1) for x in range(len(self.parameters))]

    # Method for creating a Praat .artword file
    def create_synth_params(self):

        self.artword = open("{}/Generation{!s}/Individual{!s}.praat".format(self.directory, self.current_generation, self.name), "w")

        # Configure speaker type and sound length
        self.artword.write('Create Speaker... Robovox Male 2\r\n')
        self.artword.write('Create Artword... Individual{} {}\r\n'.format(self.name, self.target_info['target_length']))

        # Specify Lungs and LevatorPalatini parameter values
        self.artword.write('Set target... 0.0  0.07  Lungs\r\n')
        self.artword.write('Set target... 0.04  0.0  Lungs\r\n')
        self.artword.write('Set target... {}  0.0  Lungs\r\n'.format(self.target_info['target_length']))
        self.artword.write('Set target... 0.00  1 LevatorPalatini\r\n')
        self.artword.write('Set target... {}  1 LevatorPalatini\r\n'.format(self.target_info['target_length']))
        self.artword.write('Set target... 0.0  0.5 Interarytenoid\r\n')
        self.artword.write('Set target... {}  0.5 Interarytenoid\r\n'.format(self.target_info['target_length']))

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(self.parameters)):
            self.artword.seek(0, 2)
            self.artword.write('Set target... 0.0 {} {}\r\n'.format(self.values[i],self.parameters[i]))
            self.artword.write('Set target... {} {} {}\r\n'.format(self.target_info['target_length'], self.values[i],self.parameters[i]))

        # Set sample rate and synthesise audio
        self.artword.write('select Artword Individual{}\r\n'.format(self.name))
        self.artword.write('plus Speaker Robovox\r\n')
        self.artword.write('To Sound... {} 25    0 0 0    0 0 0   0 0 0\r\n'.format(self.target_info['target_sample_rate']))
        self.artword.write('''nowarn do ("Save as WAV file...", "Individual{}.wav")\r\n'''.format(self.name))

        # Extract formants, pitch, and intensity
        self.artword.write('''selectObject ("Sound Individual{}_Robovox")\r\n'''.format(self.name))
        self.artword.write('To Formant (burg): 0, 5, 5000, {}, 50\r\n'.format(self.target_info['target_length']))
        self.artword.write('List: "no", "yes", 6, "no", 3, "no", 3, "no"\r\n')
        self.artword.write('''appendFile ("formants{}.txt", info$ ())\r\n'''.format(self.name))
        self.artword.write('''selectObject ("Sound Individual{}_Robovox")\r\n'''.format(self.name))
        self.artword.write('To Pitch: {}, 75, 600\r\n'.format(self.target_info['target_length']))
        self.artword.write('Get mean: 0, 0, "Hertz"\r\n')
        self.artword.write('''appendFile ("pitch{}.txt", info$ ())\r\n'''.format(self.name))
        self.artword.write('''selectObject ("Sound Individual{}_Robovox")\r\n'''.format(self.name))
        self.artword.write('To Intensity: 100, 0, "yes"\r\n')
        self.artword.write('Get standard deviation: 0, 0\r\n')
        self.artword.write('''appendFile ("intensity{}.txt", info$ ())\r\n'''.format(self.name))

        self.artword.close()

    def voiced_penalty(self):
        """
        Instance method for ascertaining whether an individual is voiced or not.
        
        """
        # Assigns True or False to self.voiced, based on whether praat can calculate pitch 
        self.voiced = praat_control.get_individual_pitch(self.name, self.directory, self.current_generation)
        
        # If a pitch is detected the formants are calculated and assigned to self.formants
        if self.voiced == True:
            self.formants = praat_control.get_individual_formants(self.name, self.directory, self.current_generation, self.target_info['target_sample_rate'])
        else:
            self.formants = [self.target_info['target_sample_rate'] / 2 for x in range(5)]
        
        # 
        self.formants = self.formants[0:self.target_info['formant_range']]

        # This acts as a baseline fitness attribute to compare different fitness functions
        self.absolutefitness = fitness_functions.fitness_a1(self.formants, self.target_info['target_formants'], "SAD")
        
        # print("absolute fitness", self.absolutefitness)
    
    # Method for calculating an individuals fitness
    def evaluate_formant(self):
        
        self.voiced_penalty()

       
       # Calls the relevant fitness function based on cmd line argument
        if self.target_info['formant_repr'] == "hz":
            self.raw_fitness = fitness_functions.fitness_a1(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == "mel":
            self.raw_fitness = fitness_functions.fitness_a2(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == "cent":
            self.raw_fitness = fitness_functions.fitness_a3(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == "bark":
            self.raw_fitness = fitness_functions.fitness_a4(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == "erb":
            self.raw_fitness = fitness_functions.fitness_a5(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        
        elif self.target_info['formant_repr'] == "brito":
            self.raw_fitness = fitness_functions.fitness_brito(self.formants, self.target_info['target_formants'])
        
        # Apply a penalty of the sound is not voiced
        if self.voiced == False:
            self.raw_fitness = self.raw_fitness * 10

        # Extract loudness features
        self.intensity = praat_control.get_individual_intensity(self.name, self.directory, self.current_generation, self.target_info['target_intensity'])
        self.rms = praat_control.get_individual_RMS(self.name, self.directory, self.current_generation, self.target_info['target_rms'])

        # Apply loudness co-efficents
        if self.target_info['loudness_measure'] == "rms":
            self.raw_fitness = self.raw_fitness * self.rms
        elif self.target_info['loudness_measure'] == "intensity":
            self.raw_fitness = self.raw_fitness * self.intensity
        elif self.target_info['loudness_measure'] == "both":
            self.raw_fitness = self.raw_fitness * ((self.rms + self.intensity) / 2.0)
        elif self.target_info['loudness_measure'] == "none":
            pass

        ###########################################################################################
        # Write feature information to a csv file
        
        stats.write_formants(self.name,
                             self.directory,
                             self.current_generation,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
        ###########################################################################################
        # Call the write_formants_cntk method if a sound is voiced

        if self.voiced and self.target_info['cntk']:
            self.write_formants_cntk()

    def evaluate_filterbank(self):
        # MFCC and filterbank based fitness functions
        
        self.voiced_penalty()

        if self.target_info['filterbank_type'] == "mfcc_average":
            self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_mfcc_average(self.target_info['target_mfcc_average'], self.mfcc_average, self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "logfbank_average":
            self.logfbank_average = praat_control.get_individual_logfbank_average(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_logfbank_average(self.target_info['target_logfbank_average'], self.logfbank_average, self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "mfcc_sad":
            self.mfcc = praat_control.get_individual_mfcc(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(self.target_info['target_mfcc'], self.mfcc)

        elif self.target_info['filterbank_type'] == "mfcc_ssd":
            self.mfcc = praat_control.get_individual_mfcc(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(self.target_info['target_mfcc'], self.mfcc)

        elif self.target_info['filterbank_type'] == "logfbank_sad":
            self.logfbank = praat_control.get_individual_logfbank(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(self.target_info['target_logfbank'], self.logfbank)

        elif self.target_info['filterbank_type'] == "logfbank_ssd":
            self.logfbank = praat_control.get_individual_logfbank(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(self.target_info['target_logfbank'], self.logfbank)
        
        stats.write_formants(self.name,
                             self.directory,
                             self.current_generation,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
        
        if self.voiced and self.target_info['cntk']:
            self.write_filterbank_cntk()

    def write_formants_cntk(self):
        """ writes features and labels to a file for use with CNTK in the following format
        |labels 0 0 0 0 0 0 0 1 0 0 |features 0 0 0 0 0 0 0 0 0 0 0

        :return:
        """

        with open('cntk_formant_data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(x) for x in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(x) for x in self.formants)))

    def write_filterbank_cntk(self):
        
        self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, self.directory, self.current_generation)

        with open('cntk_mfcc_data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(x) for x in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(x) for x in self.mfcc_average)))


class Individual_VTL:
    def __init__(self, name, target_info, directory):

        self.name = name

        # List containing the real valued genotype
        self.values = []

        # Load parameter definition from the CONSTANTS module
        self.parameters = VTL_PARAMETER_DEFS['ALL']

        # Initialise the fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0 # Used to calculate proporional fitness
        self.selection_probability = 0

        self.target_info = target_info

        self.directory = directory

        self.current_generation = 0

        # Initialise the genotype with random values for the first generation
        if self.current_generation == 0:
            self.values = [round(random.uniform(y, z), 1) for _, y, z in self.parameters]

    def create_synth_params(self):
        sample_rate = 44100
        target_time = 1.0
        fold_type = 'Geometric glottis'
        step_size = 110  # assume 44100 sample rate.
        target_pressure = 8000
        number_of_states = int((sample_rate * target_time) // step_size)
        pressure = np.geomspace(1, target_pressure, num=20)
        glottis_params = ['101.594', '0', '0.0102', '0.02035', '0.05', '1.22204', '1', '0.05', '0', '25', '-10']

        with open('{}\\Generation{}\\tract_seq{}.txt'.format(self.directory, self.current_generation, self.name), 'w') as f:
            f.write('# The first two lines (below the comment lines) indicate the name of the vocal fold model and the number of states.' + '\n')
            f.write('# The following lines contain the control parameters of the vocal folds and the vocal tract (states)' + '\n')
            f.write('# in steps of 110 audio samples (corresponding to about 2.5 ms for the sampling rate of 44100 Hz).' + '\n')
            f.write('# For every step, there is one line with the vocal fold parameters followed by' + '\n')
            f.write('# one line with the vocal tract parameters.' + '\n')

            f.write('#' + '\n')
            f.write(fold_type + '\n')
            f.write(str(number_of_states) + '\n')
            for state in pressure:
                glottis_params[1] = str(state)
                f.write(' '.join(glottis_params) + '\n')
                f.write(' '.join(map(str,self.values)) + '\n')
            
            glottis_params[1] = str(target_pressure)

            for _ in range(number_of_states - 20):
                f.write(' '.join(glottis_params) + '\n')
                f.write(' '.join(map(str,self.values)) + '\n')
    
    def get_formants(self):
        
        file_path = self.directory / self.current_generation
        praat_control.get_average_formants(file_path, self.target_info['formant_range'])


def get_target_info(formant_range, target_dict):

    target_dict['target_length'] = praat_control.get_time(target_dict['file_path'])
    target_dict['target_sample_rate'] = praat_control.get_sample_rate(target_dict['file_path'])
    target_dict['target_formants'] = praat_control.get_target_formants(target_dict['target_length'], target_dict['file_path'], formant_range)
    target_dict['target_intensity'] = praat_control.get_target_intensity(target_dict['file_path'])
    target_dict['target_rms'] = praat_control.get_target_RMS(target_dict['file_path'])
    target_dict['target_mfcc_average'] = praat_control.get_target_mfcc_average(target_dict['file_path'])
    target_dict['target_logfbank_average'] = praat_control.get_target_logfbank_average(target_dict['file_path'])
    target_dict['target_mfcc'] = praat_control.get_target_mfcc(target_dict['file_path'])
    target_dict['target_logfbank'] = praat_control.get_target_logfbank(target_dict['file_path'])


def main():
    # Store time to measure the length of a single run
    start_time = time.time()
    
    args = arguments.get_user_args()
    print(vars(args))
    target_dict = vars(args).copy()
    
    # The target sound to be matched
    target_dict['file_name'] = args.soundfile

    # Genetic operator variables
    population_size = args.population_size
    generation_size = args.generation_size
    mutation_rate = args.mutation_rate
    mutation_standard_dev = args.mutation_standard_dev
    selection_type = args.selection_type
    crossover_type = args.crossover_type
    elitism = args.elitism
    elite_size = args.elite_size
    runs = args.runs 

    # Fitness function variables
    fitness_type = args.fitness_type
    formant_range = args.formant_range
    formant_repr = args.formant_repr
    distance_metric = args.distance_metric
    filterbank_type = args.filterbank_type
    identifier = args.identifier

    # If True, the identifier variable is used as a seed for random number generation
    if True:
        random.seed(1998)

    # Creates the directory string
    prefix = '{}.Gen{}.Pop{}.Mut{}.Sd{}.'.format(target_dict['file_name'],
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
        directory = root_data_directory / '{}{} {}'.format(prefix, filterbank_type, identifier)

    # Makes the directory for all subsequent files
    if directory.exists():
        shutil.rmtree(directory)
    os.mkdir(directory)

    target_dict['file_path'] = root_target_sounds_directory / target_dict['file_name']

    # Update target_dict with information relating to the target sound
    get_target_info(formant_range, target_dict)

    # Creates a list of strings for use as keys in a dictionary
    keys = [str(x) for x in range(population_size)]

    # Create an empty dictionary for storing Individual instances
    population = {}

    average_fitness = []
    minimum_fitness = []
    voiced_percentage = []

    if target_dict['synthesiser'] == 'PRT':
        Individual = Individual_PRT
    elif target_dict['synthesiser'] == 'VTL':
        Individual = Individual_VTL
    
    for current_generation_index in range(generation_size + 1):

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
            if fitness_type == "formant":
                population[name].evaluate_formant()
            elif fitness_type == "filterbank":
                population[name].evaluate_filterbank()

        ###############################################################################################
        # do fitness statistics
        listfitness = []

        for name in keys:
            listfitness.append(population[name].raw_fitness)

        average_fitness.append(sum(listfitness) / len(listfitness))
        minimum_fitness.append(min(listfitness))

        ###############################################################################################
        # Calculate the percentage of voiced sounds in the generation
        
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
        if selection_type == "linear":
            genetic_operators.linear_ranking(population, keys)
        elif selection_type == "proportional":
            genetic_operators.fitness_proportional(population, keys)
        elif selection_type == "exponential":
            genetic_operators.exponential_ranking(population, keys)

        ###############################################################################################
        # Crossover
        if crossover_type == "one_point":
            genetic_operators.one_point_crossover(population, keys)
        elif crossover_type == "uniform":
            genetic_operators.uniform_crossover(population, keys)

        ##############################################################################################
        # Apply mutation to individuals

        genetic_operators.mutation(population, keys, mutation_rate, mutation_standard_dev)

        ##############################################################################################
        # Elitism
        
        if elitism == True:
            for i in range(elite_size):
                population[keys[i]].values = elites[i]
    
    performance_graph(average_fitness, minimum_fitness, generation_size, directory)
    dump(directory, start_time, args)
    statistics(average_fitness, minimum_fitness, directory)
    csv_file(average_fitness, minimum_fitness, voiced_percentage, directory)


def statistics(average_fitness, minimum_fitness, directory):
    """ Function for plotting performance graphs and saving run data"""
    with open("{}/Mean.txt".format(directory), "w") as mean:
        for item in average_fitness:
            mean.write("{!s}\r\n".format(item))

    with open("{}/Minimum.txt".format(directory), "w") as minimum:
        for item in minimum_fitness:
            minimum.write('{!s}\r\n'.format(item))


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


def dump(directory, start_time, args):
    with open(directory / 'Runtime.txt', 'w') as run:
        run.write('--- {} seconds ---'.format(time.time() - start_time))

    with open(directory / 'arguments.json', 'w') as outfile:
        print(vars(args))
        json.dump(vars(args), outfile, indent=4)


if __name__ == '__main__':
    main()
