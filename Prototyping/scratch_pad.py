import random
from operator import itemgetter

population_size = 10

keys = [str(x) for x in range(population_size)]
fitness = [random.randint(0,10) for x in range(population_size)]

print(keys,fitness)

keys_fitness = [(keys[i], fitness[i]) for i in range(population_size)]

print(keys_fitness)

keys_fitness = sorted(keys_fitness, key=itemgetter(1), reverse=True)

print(keys_fitness)

ranked, fitness = zip(*keys_fitness)

print(ranked, fitness)

for rank in ranked:
    print(type(rank))