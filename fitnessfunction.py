import math, 

import praatcontrol, pydistance, stats

#################################################################################################################
#################################################################################################################

def fitness_a1(formants,voiced,targetfrequencies,metric):
	"""Compares frequencies using Hz scale

	:returns: a float representing fitness
	"""
	print(formants)
	print(targetfrequencies)

	return return_distance(formants, targetfrequencies, metric)


def fitness_a2(formants,voiced,targetfrequencies,metric):
	"""Compares frequencies using the Mel scale.

	:returns: a float representing fitness
	"""

	targetfrequencies = praatcontrol.hz_to_mel(targetfrequencies)
	formants = praatcontrol.hz_to_mel(formants)

	return return_distance(formants, targetfrequencies, metric)

def fitness_a3(formants,voiced,targetfrequencies,metric):
	"""Compares frequencies using Cents

	:returns: a float representing fitness
	"""

	difference = []
	
	for i in range(len(targetfrequencies)):
		difference.append(math.fabs(1200 * math.log(formants[i] / targetfrequencies[i], 2)))
	
	targetfrequencies = [0,0,0]
	
	return return_distance(difference, targetfrequencies, metric)

def return_distance(x, y, metric):

	coefficients = [5.0, 3.0, 1.0]
	
	use_coeff = False

	if use_coeff == True:
		for i in range(len(x)):
			x[i] = x[i] * coefficients[i]

	if   metric == "SAD":
		return pydistance.SAD(x,y)
	elif metric == "SSD":
		return pydistance.SSD(x,y)
	elif metric == "MAE":
		return pydistance.MAE(x,y)
	elif metric == "MSE":
		return pydistance.MSE(x,y)
	elif metric == "EUC":
		return pydistance.EUC(x,y)
	elif metric == "CAN":
		return pydistance.CAN(x,y)

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