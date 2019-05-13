import random
import math
from operator import itemgetter

#################################################################################################################
# Functions for assigning selection probabilities

def fitness_proportional(population, keys):
    """ Fitness proportional selection """

    # duplicate the population dictionary
    temppopulation = population

    scaledfitness = []

    for name in keys:
        population[name].fitnessscaled = round(1.0 / population[name].fitness, 10)
        scaledfitness.append(population[name].fitnessscaled)

    for name in keys:
        population[name].fitnessscaled = population[name].fitnessscaled / sum(scaledfitness)

    one_point_crossover(population, keys, temppopulation)


def linear_ranking(population, keys):
    """ Linear probability distribution """

    # duplicate the population dictionary
    temppopulation = population

    # make the constant equal to the population size
    c = len(population)

    # Set he selection pressure. This can be in the range 1.0 < x <= 2.0
    s = 2.0  

    # create an empty list to hold 
    fitness = []

    # duplicate the keys list os strings
    index = keys

    # for every name in keys, check the indiviudals fitness and add to fitness list
    for name in keys:
        fitness.append(population[name].fitness)


    zippedlists = zip(index, fitness)
    sortedlist = sorted(zippedlists, key=itemgetter(1))
    x, y = zip(*sortedlist)
    ranked = list(x)
    ranked.reverse()
    print("ranking")
    print(ranked)

    probabilities = []

    for i in range(len(ranked)):
        population[ranked[i]].fitnessscaled = (2 - s) / c + (2.0 * i * (s - 1)) / (c * (c - 1))
        print(ranked[i], population[ranked[i]].fitnessscaled)
        probabilities.append(population[ranked[i]].fitnessscaled)

    print("Sum of probabilities", sum(probabilities))

    # uniform_crossover(population, keys, temppopulation)
    one_point_crossover(population, keys, temppopulation)


def exponential_ranking(population, keys):
    """Exponential ranking"""

    # duplicate the population dictionary
    temppopulation = population

    # make the constant equal to the population size
    c = len(population)

    # Set he selection pressure. This can be in the range 1.0 < x <= 2.0
    sp = 0.95  

    # create an empty list to hold 
    fitness = []

    # duplicate the keys list os strings
    index = keys

    # for every name in keys, check the indiviudals fitness and add to fitness list
    for name in keys:
        fitness.append(population[name].fitness)

    
    zippedlists = zip(index, fitness)
    sortedlist = sorted(zippedlists, key=itemgetter(1))
    x, y = zip(*sortedlist)
    ranked = list(x)
    ranked.reverse()
    print("ranking")
    print(ranked)

    probabilities = []

    for i in range(1, len(ranked)+1):
        population[ranked[i-1]].fitnessscaled = ((sp - 1) / ((sp ** c) - 1)) * (sp ** (c - i))
        print(len(ranked))
        print(ranked[i-1], population[ranked[i-1]].fitnessscaled, i)
        probabilities.append(population[ranked[i-1]].fitnessscaled)

    print("Sum of probabilities", sum(probabilities))

    one_point_crossover(population, keys, temppopulation)


#################################################################################################################

def roulette_spin(population, keys):
    """ Returns one"""
    roulette_spin = random.uniform(0, 1)
    currentcumulative = 0

    for name in keys:
        currentcumulative += population[name].fitnessscaled
        if currentcumulative > roulette_spin:
            return name

def stochastic_universal_sampling():
    pass

#################################################################################################################

def one_point_crossover(population, keys, temppopulation):
    """ One Point Crossover """

    for name in keys:
        parent_a = roulette_spin(population, keys)
        parent_b = roulette_spin(population, keys)

        limit = len(population[parent_a].values)

        cross_point = random.randint(0, limit)

        temppopulation[name].values = population[parent_a].values[0:cross_point] + population[parent_b].values[cross_point:limit]

        population[name].values = temppopulation[name].values


def uniform_crossover(population, keys, temppopulation):
    """ Uniform Crossover Operator """

    for name in keys:
        parent_a = roulette_spin(population, keys)
        parent_b = roulette_spin(population, keys)

        print("Parent A", population[parent_a].values)
        print("Parent B", population[parent_b].values)
        
        for i in range(len(temppopulation[name].values)):
            if random.random() <= 0.5:
                temppopulation[name].values[i] = population[parent_a].values[i]
            else:
                temppopulation[name].values[i] = population[parent_b].values[i]
        
        print("Child", temppopulation[name].values)

        population[name].values = temppopulation[name].values


#################################################################################################################

def mutation(population, keys, mutationprobability, standarddeviation):
    """ Mutation function A value is taken from a gaussian distribution and added to an alelle value."""

    for name in keys:
        for i in range(len(population[name].values)):

            mutationthresh = random.random()
            perturb = random.gauss(0, standarddeviation)

            if mutationprobability >= mutationthresh:
                round(population[name].values[i] + perturb, 2)
                
                if population[name].values[i] > 1.0:
                    population[name].values[i] = 1.0
                elif population[name].values[i] < -1.0:
                    population[name].values[i] = -1.0