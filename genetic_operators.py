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

    # Create a list containing all the fitness scores of the population
    fitness = [population[name].fitness for name in keys]

    # Create a zip of keys fitness then sort them by fitness
    keys_fitness = zip(keys, fitness)
    keys_fitness = sorted(keys_fitness, key=itemgetter(1), reverse=True)

    # Unpack the zip
    rank, y = zip(*keys_fitness)
    rank = list(rank)
  
    C = len(population) # Set the constant term to equal to the population size

    SP = 2.0  # Set the selection pressure. This can be in the range 1.0 < x <= 2.0

    for i in range(len(rank)):
        population[rank[i]].selection_probability = (2 - SP) / C + (2.0 * i * (SP - 1)) / (C * (C - 1))


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
        currentcumulative += population[name].selection_probability
        if currentcumulative > roulette_spin:
            return name

def stochastic_universal_sampling():
    pass

#################################################################################################################

def one_point_crossover(population, keys):
    """ One Point Crossover """

    temppopulation = population

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

def mutation(population, keys, mutation_rate, mutation_standard_dev):
    """ Mutation function A value is taken from a gaussian distribution and added to an alelle value."""

    for name in keys:
        for i in range(len(population[name].values)):

            # Proceed if mutation_rate is higher than a number taken from a uniform distrubtion
            if mutation_rate >= random.random():
                
                # Mutate the current allele value
                population[name].values[i] += random.gauss(0, mutation_standard_dev)
                
                # Then truncate tha vaule if it is now out of bounds
                if population[name].values[i] > 1.0:
                    population[name].values[i] = 1.0
                elif population[name].values[i] < -1.0:
                    population[name].values[i] = -1.0