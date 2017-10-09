import os
import random
import time
import matplotlib.pyplot as plt

from sys import argv

import fitnessfunction
import genop
import praatcontrol
import stats

# Variables given at the cmd line, unpacked using argv
script, soundfile, generations, generationsize, mutationprobability, \
    standarddeviation, parallel, ff, metric, lm, identifier = argv

# Convert variable arguments from strings to integers and floats
generations = int(generations) + 1
generationsize = int(generationsize)
mutationprobability = float(mutationprobability)
standarddeviation = float(standarddeviation)

# Set the time to measure the length of a run
start_time = time.time()

# If True, the identifier variable is used as a seed for random number generation
if True:
    random.seed(int(identifier))

# Initialises the generation index as 0
currentgeneration = 0

# Creates the directory string
directory = "%s Gen %d Pop %d Mut %g SD %g %s %s %s %s" % (soundfile,
                                                           generations - 1,
                                                           generationsize,
                                                           mutationprobability,
                                                           standarddeviation,
                                                           ff,
                                                           metric,
                                                           lm,
                                                           identifier)

# Makes the directory for all subsequent files
os.mkdir(directory)

# Call the "praatcontrol" module to get target sound features
target_length = praatcontrol.get_time(soundfile)
target_formants = praatcontrol.get_target_formants(target_length, soundfile)
target_intensity = praatcontrol.get_target_intensity(soundfile)
target_rms = praatcontrol.get_target_RMS(soundfile)
target_fbank_average = praatcontrol.get_target_fbank_average(soundfile)
target_fbank = praatcontrol.get_target_fbank(soundfile)
target_mfcc_average = praatcontrol.get_target_mfcc_average(soundfile)

# Sets the length of individuals to equal the target. Can be overwrriten with a string
length = target_length  # "0.5"


#################################################################################################################
#################################################################################################################

