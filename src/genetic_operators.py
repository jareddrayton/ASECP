import math
import random
import shutil
from operator import itemgetter


def elitism(population, keys, elite_size):
    """
    Elitism function that returns a list of values to carry over to the next generation.

    Parameters
    ----------
    population : dict
        A dictionary containing references to the Individuals of a population
    keys : list
        List of the key values for population
    elite_size : int
        Number of individuals to carry over to next generation.

    Returns
    -------
    values : list
        List of elite values to carry over
    """
    values = []

    # Create a list of tuple pairs containing key and fitness scores of each individual
    keys_fitness = [(name, population[name].raw_fitness) for name in keys]

    # Sort the list of tuples by the second tuple item fitness. Reverse=True means the higher fitness are first
    keys_fitness = sorted(keys_fitness, key=itemgetter(1))

    # Unpack the list of tuples into seperate tuples
    ranked, fitness = zip(*keys_fitness)
    #print(keys_fitness)

    for i in range(elite_size):
        values.append(population[ranked[i]].values)
    
    return values


#################################################################################################################


def linear_ranking(population, keys):
    """ Linear probability distribution """

    # Create a list of tuple pairs containing key and fitness scores of each individual
    keys_fitness = [(name, population[name].raw_fitness) for name in keys]

    # Sort the list of tuples by the second tuple item fitness. Reverse=True means the higher fitness are first
    keys_fitness = sorted(keys_fitness, key=itemgetter(1), reverse=True)

    # Unpack the list of tuples into seperate tuples
    ranked, fitness = zip(*keys_fitness)
  
    C = len(population) # Set the constant term to equal to the population size

    SP = 2.0  # Set the selection pressure. This can be in the range 1.0 < x <= 2.0

    for i, rank in enumerate(ranked):
        population[rank].selection_probability = (2 - SP) / C + (2.0 * i * (SP - 1)) / (C * (C - 1))

    #print(sum([population[name].selection_probability for name in keys]))


def exponential_ranking(population, keys):
    """ Exponential probability distribution """

    # Create a list of tuple pairs containing key and fitness scores of each individual
    keys_fitness = [(name, population[name].raw_fitness) for name in keys]

    # Sort the list of tuples by the second tuple item fitness. Reverse=True means the higher fitness are first
    keys_fitness = sorted(keys_fitness, key=itemgetter(1), reverse=True)
    #print(keys_fitness)

    # Unpack the list of tuples into seperate tuples
    ranked, fitness = zip(*keys_fitness)
  
    C = len(population) # Set the constant term to equal to the population size

    NF = C * (2 * C - 1) / (6 * (C - 1))  # Set the normalisation factor.

    for i, rank in enumerate(ranked):
        population[rank].selection_probability = ((i ** 2)/(C - 1)**2)  / NF
        #print(population[rank].selection_probability, population[rank].raw_fitness)
    #print()


    #print(sum([population[name].selection_probability for name in keys]))


def fitness_proportional(population, keys):
    """ Fitness proportional selection """

    scaled_fitness = []

    for name in keys:
        population[name].scaled_fitness = round(1.0 / (population[name].raw_fitness), 10)
        scaled_fitness.append(population[name].raw_fitness)

    for name in keys:
        population[name].selection_probability = population[name].scaled_fitness / sum(scaled_fitness)
    
    #print(sum([population[name].selection_probability for name in keys]))


#################################################################################################################


def roulette_wheel_sampling(population, keys):

    N = len(keys) * 2

    mating_pool = []

    for i in range(N):
        roulette_spin = random.uniform(0, 1)
        currentcumulative = 0
        
        for name in keys:
            currentcumulative += population[name].selection_probability
            if currentcumulative > roulette_spin:
                mating_pool.append(name)
                break
            
    return mating_pool


def stochastic_universal_sampling(population, keys):

    N = len(keys) * 2

    mating_pool = []

    r = random.uniform(0, 1/N) # pick a number from 0, 1/N

    multi_arm_bandit = [r+i/N for i in range(N)]

    for arm in multi_arm_bandit:
        cumulative_probability = 0
        
        for name in keys:    
            cumulative_probability += population[name].selection_probability
            
            if cumulative_probability >= arm:
                mating_pool.append(name)
                break
            
    return mating_pool


