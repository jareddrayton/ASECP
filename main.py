import os
import random
import time
import csv
import argparse
import matplotlib.pyplot as plt

import fitnessfunction
import genop
import praatcontrol
import stats

###################################################################################################
# Variables provided at the cmd line using argparse

parser = argparse.ArgumentParser()

parser.add_argument("-sf", "--soundfile",
                    type=str,
                    default='vowel-01.wav',
                    help="sets the filename of the target sound")

parser.add_argument("-ps", "--populationsize", 
					type=int,
					default=10,
                    help="sets the population size")

parser.add_argument("-gs", "--generations",
					type=int, 
					default=2,
                    help="sets the number of generations")

parser.add_argument("-mr", "--mutationrate",
					type=float, 
					default=0.2,
                    help="sets the rate of mutation")

parser.add_argument("-sd", "--standarddev",
					type=float, 
					default=0.2,
                    help="sets the gaussian standard deviation")

parser.add_argument("-ft", "--fitnesstype",
					type=str,
					default='formant',
					help="choose between formant or filterbank")

parser.add_argument("-nf", "--noformants",
                    type=int,
                    default=3,
                    help="sets the number of formants used for analysis")

parser.add_argument("-fr", "--formantrepresentation",
					type=str,
					default='hz',
					help="Choose the type of formant fitness function")

parser.add_argument("-dm", "--distancemetric",
					type=str,
					default='SSD',
					help="Choose the type of distance metrics")

parser.add_argument("-lm", "--loudnessmeasure",
					type=str,
					default='none',
					help="Choose the type of loudness co-efficent")

parser.add_argument("-fb", "--fffilterbank",
					type=str,
					default='mfcc_average',
					help="Choose the type of formant fitness function")

parser.add_argument("-id", "--identifier", 
					type=str,
					default='2',
					help="used as random() seed")

parser.add_argument("-pl","--parallel", 
					type=bool,
					default=True,
					help="used to enable multiple praat processes")

parser.add_argument("-sl", "--selection",
                    type=str,
                    default='linear',
                    help="use to specify GA selection type. Choose from linear, proportional")

parser.add_argument("-cntk", "--cntk",
                    type=bool,
                    default=False,
                    help="write a csv file for use with the CNTK machine learning library")

args = parser.parse_args()

###################################################################################################
# Unpack the variables from argparse

soundfile = args.soundfile
populationsize = args.populationsize
generations = args.generations + 1
mutationrate = args.mutationrate
standarddev = args.standarddev
fitnesstype = args.fitnesstype
NO_FORMANTS = args.noformants
formantrepresentation = args.formantrepresentation
metric = args.distancemetric
loudnessmeasure = args.loudnessmeasure
fffilterbank = args.fffilterbank
identifier = args.identifier
parallel = args.parallel
SELECTION = args.selection
CNTK = args.cntk

###################################################################################################
# Set the time to measure the length of a run
start_time = time.time()

# If True, the identifier variable is used as a seed for random number generation
if False:
    random.seed(int(identifier))

# Initialises the generation index as 0
CURRENT_GEN = 0

# Creates the directory string
prefix = "{} Gen {} Pop {} Mut {} Sd {} ".format(soundfile,
                                                 generations-1,
                                                 populationsize,
                                                 mutationrate,
                                                 standarddev)


if fitnesstype == 'formant':
    directory = prefix + "{} {} {} {}".format(formantrepresentation, metric, loudnessmeasure, identifier)
elif fitnesstype == 'filterbank':
    directory = prefix + "{} {}".format(fffilterbank, identifier)

print(directory)

# Makes the directory for all subsequent files
os.mkdir(directory)

soundfile = 'Vowels\{}'.format(soundfile)

# Call the "praatcontrol" module to get target sound features
target_length = praatcontrol.get_time(soundfile)
target_sample_rate = praatcontrol.get_sample_rate(soundfile)
target_formants = praatcontrol.get_target_formants(target_length, soundfile, NO_FORMANTS)
target_intensity = praatcontrol.get_target_intensity(soundfile)
target_rms = praatcontrol.get_target_RMS(soundfile)

