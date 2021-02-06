import csv
import matplotlib.pyplot as plt
import os
import pathlib
import random
import shutil
import time
from tqdm import tqdm

import arguments
import fitness_functions
import genetic_operators
import praat_control
import stats
from CONSTANTS import PARAMETER_LISTS

###################################################################################################
# Variables provided at the cmd line using argparse

args = arguments.get_user_args()

###################################################################################################
# Unpacking the variables from argparse

# The target sound to be matched
soundfile = args.soundfile

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
loudness_measure = args.loudness_measure
filterbank_type = args.filterbank_type
identifier = args.identifier

# Constants that are flags
PARALLEL = args.parallel
CNTK = args.cntk

###################################################################################################
# Set the time to measure the length of a run
start_time = time.time()

# If True, the identifier variable is used as a seed for random number generation
# if False:
#     random.seed(int(identifier))



# Creates the directory string
prefix = '{}.Gen{}.Pop{}.Mut{}.Sd{}.'.format(soundfile,
                                                 generation_size,
                                                 population_size,
                                                 mutation_rate,
                                                 mutation_standard_dev)


root_data_directory = pathlib.Path.cwd().parent / 'data'


if fitness_type == 'formant':
    directory = root_data_directory / '{}{} {} {} {}'.format(prefix, formant_repr, distance_metric, loudness_measure, identifier)
elif fitness_type == 'filterbank':
    directory = root_data_directory / '{}{} {}'.format(prefix, filterbank_type, identifier)



print(directory)

# Makes the directory for all subsequent files
if directory.exists():
    shutil.rmtree(directory)

os.mkdir(directory)

soundfile = '{}'.format(soundfile)

# Call the "praat_control" module to get target sound features
target_length = praat_control.get_time(soundfile)
target_sample_rate = praat_control.get_sample_rate(soundfile)
target_formants = praat_control.get_target_formants(target_length, soundfile, formant_range)
target_intensity = praat_control.get_target_intensity(soundfile)
target_rms = praat_control.get_target_RMS(soundfile)

target_mfcc_average = praat_control.get_target_mfcc_average(soundfile)
target_logfbank_average = praat_control.get_target_logfbank_average(soundfile)
target_mfcc = praat_control.get_target_mfcc(soundfile)
target_logfbank = praat_control.get_target_logfbank(soundfile)


# Sets the length of individuals to equal the target. Can be overwrriten with a string
length = target_length  # "0.5"

###################################################################################################
###################################################################################################