def tournament_sampling(population, keys):

    # Set the tournament size and essentially the selection pressure
    # Not used in conjubction  with 

    tourn_size = 3

    N = len(keys) * 2 

    mating_pool = []
    
    for i in range(N):
        # Select the individuals used in this tournament
        selection = random.sample(keys, tourn_size)

        keys_fitness = [(name, population[name].raw_fitness) for name in selection]

        # Sort the list of tuples by the second tuple item fitness. Reverse=True means the higher fitness are first
        keys_fitness = sorted(keys_fitness, key=itemgetter(1), reverse=False)

        # Unpack the list of tuples into seperate tuples
        ranked, fitness = zip(*keys_fitness)
        
        mating_pool.append(ranked[0])

    return mating_pool


#################################################################################################################


def one_point_crossover(population, keys):
    """ One Point Crossover """
    
    # Call a sampling function that returns a pool of parents double the size of the population
    mating_pool = stochastic_universal_sampling(population, keys) 
    #mating_pool = roulette_wheel_sampling(population, keys)
    #mating_pool = tournament_sampling(population, keys)

    # Shuffle the mating pool
    random.shuffle(mating_pool)
    
    # split the mating pool into even length mother and father lists
    mothers = [mating_pool[x] for x in range(0, len(mating_pool), 2)]
    fathers = [mating_pool[x] for x in range(1, len(mating_pool), 2)]

    # create an empty list to hold the child values
    hold = []

    for i, name in enumerate(keys):
        crossover_point = random.randint(0, len(population[keys[i]].values))        
        hold.append(population[mothers[i]].values[0:crossover_point] + population[fathers[i]].values[crossover_point:])

    # overwrite the parents with the new child values
    for i, name in enumerate(keys):
        population[name].values = hold[i]


def uniform_crossover(population, keys):
    """ Uniform Crossover 
    
    Parameters
    ----------
    population : dictionary
        A dictionary containing the collection of Individual objects
    keys : list
        A list of keys for the population dictionary

    """
    
    # Call a sampling function that returns a pool of parents double the size of the population
    mating_pool = stochastic_universal_sampling(population, keys) 
    #mating_pool = roulette_wheel_sampling(population, keys)
    #mating_pool = tournament_sampling(population, keys)
    
    # Shuffle the mating pool
    random.shuffle(mating_pool)
    
    # split the mating pool into even length mother and father lists
    mothers = [mating_pool[x] for x in range(0, len(mating_pool), 2)]
    fathers = [mating_pool[x] for x in range(1, len(mating_pool), 2)]

    hold = []

    for i, name in enumerate(keys):
        
        tt = [random.randint(0, 1) for x in range(len(population[keys[i]].values))]
        hold.append([population[mothers[i]].values[j] if tt[j] == True 
                    else population[fathers[i]].values[j] 
                    for j in range(len(tt))])

    for i, name in enumerate(keys):
        population[name].values = hold[i]


#################################################################################################################


def gaussian_mutation(population, keys, mutation_rate, mutation_standard_dev):

    for name in keys:
        for i in range(len(population[name].values)):
            lower_bound = population[name].parameters[i][1]
            upper_bound = population[name].parameters[i][2]
            # Proceed if mutation_rate is higher than a number taken from a uniform distrubtion
            if mutation_rate >= random.random():
                difference = abs(lower_bound - upper_bound)
                scale_factor = difference / 2
                # Mutate the current allele value
                population[name].values[i] = round(population[name].values[i] + random.gauss(0, mutation_standard_dev * scale_factor), 2)

                # Then truncate the vaule if it is now out of bounds
                if population[name].values[i] > upper_bound:
                    population[name].values[i] = upper_bound
                elif population[name].values[i] < lower_bound:
                    population[name].values[i] = lower_bound


def uniform_mutation(population, keys, mutation_rate):

    for name in keys:
        for i in range(len(population[name].values)):
            lower_bound = population[name].parameters[i][1]
            upper_bound = population[name].parameters[i][2]
            
            # Proceed if mutation_rate is higher than a number taken from a uniform distrubtion
            if mutation_rate >= random.random():

                population[name].values[i] = round(random.uniform(lower_bound, upper_bound), 2)