class Individual:
    def __init__(self, name):

        self.name = name

        # List containing the real valued genotype
        self.values = []

        # List of the muscle parameters associated with the genotype
        self.parameters = ['Interarytenoid',
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

        # Initialise the fitness cores to one
        self.fitness = 0
        self.fitnessscaled = 0

        # Initialise the genotype with values for the first generation
        if currentgeneration == 0:
            self.values = [round(random.uniform(0, 1), 1) for x in range(len(self.parameters))]

    # Method for creating the Praat .artword file
    def create_artword(self):

        # Create the file
        self.artword = open("{}/Generation{!s}/Individual{!s}.praat".format(directory, currentgeneration, self.name),
                            "w")

        # Configure speaker type and sound length
        self.artword.write('Create Speaker... Robovox Male 2\r\n')
        self.artword.write('Create Artword... Individual' + self.name + ' ' + length + '\r\n')

        # Specify Lungs and LevatorPalatini parameter values
        self.artword.write('Set target... 0.0  0.07  Lungs\r\n')
        self.artword.write('Set target... 0.04  0.0  Lungs\r\n')
        self.artword.write('Set target... %s   0.0  Lungs\r\n' % length)
        self.artword.write('Set target... 0.00 1 LevatorPalatini\r\n')
        self.artword.write('Set target... ' + length + ' 1 LevatorPalatini\r\n')

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(self.parameters)):
            self.artword.seek(0, 2)
            self.artword.write('Set target... 0.0 ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')
            self.artword.write(
                'Set target... ' + length + ' ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')

        # Set sample rate and synthesise audio
        self.artword.write('select Artword Individual' + self.name + '\r\n')
        self.artword.write('plus Speaker Robovox\r\n')
        self.artword.write('To Sound... 22050 25    0 0 0    0 0 0   0 0 0\r\n')
        self.artword.write('''nowarn do ("Save as WAV file...", "Individual''' + self.name + '''.wav")\r\n''')

        # Extract formants, pitch, and intensity
        self.artword.write('''selectObject ("Sound Individual''' + self.name + '''_Robovox")\r\n''')
        self.artword.write('To Formant (burg): 0, 5, 5000, %s, 50\r\n' % length)
        self.artword.write('List: "no", "yes", 6, "no", 3, "no", 3, "no"\r\n')
        self.artword.write('''appendFile ("formants''' + self.name + '''.txt", info$ ())\r\n''')
        self.artword.write('''selectObject ("Sound Individual''' + self.name + '''_Robovox")\r\n''')
        self.artword.write('To Pitch: %s, 75, 600\r\n' % length)
        self.artword.write('Get mean: 0, 0, "Hertz"\r\n')
        self.artword.write('''appendFile ("pitch''' + self.name + '''.txt", info$ ())\r\n''')
        self.artword.write('''selectObject ("Sound Individual''' + self.name + '''_Robovox")\r\n''')
        self.artword.write('To Intensity: 100, 0, "yes"\r\n')
        self.artword.write('Get standard deviation: 0, 0\r\n')
        self.artword.write('''appendFile ("intensity''' + self.name + '''.txt", info$ ())\r\n''')

        self.artword.close()

    # Method for calculating an individuals fitness
    def evaluate_fitness(self):

        # Extract formant features
        self.formants, self.voiced = praatcontrol.get_individual_frequencies(self.name, directory, currentgeneration)

        # Extract loudness features
        self.intensity = praatcontrol.get_individual_intensity(self.name, directory, currentgeneration,
                                                               target_intensity)
        self.rms = praatcontrol.get_individual_RMS(self.name, directory, currentgeneration, target_rms)


        self.fbank_average = praatcontrol.get_individual_fbank_average(self.name, directory, currentgeneration)
        self.fbank = praatcontrol.get_individual_fbank(self.name, directory, currentgeneration)
        self.mfcc_average = praatcontrol.get_individual_mfcc_average(self.name, directory, currentgeneration)

        # Calls the relevant fitness function based on cmd line argument
        if ff == "hz":
            self.fitness = fitnessfunction.fitness_a1(self.formants, target_formants, metric)
        elif ff == "mel":
            self.fitness = fitnessfunction.fitness_a2(self.formants, target_formants, metric)
        elif ff == "cent":
            self.fitness = fitnessfunction.fitness_a3(self.formants, target_formants, metric)
        elif ff == "bark":
            self.fitness = fitnessfunction.fitness_a4(self.formants, target_formants, metric)
        elif ff == "erb":
            self.fitness = fitnessfunction.fitness_a5(self.formants, target_formants, metric)
        elif ff == "brito":
            self.fitness = fitnessfunction.fitness_brito(self.formants, target_formants)
        elif ff == "fbank_average":
            self.fitness = fitnessfunction.fitness_fbank_average(target_fbank_average, self.fbank_average, metric)
        elif ff == "fbank_sad":
            self.fitness = fitnessfunction.fitness_fbank_sad(target_fbank, self.fbank)
        elif ff == "fbank_ssd":
            self.fitness = fitnessfunction.fitness_fbank_ssd(target_fbank, self.fbank)
        elif ff == "mfcc_average":
            self.fitness = fitnessfunction.fitness_fbank_average(target_mfcc_average, self.mfcc_average, metric)

        # Apply a penalty of the sound is not voiced
        if self.voiced == False:
            self.fitness = self.fitness * 10

        # Create loudness co-efficents
        if lm == "rms":
            self.fitness = self.fitness * self.rms
        elif lm == "intensity":
            self.fitness = self.fitness * self.intensity
        elif lm == "both":
            self.fitness = self.fitness * ((self.rms + self.intensity) / 2.0)
        elif lm == "none":
            pass

        # Print
        print("Individual ", self.name)
        print("Is Voiced?            :", self.voiced)
        print("Fitness Score         :", self.fitness)
        print("Intensity Coefficient :", self.intensity)
        print("Fitness * Intensity   :", self.fitness * self.intensity)
        print("RMS Coefficient       :", self.rms)
        print("Fitness * RMS         :", self.fitness * self.rms)

        # Call the write_cntk method if a sound is voiced
        if self.voiced:
            self.write_cntk()

        # Write feature information to a csv file
        stats.write_formants(self.name,
                             directory,
                             currentgeneration,
                             self.formants,
                             self.fitness,
                             self.voiced)

    def write_cntk(self):
        """ This method adds writes features and labels to a file for use with CNTK
        The format is as below.
        |labels 0 0 0 0 0 0 0 1 0 0 |features 0 0 0 0 0 0 0 0 0 0 0

        :return:
        """

        #
        with open('data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(elm) for elm in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(elm) for elm in self.formants)))


#################################################################################################################
#################################################################################################################

# Creates a list of strings for use as keys in a dictionary
keys = [str(x) for x in range(generationsize)]

# Create an empty dictionary for storing Individual instances
population = {}

# Lists to hold fitness stats
averagefitness = []
minimumfitness = []

# Main loop for Genetic Algorithm logic
for i in range(generations):

    # Creates a folder for the current generation
    os.mkdir(directory + "/Generation%d" % currentgeneration)

    # If it is the first generation, instantiate the Indiviudal class and associate it with
    # a key in the population dictionary
    if currentgeneration == 0:
        for name in keys:
            population[name] = Individual(name)

    # Call the artword method for object in the population dictionary
    for name in keys:
        population[name].create_artword()

    # Synthesise artwords and run a single or multiple instances of Praat
    if parallel == "P":
        praatcontrol.synthesise_artwords_parallel(currentgeneration, generationsize, directory)
    elif parallel == "S":
        praatcontrol.synthesise_artwords_serial(currentgeneration, generationsize, directory)

    # Calculate fitness scores by calling the evaluate_fitness method
    for name in keys:
        population[name].evaluate_fitness()

    # Increment the generation index
    currentgeneration += 1

    ######################################################################################################
    ######################################################################################################

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

    for i in range(len(a)):
        elite.append(population[str(a[i])].values)
        print(i, elite[i])

    print("\n")

    for i in keys:
        print(i, population[i].values)

    # print(elite)
    # print(population)

    ######################################################################################################
    ######################################################################################################

    # total the number of voiced sounds in a generation
    voiced_total = 0

    for name in keys:
        if population[name].voiced:
            voiced_total += 1

    voiced_percentage = voiced_total / generationsize

    # GA behaviour

    if voiced_percentage < 0.5:
        genop.fitness_proportional(population, keys)
        # print("FPS")
    else:
        genop.lin_rank(population, keys)
        # print("Linear")

    # genop.lin_rank(population, keys)
    # genop.fitness_proportional(population, keys)

    genop.mutation(population, keys, mutationprobability, standarddeviation)

    elitism = True

    print("\n")

    if elitism == True:
        for i in range(len(a)):
            print(elite[i])

            print(i, population[str(a[i])].values)

            population[str(a[i])].values = elite[i]

            print(i, population[str(a[i])].values)

    print("\n")

    for i in keys:
        print(i, population[i].values)


#################################################################################################################
#################################################################################################################

def statistics():
    """ Function for plotting performance graphs and saving run data"""

    with open("{}/Mean.txt".format(directory), "w") as mean:
        for item in averagefitness:
            mean.write("{!s}\r\n".format(item))

    with open("{}/Minimum.txt".format(directory), "w") as minimum:
        for item in minimumfitness:
            minimum.write('{!s}\r\n'.format(item))

    plt.plot(averagefitness, 'k', label='Mean Fitness')
    plt.plot(minimumfitness, 'k--', label='Minimum Fitness')
    plt.axis([0, generations - 1, 0, max(averagefitness)])
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig("{}/Performance Graph".format(directory))


statistics()

with open("{}/{}Runtime.txt".format(directory, directory), "w") as run:
    run.write("--- %d seconds ---" % (time.time() - start_time))

time.sleep(2)

#################################################################################################################
#################################################################################################################