target_mfcc_average = praatcontrol.get_target_mfcc_average(soundfile)
target_logfbank_average = praatcontrol.get_target_logfbank_average(soundfile)
target_mfcc = praatcontrol.get_target_mfcc(soundfile)
target_logfbank = praatcontrol.get_target_logfbank(soundfile)


# Sets the length of individuals to equal the target. Can be overwrriten with a string
length = target_length  # "0.5"

###################################################################################################
###################################################################################################

class Individual:
    def __init__(self, name):

        self.name = name

        # List containing the real valued genotype
        self.values = []

        # Full list of muscle parameters for Praat
        self.full = ['Interarytenoid',
                     'Cricothyroid',
                     'Vocalis',
                     'Thyroarytenoid',
                     'PosteriorCricoarytenoid',
                     'LateralCricoarytenoid',
                     'Stylohyoid',
                     'Sternohyoid',
                     'Thyropharyngeus',
                     'LowerConstrictor',
                     'MiddleConstrictor',
                     'UpperConstrictor',
                     'Sphincter',
                     'Hyoglossus',
                     'Styloglossus',
                     'Genioglossus',
                     'UpperTongue',
                     'LowerTongue',
                     'TransverseTongue',
                     'VerticalTongue',
                     'Risorius',
                     'OrbicularisOris',
                     'TensorPalatini',
                     'Masseter',
                     'Mylohyoid',
                     'LateralPterygoid',
                     'Buccinator']

        # Constrained list of muscle parameters for Praat
        self.constrained = ['Hyoglossus',
                            'Styloglossus',
                            'Genioglossus',
                            'UpperTongue',
                            'LowerTongue',
                            'TransverseTongue',
                            'VerticalTongue',
                            'Risorius',
                            'OrbicularisOris',
                            'TensorPalatini',
                            'Masseter',
                            'Mylohyoid',
                            'LateralPterygoid',
                            'Buccinator']

        # Choose which parameters set to use
        self.parameters = self.constrained

        # Initialise the fitness score variables
        self.fitness = 0
        self.fitnessscaled = 0

        # Initialise the genotype with random values for the first generation
        if CURRENT_GEN == 0:
            self.values = [round(random.uniform(0, 1), 1) for x in range(len(self.parameters))]

    # Method for creating the Praat .artword file
    def create_artword(self):

        self.artword = open("{}/Generation{!s}/Individual{!s}.praat".format(directory, CURRENT_GEN, self.name), "w")

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

    # Method 
    def universal(self):
        
        # Assigns True or False to self.voiced, based on whether praat can calculate pitch 
        self.voiced = praatcontrol.get_individual_pitch(self.name, directory, CURRENT_GEN)
        
        # If a pitch is detected the formants are calculated and assigned to self.formants
        if self.voiced == True:
            self.formants = praatcontrol.get_individual_formants(self.name, directory, CURRENT_GEN, target_sample_rate)
        else:
            self.formants = [target_sample_rate/2 for x in range(5)]
        
        # 
        self.formants = self.formants[0:NO_FORMANTS]

        # This acts as a baseline fitness attribute to compare different fitness functions
        self.absolutefitness = fitnessfunction.fitness_a1(self.formants, target_formants, "SAD")
        
        print("absolute fitness", self.absolutefitness)
    
    # Method for calculating an individuals fitness
    def evaluate_formant(self):
        
        self.universal()
        print(self.voiced)
        print(self.formants)
        print(target_formants)
       
       # Calls the relevant fitness function based on cmd line argument
        if formantrepresentation == "hz":
            self.fitness = fitnessfunction.fitness_a1(self.formants, target_formants, metric)
        elif formantrepresentation == "mel":
            self.fitness = fitnessfunction.fitness_a2(self.formants, target_formants, metric)
        elif formantrepresentation == "cent":
            self.fitness = fitnessfunction.fitness_a3(self.formants, target_formants, metric)
        elif formantrepresentation == "bark":
            self.fitness = fitnessfunction.fitness_a4(self.formants, target_formants, metric)
        elif formantrepresentation == "erb":
            self.fitness = fitnessfunction.fitness_a5(self.formants, target_formants, metric)
        elif formantrepresentation == "brito":
            self.fitness = fitnessfunction.fitness_brito(self.formants, target_formants)
        
        # Apply a penalty of the sound is not voiced
        if self.voiced == False:
            self.fitness = self.fitness * 10

        # Extract loudness features
        self.intensity = praatcontrol.get_individual_intensity(self.name, directory, CURRENT_GEN, target_intensity)
        self.rms = praatcontrol.get_individual_RMS(self.name, directory, CURRENT_GEN, target_rms)

        # Apply loudness co-efficents
        if loudnessmeasure == "rms":
            self.fitness = self.fitness * self.rms
        elif loudnessmeasure == "intensity":
            self.fitness = self.fitness * self.intensity
        elif loudnessmeasure == "both":
            self.fitness = self.fitness * ((self.rms + self.intensity) / 2.0)
        elif loudnessmeasure == "none":
            pass

        ###########################################################################################
        # Write feature information to a csv file
        
        stats.write_formants(self.name,
                             directory,
                             CURRENT_GEN,
                             self.formants,
                             self.fitness,
                             self.voiced,
                             self.absolutefitness)
        ###########################################################################################
        # Call the write_formants_cntk method if a sound is voiced

        if self.voiced and CNTK:
            self.write_formants_cntk()

    
    def evaluate_filterbank(self):
        # MFCC and filterbank based fitness functions
        
        self.universal()

        if fffilterbank == "mfcc_average":
            self.mfcc_average = praatcontrol.get_individual_mfcc_average(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_mfcc_average(target_mfcc_average, self.mfcc_average, metric)

        elif fffilterbank == "logfbank_average":
            self.logfbank_average = praatcontrol.get_individual_logfbank_average(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_logfbank_average(target_logfbank_average, self.logfbank_average, metric)

        elif fffilterbank == "mfcc_sad":
            self.mfcc = praatcontrol.get_individual_mfcc(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_twodim_sad(target_mfcc, self.mfcc)

        elif fffilterbank == "mfcc_ssd":
            self.mfcc = praatcontrol.get_individual_mfcc(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_twodim_ssd(target_mfcc, self.mfcc)

        elif fffilterbank == "logfbank_sad":
            self.logfbank = praatcontrol.get_individual_logfbank(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_twodim_sad(target_logfbank, self.logfbank)

        elif fffilterbank == "logfbank_ssd":
            self.logfbank = praatcontrol.get_individual_logfbank(self.name, directory, CURRENT_GEN)
            self.fitness = fitnessfunction.fitness_twodim_ssd(target_logfbank, self.logfbank)
        
        stats.write_formants(self.name,
                             directory,
                             CURRENT_GEN,
                             self.formants,
                             self.fitness,
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
        
        self.mfcc_average = praatcontrol.get_individual_mfcc_average(self.name, directory, CURRENT_GEN)

        with open('cntk_mfcc_data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(x) for x in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(x) for x in self.mfcc_average)))
        

###################################################################################################
###################################################################################################

# Creates a list of strings for use as keys in a dictionary
keys = [str(x) for x in range(populationsize)]

# Create an empty dictionary for storing Individual instances
population = {}

# Lists to hold fitness stats
averagefitness = []
minimumfitness = []
AVERAGE_VOICED = []

# Main loop for Genetic Algorithm logic
for i in range(generations):

    # Creates a folder for the current generation
    os.mkdir(directory + "/Generation{!s}".format(CURRENT_GEN))

    # If it is the first generation, instantiate the Indiviudal class and associate it with
    # a key in the population dictionary
    if CURRENT_GEN == 0:
        for name in keys:
            population[name] = Individual(name)

    # Call the artword method for object in the population dictionary
    for name in keys:
        population[name].create_artword()

    # Synthesise artwords and run a single or multiple instances of Praat
    if parallel == True:
        praatcontrol.synthesise_artwords_threadpool(directory, CURRENT_GEN, populationsize)
    elif parallel == False:
        praatcontrol.synthesise_artwords_serial(CURRENT_GEN, populationsize, directory)

    # Calculate fitness scores by calling the evaluate_formants method
    for name in keys:
        if fitnesstype == "formant":
            population[name].evaluate_formant()
        elif fitnesstype == "filterbank":
            population[name].evaluate_filterbank()

    ###############################################################################################

    listfitness = []

    for name in keys:
        listfitness.append(population[name].fitness)

    numbered_list = list(enumerate(listfitness))

    averagefitness.append(sum(listfitness) / len(listfitness))
    minimumfitness.append(min(listfitness))

    # save the n number of best individuals
    a, b = list(zip(*sorted((numbered_list), key=lambda student: student[1])[:5]))

    elite = []

    print("\n")
    print("elitism")
    for i in range(len(a)):
        elite.append(population[str(a[i])].values)
        print(i, elite[i])

    print("\n")

    for i in keys:
        print(i, population[i].values)

    ###############################################################################################
    # Total the number of voiced sounds in a generation
    VOICED_TOTAL = 0.0

    for name in keys:
        if population[name].voiced:
            VOICED_TOTAL += 1

    VOICED_PERCENTAGE = VOICED_TOTAL / populationsize
    AVERAGE_VOICED.append(VOICED_PERCENTAGE)

    ###############################################################################################
    # Choose GA selection behaviour

    if SELECTION == "linear":
        genop.lin_rank(population, keys)
    elif SELECTION == "proportional":
        genop.fitness_proportional(population, keys)
    elif SELECTION == "hybrid":
        if VOICED_PERCENTAGE < 0.5:
            genop.fitness_proportional(population, keys)
        else:
            genop.lin_rank(population, keys)

    # The mutation function
    genop.mutation(population, keys, mutationrate, standarddev)

    # Activate elitism 
    ELITISM = False

    if ELITISM == True:
        for i in range(len(a)):
            print(elite[i])

            print(i, population[str(a[i])].values)
            population[str(a[i])].values = elite[i]
            print(i, population[str(a[i])].values)
    
    ###############################################################################################
    # Finish loop by incrementing the generation counter by 1
    CURRENT_GEN += 1

###################################################################################################
###################################################################################################
# Statisticss stuff

def statistics():
    """ Function for plotting performance graphs and saving run data"""
    with open("{}/Mean.txt".format(directory), "w") as mean:
        for item in averagefitness:
            mean.write("{!s}\r\n".format(item))

    with open("{}/Minimum.txt".format(directory), "w") as minimum:
        for item in minimumfitness:
            minimum.write('{!s}\r\n'.format(item))
statistics()

def performance_graph():
    plt.plot(averagefitness, 'k', label='Mean Fitness')
    plt.plot(minimumfitness, 'k--', label='Minimum Fitness')
    plt.axis([0, generations - 1, 0, max(averagefitness)])
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig("{}/Performance Graph".format(directory))
performance_graph()


def csv_file():
    with open('{}/Stats.csv'.format(directory), 'w', newline='') as csvfile:
        for i in range(len(averagefitness)):
            csvdata = (averagefitness[i], minimumfitness[i])
            spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(csvdata)
csv_file()

def runtime():
    with open("{}/{}Runtime.txt".format(directory, directory), "w") as run:
        run.write("--- %d seconds ---" % (time.time() - start_time))
runtime()

time.sleep(2)

###################################################################################################
###################################################################################################
