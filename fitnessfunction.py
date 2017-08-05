import math

import pydistance


#################################################################################################################
#################################################################################################################

def fitness_a1(formants, targetfrequencies, metric):
    """Compares frequencies using Hz scale

	:returns: a float representing fitness
	"""
    print(formants)
    print(targetfrequencies)

    return return_distance(formants, targetfrequencies, metric)


def fitness_a2(formants, targetfrequencies, metric):
    """Compares frequencies using the Mel scale.

	:returns: a float representing fitness
	"""

    targetfrequencies = hz_to_mel(targetfrequencies)
    formants = hz_to_mel(formants)

    return return_distance(formants, targetfrequencies, metric)


def fitness_a3(formants, targetfrequencies, metric):
    """Compares frequencies using Cents

	:returns: a float representing fitness
	"""

    difference = []

    for i in range(len(targetfrequencies)):
        difference.append(math.fabs(1200 * math.log(formants[i] / targetfrequencies[i], 2)))

    targetfrequencies = [0, 0]

    return return_distance(difference, targetfrequencies, metric)


def fitness_a4(formants, targetfrequencies, metric):

    formants = list(map(hz_to_bark, formants))
    targetfrequencies = list(map(hz_to_bark, targetfrequencies))

    return return_distance(formants, targetfrequencies, metric)


def return_distance(x, y, metric):
    coefficients = [1.0, 2.0]

    use_coeff = False

    if use_coeff == True:
        for i in range(len(x)):
            x[i] = x[i] * coefficients[i]

    if metric == "SAD":
        return pydistance.SAD(x, y)
    elif metric == "SSD":
        return pydistance.SSD(x, y)
    elif metric == "MAE":
        return pydistance.MAE(x, y)
    elif metric == "MSE":
        return pydistance.MSE(x, y)
    elif metric == "EUC":
        return pydistance.EUC(x, y)
    elif metric == "CAN":
        return pydistance.CAN(x, y)


#################################################################################################################
#################################################################################################################

def fitness_c1():
    """
	Compare the MFCC features of the target and candidate sound.
	"""

    # DTW Dynamic Time Warping

    # obtain an array of the average mfcc features

    pass


#################################################################################################################
#################################################################################################################

def fitness_d():
    """
	Compare a cochleargram by using a Structural Similarity index
	"""

    pass


#################################################################################################################
#################################################################################################################

def fitness_e():
    """
	Compare using Auto/Cross-correlation
	"""

    pass


#################################################################################################################
#################################################################################################################

def hz_to_mel(frequencies):
    """ Converts a list of frequencies to mel scale

    returns: a list of frequencies converted to mel
    """

    for i in range(len(frequencies)):
        frequencies[i] = 2595 * math.log10(1 + (frequencies[i] / 700.0))

    return frequencies


def hz_to_cent(list1, list2):
    """ Takes two lists of frequencies and returns their differences in cents

    returns:
    """

    for i in range(len(frequencies)):
        (math.fabs(1200 * math.log(list2[i] / list1[i], 2)))
    return frequencies


def hz_to_bark(f):
    """ """
    return ((26.81 * f) / (1960 + f)) - 0.53