class Individual:
    def __init__(self, name):

        self.name = name

        # List containing the real valued genotype
        self.values = []

        # Load parameters fomr CONSTANTS file
        self.parameters = PARAMETER_LISTS['CONSTRAINED']

        # Initialise the fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.selection_probability = 0

        # Initialise the genotype with random values for the first generation
        if current_generation_index == 0:
            self.values = [round(random.uniform(-1, 1), 1) for x in range(len(self.parameters))]

    # Method for creating a Praat .artword file
    def create_artword(self):

        self.artword = open("{}/Generation{!s}/Individual{!s}.praat".format(directory, current_generation_index, self.name), "w")

        # Configure speaker type and sound length
        self.artword.write('Create Speaker... Robovox Male 2\r\n')
        self.artword.write('Create Artword... Individual{} {}\r\n'.format(self.name, length))

        # Specify Lungs and LevatorPalatini parameter values
        self.artword.write('Set target... 0.0  0.07  Lungs\r\n')
        self.artword.write('Set target... 0.04  0.0  Lungs\r\n')
        self.artword.write('Set target... {}  0.0  Lungs\r\n'.format(length))
        self.artword.write('Set target... 0.00  1 LevatorPalatini\r\n')
        self.artword.write('Set target... {}  1 LevatorPalatini\r\n'.format(length))
        self.artword.write('Set target... 0.0  0.5 Interarytenoid\r\n')
        self.artword.write('Set target... {}  0.5 Interarytenoid\r\n'.format(length))

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(self.parameters)):
            self.artword.seek(0, 2)
            self.artword.write('Set target... 0.0 {} {}\r\n'.format(self.values[i],self.parameters[i]))
            self.artword.write('Set target... {} {} {}\r\n'.format(length, self.values[i],self.parameters[i]))

        # Set sample rate and synthesise audio
        self.artword.write('select Artword Individual{}\r\n'.format(self.name))
        self.artword.write('plus Speaker Robovox\r\n')
        self.artword.write('To Sound... {} 25    0 0 0    0 0 0   0 0 0\r\n'.format(target_sample_rate))
        self.artword.write('''nowarn do ("Save as WAV file...", "Individual{}.wav")\r\n'''.format(self.name))

        # Extract formants, pitch, and intensity
        self.artword.write('''selectObject ("Sound Individual{}_Robovox")\r\n'''.format(self.name))
        self.artword.write('To Formant (burg): 0, 5, 5000, {}, 50\r\n'.format(length))
        self.artword.write('List: "no", "yes", 6, "no", 3, "no", 3, "no"\r\n')
        self.artword.write('''appendFile ("formants{}.txt", info$ ())\r\n'''.format(self.name))
        self.artword.write('''selectObject ("Sound Individual{}_Robovox")\r\n'''.format(self.name))
        self.artword.write('To Pitch: {}, 75, 600\r\n'.format(length))
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
        self.voiced = praat_control.get_individual_pitch(self.name, directory, current_generation_index)
        
        # If a pitch is detected the formants are calculated and assigned to self.formants
        if self.voiced == True:
            self.formants = praat_control.get_individual_formants(self.name, directory, current_generation_index, target_sample_rate)
        else:
            self.formants = [target_sample_rate/2 for x in range(5)]
        
        # 
        self.formants = self.formants[0:formant_range]

        # This acts as a baseline fitness attribute to compare different fitness functions
        self.absolutefitness = fitness_functions.fitness_a1(self.formants, target_formants, "SAD")
        
        # print("absolute fitness", self.absolutefitness)
    
    # Method for calculating an individuals fitness
    def evaluate_formant(self):
        
        self.voiced_penalty()

       
       # Calls the relevant fitness function based on cmd line argument
        if formant_repr == "hz":
            self.raw_fitness = fitness_functions.fitness_a1(self.formants, target_formants, distance_metric)
        elif formant_repr == "mel":
            self.raw_fitness = fitness_functions.fitness_a2(self.formants, target_formants, distance_metric)
        elif formant_repr == "cent":
            self.raw_fitness = fitness_functions.fitness_a3(self.formants, target_formants, distance_metric)
        elif formant_repr == "bark":
            self.raw_fitness = fitness_functions.fitness_a4(self.formants, target_formants, distance_metric)
        elif formant_repr == "erb":
            self.raw_fitness = fitness_functions.fitness_a5(self.formants, target_formants, distance_metric)
        
        elif formant_repr == "brito":
            self.raw_fitness = fitness_functions.fitness_brito(self.formants, target_formants)
        
        # Apply a penalty of the sound is not voiced
        if self.voiced == False:
            self.raw_fitness = self.raw_fitness * 10

        # Extract loudness features
        self.intensity = praat_control.get_individual_intensity(self.name, directory, current_generation_index, target_intensity)
        self.rms = praat_control.get_individual_RMS(self.name, directory, current_generation_index, target_rms)

        # Apply loudness co-efficents
        if loudness_measure == "rms":
            self.raw_fitness = self.raw_fitness * self.rms
        elif loudness_measure == "intensity":
            self.raw_fitness = self.raw_fitness * self.intensity
        elif loudness_measure == "both":
            self.raw_fitness = self.raw_fitness * ((self.rms + self.intensity) / 2.0)
        elif loudness_measure == "none":
            pass

        ###########################################################################################
        # Write feature information to a csv file
        
        stats.write_formants(self.name,
                             directory,
                             current_generation_index,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
        ###########################################################################################
        # Call the write_formants_cntk method if a sound is voiced

        if self.voiced and CNTK:
            self.write_formants_cntk()

    
    def evaluate_filterbank(self):
        # MFCC and filterbank based fitness functions
        
        self.voiced_penalty()

        if filterbank_type == "mfcc_average":
            self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_mfcc_average(target_mfcc_average, self.mfcc_average, distance_metric)

        elif filterbank_type == "logfbank_average":
            self.logfbank_average = praat_control.get_individual_logfbank_average(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_logfbank_average(target_logfbank_average, self.logfbank_average, distance_metric)

        elif filterbank_type == "mfcc_sad":
            self.mfcc = praat_control.get_individual_mfcc(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(target_mfcc, self.mfcc)

        elif filterbank_type == "mfcc_ssd":
            self.mfcc = praat_control.get_individual_mfcc(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(target_mfcc, self.mfcc)

        elif filterbank_type == "logfbank_sad":
            self.logfbank = praat_control.get_individual_logfbank(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(target_logfbank, self.logfbank)

        elif filterbank_type == "logfbank_ssd":
            self.logfbank = praat_control.get_individual_logfbank(self.name, directory, current_generation_index)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(target_logfbank, self.logfbank)
        
        stats.write_formants(self.name,
                             directory,
                             current_generation_index,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
        
        if self.voiced and CNTK:
            self.write_filterbank_cntk()

    ###############################################################################################

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
        
        self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, directory, current_generation_index)

        with open('cntk_mfcc_data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(x) for x in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(x) for x in self.mfcc_average)))
        

###################################################################################################
###################################################################################################

# Creates a list of strings for use as keys in a dictionary
keys = [str(x) for x in range(population_size)]

# Create an empty dictionary for storing Individual instances
population = {}

# Lists to hold fitness stats
average_fitness = []
minimum_fitness = []
voiced_percentage = []

# Main loop containg all Genetic Algorithm logic
for current_generation_index in range(generation_size + 1):

    # Creates a folder for the current generation
    os.mkdir(directory / 'Generation{!s}'.format(current_generation_index))

    # If it is the first generation, instantiate the Indiviudal class and associate it with
    # a key in the population dictionary
    if current_generation_index == 0:
        for name in keys:
            population[name] = Individual(name)

    # Call the artword method for object in the population dictionary
    for name in keys:
        population[name].create_artword()

    # Synthesise artwords and run a single or multiple instances of Praat
    if PARALLEL == True:
        praat_control.synthesise_artwords_threadpool(directory, current_generation_index, population_size)
    elif PARALLEL == False:
        praat_control.synthesise_artwords_serial(current_generation_index, population_size, directory)

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

    numbered_list = list(enumerate(listfitness))

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
    # Elitism

    elites = genetic_operators.elitism(population, keys, elite_size)

    ###############################################################################################
    # Selection
    # Assigns selection probability
    if selection_type == "linear":
        genetic_operators.linear_ranking(population, keys)
    elif selection_type == "proportional":
        genetic_operators.fitness_proportional(population, keys)
    elif selection_type == "exponential":
        genetic_operators.exponential_ranking(population, keys)

    ###############################################################################################
    # Crossover
    print("yelp")
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
    
    ##############################################################################################

    # Finish the loop by incrementing the generation counter index by 1
    # current_generation_index += 1



###################################################################################################
# Statisticss stuff

def statistics():
    """ Function for plotting performance graphs and saving run data"""
    with open("{}/Mean.txt".format(directory), "w") as mean:
        for item in average_fitness:
            mean.write("{!s}\r\n".format(item))

    with open("{}/Minimum.txt".format(directory), "w") as minimum:
        for item in minimum_fitness:
            minimum.write('{!s}\r\n'.format(item))
statistics()

def performance_graph():
    plt.plot(average_fitness, 'k', label='Mean Fitness')
    plt.plot(minimum_fitness, 'k--', label='Minimum Fitness')
    plt.axis([0, generation_size, 0, max(average_fitness)])
    plt.xlabel('Generation_size')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig("{}/Performance Graph".format(directory))
performance_graph()


def csv_file():
    with open('{}/Stats.csv'.format(directory), 'w', newline='') as csvfile:
        for i in range(len(average_fitness)):
            csvdata = (average_fitness[i], minimum_fitness[i], voiced_percentage[i])
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(csvdata)
csv_file()

def runtime():
    with open(directory / 'Runtime.txt', 'w') as run:
        run.write("--- %d seconds ---" % (time.time() - start_time))
runtime()

time.sleep(2)
