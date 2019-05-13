import random
from tqdm import tqdm

import genetic_operators

population_size = 10
generations = 10

mutation_rate = 0.1
mutation_standard_dev = 0.1

test = [-0.7, 0.5, 0.3, -0.9, 0.8]

random.seed(2)

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

    if current_generation_index == 0:
        for name in keys:
            population[name] = Individual(name)

    for name in keys:
        population[name].evaluate_fitness()
        print(population[name].fitness)
    
    genetic_operators.linear_ranking(population, keys)
    
    genetic_operators.one_point_crossover(population, keys)

    genetic_operators.mutation(population, keys, mutation_rate, mutation_standard_dev)
    
    current_generation_index += 1

