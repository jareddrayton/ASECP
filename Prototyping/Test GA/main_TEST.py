import random
from tqdm import tqdm

import genetic_operators_TEST

population_size = 100
generations = 100

mutation_rate = 0.05
mutation_standard_dev = 0.1

elitism = True
elite_size = 5

test = [-0.7, 0.5, 0.3, -0.9, 0.8]

random.seed(5)

# Create a custom data structure using a class
class Individual:
    def __init__(self, name):

        self.name = name
        
        self.values = []

        if current_generation_index == 0:
            self.values = [random.uniform(-1, 1) for x in range(5)]

        self.fitness = 0
        self.selection_probability = 0

    def evaluate_fitness(self):
        
        self.fitness = 0

        for i in range(len(test)):
            self.fitness += abs(test[i] - self.values[i])


population = {}

keys = [str(x) for x in range(population_size)]

current_generation_index = 0

for i in tqdm(range(generations + 1)):

    fitness_list = []

    if current_generation_index == 0:
        for name in keys:
            population[name] = Individual(name)

    for name in keys:
        population[name].evaluate_fitness()
        fitness_list.append(population[name].fitness)

    # store n number of elite members if enabled
    elites = genetic_operators_TEST.elitism(population, keys, elite_size)

    #genetic_operators_TEST.linear_ranking(population, keys)
    genetic_operators_TEST.exponential_ranking(population, keys)
    #genetic_operators_TEST.fitness_proportional(population, keys)
    
    genetic_operators_TEST.one_point_crossover(population, keys)
    #genetic_operators_TEST.uniform_crossover(population, keys)

    genetic_operators_TEST.mutation(population, keys, mutation_rate, mutation_standard_dev)

    if elitism == True:
        for i in range(elite_size):
            population[keys[i]].values = elites[i]
    
    print(current_generation_index, sum(fitness_list)/len(fitness_list), min(fitness_list))
    
    current_generation_index += 1

