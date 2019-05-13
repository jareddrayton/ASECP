import random
import math
from operator import itemgetter

def linear_ranking(population, keys):
    """ Linear probability distribution """

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
        
        #print(rank[i], population[rank[i]].selection_probability, population[rank[i]].fitness)
    
    #print("Sum of Probs", sum([population[rank[i]].selection_probability for i in range(len(keys))]))

#################################################################################################################

def roulette_spin(population, keys):
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


#################################################################################################################

def mutation(population, keys, mutation_rate, mutation_standard_dev):

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