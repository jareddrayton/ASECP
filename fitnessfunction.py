import math

import pydistance


#################################################################################################################
#################################################################################################################

def fitness_a1(formants, targetfrequencies, metric):
    """Compares frequencies using Hz scale

	:returns: a float representing fitness
	"""

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

    targetfrequencies = [0 for x in targetfrequencies]

    return return_distance(difference, targetfrequencies, metric)


def fitness_a4(formants, targetfrequencies, metric):
    formants = list(map(hz_to_bark, formants))
    targetfrequencies = list(map(hz_to_bark, targetfrequencies))

    return return_distance(formants, targetfrequencies, metric)


def return_distance(x, y, metric):
    coefficients = [1.0, 2.0]

    use_coeff = False

    if use_coeff:
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


def hz_to_mel(f):
    """ converts a frequency in hz to the mel scale

    returns: a float mel
    """

    return 2595 * math.log10(1 + (f / 700.0))


def hz_to_cent(f1, f2):
    """ Takes two lists of frequencies and returns their differences in cents

    returns:
    """

    return math.fabs(1200 * math.log(f1 / f2, 2))


def hz_to_bark(f):
    """ converts a given frequency

    returns a float value representing
    """

    return ((26.81 * f) / (1960 + f)) - 0.53
