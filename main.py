import os
import random
import time
import matplotlib.pyplot as plt

from sys import argv

import fitnessfunction
import genop
import praatcontrol
import stats

# Key Word Arguments HERE

script, soundfile, generations, generationsize, mutationprobability, standarddeviation, parallel, ff, metric, lm, identifier = argv

# Convert arguments from strings to integers and floats 

generations = int(generations) + 1
generationsize = int(generationsize)
mutationprobability = float(mutationprobability)
standarddeviation = float(standarddeviation)

#################################################################################################################
#################################################################################################################

start_time = time.time()

random.seed(int(identifier))

currentgeneration = 0

directory = "%s Gen %d Pop %d Mut %g SD %g %s %s %s %s" % (soundfile,
                                                        generations - 1,
                                                        generationsize,
                                                        mutationprobability,
                                                        standarddeviation,
                                                        ff,
                                                        metric,
                                                        lm,
                                                        identifier)

os.mkdir(directory)

targetlength = praatcontrol.get_time(soundfile)
targetformants = praatcontrol.get_target_formants(targetlength, soundfile)
targetintensity = praatcontrol.get_target_intensity(soundfile)
targetrms = praatcontrol.get_target_RMS(soundfile)

length = "0.5"


#################################################################################################################
#################################################################################################################

class Individual:
    def __init__(self, name):

        self.name = name

        self.values = []

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

        self.fitness = 0
        self.fitnessscaled = 0

        if currentgeneration == 0:
            self.initialise_values()

    def initialise_values(self):
        """ Method for Initialising candidates with random values """

        self.values = [round(random.uniform(0, 1), 1) for x in range(len(self.parameters))]

        return self.values

    def create_artword(self):

        self.artword = open("{}/Generation{!s}/Individual{!s}.praat".format(directory, currentgeneration, self.name),
                            "w")

        self.artword.write('Create Speaker... Robovox Male 2\r\n')
        self.artword.write('Create Artword... Individual' + self.name + ' ' + length + '\r\n')
        self.artword.write('Set target... 0.0  0.07  Lungs\r\n')
        self.artword.write('Set target... 0.04  0.0  Lungs\r\n')
        self.artword.write('Set target... %s   0.0  Lungs\r\n' % length)
        self.artword.write('Set target... 0.00 1 LevatorPalatini\r\n')
        self.artword.write('Set target... ' + length + ' 1 LevatorPalatini\r\n')

        for i in range(len(self.parameters)):
            self.artword.seek(0, 2)
            self.artword.write('Set target... 0.0 ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')
            self.artword.write(
                'Set target... ' + length + ' ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')

        self.artword.write('select Artword Individual' + self.name + '\r\n')
        self.artword.write('plus Speaker Robovox\r\n')
        self.artword.write('To Sound... 22500 25    0 0 0    0 0 0   0 0 0\r\n')
        self.artword.write('''nowarn do ("Save as WAV file...", "Individual''' + self.name + '''.wav")\r\n''')
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

    def evaluate_fitness(self):

        # maybe this method should pull

        self.formants, self.voiced = praatcontrol.get_individual_frequencies(self.name, directory, currentgeneration)
        self.intensity = praatcontrol.get_individual_intensity(self.name, directory, currentgeneration, targetintensity)
        self.rms = praatcontrol.get_individual_RMS(self.name, directory, currentgeneration, targetrms)

        print(self.formants)

        if ff == "hz":
            self.fitness = fitnessfunction.fitness_a1(self.formants, targetformants, metric)
        elif ff == "mel":
            self.fitness = fitnessfunction.fitness_a2(self.formants, targetformants, metric)
        elif ff == "cent":
            self.fitness = fitnessfunction.fitness_a3(self.formants, targetformants, metric)
        elif ff == "bark":
            self.fitness = fitnessfunction.fitness_a4(self.formants, targetformants, metric)
        elif ff == "erb":
            self.fitness = fitnessfunction.fitness_a5(self.formants, targetformants, metric)

        print(self.formants)

        if lm == "rms":
            self.fitness = self.fitness * self.rms
        elif lm == "intensity":
            self.fitness = self.fitness * self.intensity
        elif lm == "both":
            self.fitness = self.fitness * ((self.rms + self.intensity) / 2.0)

        print(self.formants)

        print("Individual ", self.name)
        print("Is Voiced?            :", self.voiced)
        print("Fitness Score         :", self.fitness)
        print("Intensity Coefficient :", self.intensity)
        print("Fitness * Intensity   :", self.fitness * self.intensity)
        print("RMS Coefficient       :", self.rms)
        print("Fitness * RMS         :", self.fitness * self.rms)

        if self.voiced:
            self.write_cntk()

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

keys = [str(x) for x in range(generationsize)]

population = {}

averagefitness = []
minimumfitness = []

for i in range(generations):

    # creates
    os.mkdir(directory + "/Generation%d" % currentgeneration)

    if currentgeneration == 0:
        for name in keys:
            population[name] = Individual(name)

    for name in keys:
        population[name].create_artword()

    if parallel == "P":
        praatcontrol.synthesise_artwords_parallel(currentgeneration, generationsize, directory)
    elif parallel == "S":
        praatcontrol.synthesise_artwords_serial(currentgeneration, generationsize, directory)

    for name in keys:
        population[name].evaluate_fitness()

    currentgeneration += 1

    listfitness = []

    for name in keys:
        listfitness.append(population[name].fitness)

    averagefitness.append(sum(listfitness) / len(listfitness))
    minimumfitness.append(min(listfitness))

    # total the number of voiced sounds in a generation
    voiced_total = 0

    for name in keys:
        if population[name].voiced:
            voiced_total += 1

    voiced_percentage = voiced_total / generationsize

    if voiced_percentage < 0.5:
        genop.fitness_proportional(population, keys)
        print("FPS")
    else:
        genop.lin_rank(population, keys)
        print("Linear")

    #genop.lin_rank(population, keys)
    #genop.fitness_proportional(population, keys)

    genop.mutation(population, keys, mutationprobability, standarddeviation)


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
