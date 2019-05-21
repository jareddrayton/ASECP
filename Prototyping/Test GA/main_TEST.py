import random
from tqdm import tqdm

import genetic_operators_TEST

population_size = 100
generations = 100

mutation_rate = 0.05
mutation_standard_dev = 0.15

elitism = 0

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
        #print(name, population[name].selection_probability)
        #print(name, population[name].fitness)
        fitness_list.append(population[name].fitness)


    genetic_operators_TEST.linear_ranking(population, keys)
    
    #genetic_operators_TEST.one_point_crossover(population, keys)
    genetic_operators_TEST.uniform_crossover(population, keys)

    genetic_operators_TEST.mutation(population, keys, mutation_rate, mutation_standard_dev)
    
    print(current_generation_index, sum(fitness_list)/len(fitness_list))
    
    current_generation_index += 1

