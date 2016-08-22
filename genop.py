import random, math
from operator import itemgetter

#################################################################################################################
#################################################################################################################

"""Functions for assigning the selection probabilities"""

def fitness_proportional(population, keys):
	""" Fitness proportional selection """

	temppopulation = population

	scaledfitness = []
	
	for name in keys:
		population[name].fitnessscaled = round(1.0 / population[name].fitness, 10)
		scaledfitness.append(population[name].fitnessscaled)
	
	for name in keys: 
		population[name].fitnessscaled = population[name].fitnessscaled / sum(scaledfitness)

	one_crossover(population, keys, temppopulation)


def lin_rank(population,keys):
	""" Linear probability distribution """ 
	
	temppopulation = population

	c = len(population)
	
	s = 2.0 # This can be in the range 1.0 < x <= 2.0

	fitness = []

	index = keys
	
	for name in keys:
		fitness.append(population[name].fitness)
	
	zippedlists = zip(index, fitness)
	sortedlist = sorted(zippedlists, key=itemgetter(1))
	x, y = zip(*sortedlist)
	ranked = list(x)
	ranked.reverse()
	
	print ranked
	
	probabilities = []
	
	for i in range(len(ranked)):
				
		population[ranked[i]].fitnessscaled = (2 - s) / c + (2.0 * i * (s - 1)) / (c*(c-1))
		print ranked[i], population[ranked[i]].fitnessscaled
		probabilities.append(population[ranked[i]].fitnessscaled)
	
	print sum(probabilities)

	# uniform_crossover(population, keys, temppopulation)
	one_crossover(population, keys, temppopulation)


def exp_rank():
	"""Exponential ranking"""

	probabilities = []
	
	for i in range(c):
		
		prob = 1 - (math.e ** -i)
		prob = prob / c

		probabilities.append(prob)

################################################################

def roulette_spin(population, keys):
	
	roulettespin = random.uniform(0, 1) 
	currentcumulative = 0
	
	for name in keys:
		currentcumulative += population[name].fitnessscaled
		if currentcumulative > roulettespin:
			return name


def stochastic_u_sampling():
	""" Stochastic Universal Sampling Selection """

	pass

#####################################################################

def tournament_selection():
	""" Tournament selection"""
	
	pass

#################################################################################################################
#################################################################################################################

def one_crossover(population, keys, temppopulation):
	""" One Point Crossover """
	
	for name in keys:
		
		ca = roulette_spin(population, keys)
		cb = roulette_spin(population, keys)
		
		crossoverpoint = random.randint(0,27)
		
		temppopulation[name].values = population[ca].values[0:crossoverpoint] + population[cb].values[crossoverpoint:27]  
		
		population[name].values = temppopulation[name].values


def two_crossover():
	""" Two point Crossover Operator """

	pass

def uniform_crossover(population, keys, temppopulation):
	""" Uniform Crossover Operator """

	for name in keys:
		ca = roulette_spin(population, keys)
		cb = roulette_spin(population, keys)
		print "Parent A", population[ca].values
		print "Parent B", population[cb].values
		for i in range(len(temppopulation[name].values)):
			if random.random() < 0.5:
				temppopulation[name].values[i] = population[ca].values[i]
			else:
				temppopulation[name].values[i] = population[cb].values[i]
		print "Child", temppopulation[name].values 
		population[name].values = temppopulation[name].values


#################################################################################################################
#################################################################################################################

def mutation(population, keys, mutationprobability, standarddeviation):
	""" Mutation function """
	
	for name in keys:
		for i in range(len(population[name].values)):
			mutationthresh = random.random()
			if mutationprobability > mutationthresh:
				population[name].values[i] = population[name].values[i] + round(random.gauss(0, standarddeviation), 1)
				if population[name].values[i] > 1.0:
					population[name].values[i] = 1
				elif population[name].values[i] < -1.0:
					population[name].values[i] = -1.0