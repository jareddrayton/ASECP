import math, praatcontrol, pydistance, stats

#################################################################################################################
#################################################################################################################

def fitness_a1(name, directory, currentgeneration, targetformants, metric):
	"""Compares frequencies using Hz scale

	:returns: a float representing fitness
	"""

	individualfrequencies = praatcontrol.get_individual_frequencies(name,directory,currentgeneration)
	
	stats.write_formants(name, directory, currentgeneration, individualfrequencies)
	
	return return_distance(individualfrequencies, targetformants, metric)


def fitness_a2(name, directory, currentgeneration, targetformants, metric):
	"""Compares frequencies using the Mel scale.

	:returns: a float representing fitness
	"""

	individualfrequencies = praatcontrol.get_individual_frequencies(name,directory,currentgeneration)

	stats.write_formants(name, directory, currentgeneration, individualfrequencies)

	targetformants = praatcontrol.hz_to_mel(targetformants)
	individualfrequencies = praatcontrol.hz_to_mel(individualfrequencies)

	return return_distance(individualfrequencies, targetformants, metric)


def fitness_a3(name, directory, currentgeneration, targetformants, metric):
	"""Compares frequencies using Cents

	:returns: a float representing fitness
	"""

	individualfrequencies = praatcontrol.get_individual_frequencies(name,directory,currentgeneration)
	difference = []
	
	stats.write_formants(name, directory, currentgeneration, individualfrequencies)
	
	for i in range(len(targetformants)):
		difference.append(math.fabs(1200 * math.log(individualfrequencies[i] / targetformants[i], 2)))
	
	targetformants = [0,0]
	
	return return_distance(difference, targetformants, metric)

def return_distance(x, y, metric):

	coefficients = [1.5, 3.0, 2.0, 1.0]
	
	use_coeff = False

	if use_coeff == True:
		for i in range(len(x)):
			x[i] = x[i] * coefficients[i]

	if metric == "SAD":
		return pydistance.SAD(x,y)
	elif metric == "SSD":
		return pydistance.SSD(x,y)
	elif metric == "MAE":
		return pydistance.MAE(x,y)
	elif metric == "MSE":
		return pydistance.MSE(x,y)
	elif metric == "EUC":
		return pydistance.EUC(x,y)

#################################################################################################################
#################################################################################################################

def fitness_c1():
	"""
	Compare the MFCC features of the target and candidate sound.
	"""

	# DTW Dynamic Time Warping

	#obtain an array of the average mfcc features


	return fitness

#################################################################################################################
#################################################################################################################

def fitness_d():
	"""
	Compare a cochleargram by using a Structural Similarity index
	"""
	

	return fitness

#################################################################################################################
#################################################################################################################

def fitness_e():
	"""
	Compare using Auto/Cross-correlation
	"""

	return fitness