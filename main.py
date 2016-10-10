import os, random, time, math
from operator import itemgetter 
from sys import argv

import matplotlib.pyplot as plt

import praatcontrol, fitnessfunction, genop, stats


# Key Word Arguments HERE

script, soundfile, generations, generationsize, mutationprobability, standarddeviation, parallel, ff, metric, identifier = argv 

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

directory = "%s Gen %d Pop %d Mut %g SD %g %s %s %s" % (soundfile, generations-1,
generationsize, mutationprobability, standarddeviation, ff, metric, identifier)

os.mkdir(directory)

targetlength = praatcontrol.get_time(soundfile)
targetfrequencies = praatcontrol.get_target_frequencies(targetlength, soundfile)
targetintensity = praatcontrol.get_target_intensity(soundfile)
targetrms = praatcontrol.get_target_RMS(soundfile)

length = "0.5"

#################################################################################################################
#################################################################################################################

class Individual:

    def __init__(self, name):
        
        self.name = name
        
        self.values = []
        
        self.parameters = ['Interarytenoid','Cricothyroid', 'Vocalis', 'Thyroarytenoid', 
        'PosteriorCricoarytenoid', 'LateralCricoarytenoid', 'Stylohyoid', 'Sternohyoid',
        'Thyropharyngeus', 'LowerConstrictor', 'MiddleConstrictor', 'UpperConstrictor',
        'Sphincter', 'Hyoglossus', 'Styloglossus', 'Genioglossus', 'UpperTongue',
        'LowerTongue', 'TransverseTongue', 'VerticalTongue', 'Risorius', 'OrbicularisOris',
        'TensorPalatini', 'Masseter', 'Mylohyoid', 'LateralPterygoid', 'Buccinator']

        
        """
        self.parameters = ['Interarytenoid','Cricothyroid', 'Vocalis', 
        'Thyroarytenoid', 'LateralCricoarytenoid', 'Stylohyoid', 'Sternohyoid',
        'Hyoglossus', 'Styloglossus', 'Genioglossus', 'UpperTongue',
        'LowerTongue', 'VerticalTongue', 'Risorius', 'OrbicularisOris',
        'Masseter', 'Mylohyoid', 'Buccinator']
        """
        
        """
        self.parameters = ['Interarytenoid','Cricothyroid', 'Hyoglossus', 'Styloglossus', 
        'Genioglossus', 'OrbicularisOris', 'LowerTongue', 'LevatorPalatini', 'Masseter', 
        'Mylohyoid']
        """

        self.fitness = 0
        self.fitnessscaled = 0
        
        if currentgeneration == 0:
            self.initialise_values()
            
    def initialise_values(self): 
        """ Method for Initialising candidates with random values """

        self.values = [round(random.uniform(-1, 1), 1) for x in range(len(self.parameters))]
    
        return self.values

    def create_artword(self):
    
        self.artword = open("%s\Generation%d\Individual%d.praat" % (directory, currentgeneration, int(self.name)), "wb")        
        
        self.artword.write('Create Speaker... Robovox Male 2\r\n')
        self.artword.write('Create Artword... Individual'+ self.name + ' ' + length + '\r\n')
        self.artword.write('Set target... 0.0  0.07  Lungs\r\n')
        self.artword.write('Set target... 0.04  0.0  Lungs\r\n')
        self.artword.write('Set target... %s   0.0  Lungs\r\n' % length)
        self.artword.write('Set target... 0.00 1 LevatorPalatini\r\n')
        self.artword.write('Set target... ' + length + ' 1 LevatorPalatini\r\n')

        for i in range(len(self.parameters)):
            
            self.artword.seek(0, 2)
            self.artword.write('Set target... 0.0 ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')
            self.artword.write('Set target... ' + length + ' ' + str(self.values[i]) + ' ' + self.parameters[i] + '\r\n')
        
        self.artword.write('select Artword Individual'+ self.name + '\r\n')
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
        

        self.intensity = praatcontrol.get_individual_intensity(self.name, directory, currentgeneration,targetintensity)
        self.rms = praatcontrol.get_individual_RMS(self.name,directory,currentgeneration,targetrms)
        self.formants, self.voiced = praatcontrol.get_individual_frequencies(self.name,directory,currentgeneration)
        

        if ff == "A1":
            self.fitness = fitnessfunction.fitness_a1(self.formants, self.voiced, targetfrequencies, metric)
        elif ff == "A2":
            self.fitness = fitnessfunction.fitness_a2(self.formants, self.voiced, targetfrequencies, metric)
        elif ff == "A3":
            self.fitness = fitnessfunction.fitness_a3(self.formants, self.voiced, targetfrequencies, metric)

        print
        print "Individual ", self.name
        print "Voiced                :", self.voiced
        print "Fitness               :", self.fitness
        print "Intensity Coefficient :", self.intensity
        print "Fitness * Intensity   :", self.fitness * self.intensity
        print "RMS Coefficient       :", self.rms
        print "Fitness * RMS         :", self.fitness * self.rms
        print

        #self.fitness = self.fitness * self.rms
        self.fitness = self.fitness * self.intensity
        #self.fitness = self.fitness * ((self.rms + self.intensity) / 2.0)
        
        stats.write_formants(self.name, directory, currentgeneration, 
        	self.formants, self.fitness, self.voiced)

#################################################################################################################
#################################################################################################################

keys = [str(x) for x in range(generationsize)]

population = {}

averagefitness = []
minimumfitness = []

for i in range(generations):
    
    os.mkdir(directory + "\Generation%d" % currentgeneration)
    
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

    averagefitness.append(sum(listfitness)/len(listfitness))
    minimumfitness.append(min(listfitness))

    # genop.lin_rank(population, keys)
    
    genop.fitness_proportional(population, keys)        
    
    genop.mutation(population, keys,mutationprobability,standarddeviation)

#################################################################################################################
#################################################################################################################

def statistics():
    """ Function for plotting performance graphs and saving run data"""

    with open("%s\\Mean.txt" % directory, "wb") as mean:
        for item in averagefitness:
            mean.write("%s\r\n" % item)
    
    with open("%s\\Minimum.txt" % directory, "wb") as minimum:
        for item in minimumfitness:
            minimum.write("%s\r\n" % item)

    plt.plot(averagefitness, 'k', label = 'Mean Fitness')
    plt.plot(minimumfitness, 'k--', label = 'Minimum Fitness')
    plt.axis([0, generations - 1, 0, max(averagefitness)])
    plt.xlabel('Generations')
    plt.ylabel('Fitness')
    plt.legend()
    plt.savefig(directory + "\\Performance Graph")

statistics()

with open("%s\\%sRuntime.txt" % (directory, directory), "wb") as run:
    run.write("--- %d seconds ---" % (time.time() - start_time))
    run.close

time.sleep(2)

#################################################################################################################
#################################################################################################################