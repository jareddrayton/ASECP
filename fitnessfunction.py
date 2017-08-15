import math

import pydistance


#################################################################################################################
#################################################################################################################

def fitness_a1(formants, targetformants, metric):
    """Compares frequencies using Hz scale

    :returns: a float representing fitness
    """

    return return_distance(formants, targetformants, metric)


def fitness_a2(formants, targetformants, metric):
    """Compares frequencies using the Mel scale.

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_mel, formants))
    targetformants = list(map(hz_to_mel, targetformants))

    return return_distance(formants, targetformants, metric)


def fitness_a3(formants, targetformants, metric):
    """Compares frequencies using Cents

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_cent, formants, targetformants))
    targetformants = [0 for x in formants]

    return return_distance(formants, targetformants, metric)


def fitness_a4(formants, targetformants, metric):
    """Compares frequencies using the bark scale

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_bark, formants))
    targetformants = list(map(hz_to_bark, targetformants))

    return return_distance(formants, targetformants, metric)


def fitness_a5(formants, targetformants, metric):
    """Compares frequencies using the bark scale

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_erb, formants))
    targetformants = list(map(hz_to_erb, targetformants))

    return return_distance(formants, targetformants, metric)

def return_distance(x, y, metric):

    # a list comprhension for automatically generating co efficients
    coefficients = [1.0 + i for i in range(len(x))]

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


def fitness_brito(formants, targetformants):
    """
    Implements the distance measure as defined by Brito 2007 and 2006
    """

    weights_osix = [90, 60, 24, 12]
    weights_oseven = [40, 30, 15, 10]

    formant_distances = []

    for i in range(len(formants)):
        formant_distances.append(weights_oseven[i] * (abs(formants[i] - targetformants[i]) / formants[i]))

    print(sum(formant_distancess))

    return sum(formant_distances)

#################################################################################################################
#################################################################################################################

def fitness_mfcc()
    """
    Compare the MFCC features of target and candidate sound.
    """



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

# Helper functions for value conversion

def hz_to_mel(f):
    """ converts a frequency in hz to the mel scale

    returns: a float
    """

    return 2595 * math.log10(1 + (f / 700.0))


def hz_to_cent(f1, f2):
    """ takes two lists of frequencies in hz and returns the differences in cents

    returns: a float
    """

    return math.fabs(1200 * math.log(f1 / f2, 2))


def hz_to_bark(f):
    """ converts a given frequency to the bark scale

    returns a float
    """

    return ((26.81 * f) / (1960 + f)) - 0.53

def hz_to_erb(f):
    """ converts a given frequency to the erb scale

    returns a float
    """

    return 0.108 * f + 24.7