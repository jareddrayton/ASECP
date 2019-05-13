import random
import math
from operator import itemgetter

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
    print("Current Ranking", ranked)

    probabilities = []

    for i in range(len(ranked)):
        population[ranked[i]].fitnessscaled = (2 - s) / c + (2.0 * i * (s - 1)) / (c * (c - 1))
        #print(ranked[i], population[ranked[i]].fitnessscaled)
        probabilities.append(population[ranked[i]].fitnessscaled)

    print("Sum of probabilities", sum(probabilities))

    # uniform_crossover(population, keys, temppopulation)
    one_point_crossover(population, keys, temppopulation)


def roulette_spin(population, keys):
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


def mutation(population, keys, mutation_rate, mutation_standard_dev):
    """ Mutation function A value is taken from a gaussian distribution and added to an alelle value."""

    for name in keys:
        print("Before Mutation", population[name].values)

        for i in range(len(population[name].values)):

            mutation_threshold = random.random()
            perturbation = random.gauss(0, mutation_standard_dev)

            if mutation_rate >= mutation_threshold:
                population[name].values[i] += perturbation
                
                if population[name].values[i] > 1.0:
                    population[name].values[i] = 1.0
                elif population[name].values[i] < -1.0:
                    population[name].values[i] = -1.0

        print("After Mutation ", population[name].values)
