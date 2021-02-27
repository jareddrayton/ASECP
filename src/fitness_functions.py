import math
import pydistance
import scipy.io.wavfile as wav
import numpy as np

from python_speech_features import mfcc
from python_speech_features import delta
from python_speech_features import logfbank

from CONSTANTS import WEIGHTS

def evaluate_fitness(formants, target_formants, formant_repr, metric, weight_features):
    """
    
    RETURNS
    -------
    fitness: float
    
    """
    feature_representations = {'hz': fitness_a1,
                               'mel': fitness_a2,
                               'cent': fitness_a3,
                               'bark': fitness_a4,
                               'erb': fitness_a5,
                               }

    formants, target_formants = feature_representations[formant_repr](formants, target_formants)

    if weight_features:
        formants, target_formants = apply_weights(formants, target_formants)

    fitness = return_distance(formants, target_formants, metric)

    return fitness


def apply_weights(x, y):
    no_of_weights = str(len(x))
    
    coefficients = WEIGHTS[no_of_weights]

    for i, weight in enumerate(coefficients):
        x[i] = x[i] * weight
        y[i] = y[i] * weight

    return x, y


def return_distance(x, y, metric):
    # a list comprhension for automatically generating co efficients

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


def fitness_a1(formants, target_formants):
    """Compares frequencies using Hz scale

    :returns: a float representing fitness
    """
    formants = formants[:]
    target_formants = target_formants[:]

    return formants, target_formants


def fitness_a2(formants, target_formants):
    """Compares frequencies using the Mel scale.

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_mel, formants))
    target_formants = list(map(hz_to_mel, target_formants))

    return formants, target_formants


def fitness_a3(formants, target_formants):
    """Compares frequencies using Cents

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_cent, formants, target_formants))
    target_formants = [0 for x in formants]

    return formants, target_formants


def fitness_a4(formants, target_formants):
    """Compares frequencies using the bark scale

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_bark, formants))
    target_formants = list(map(hz_to_bark, target_formants))

    return formants, target_formants


def fitness_a5(formants, target_formants):
    """Compares frequencies using erb scale

    :returns: a float representing fitness
    """

    formants = list(map(hz_to_erb, formants))
    target_formants = list(map(hz_to_erb, target_formants))

    return formants, target_formants


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


#################################################################################################################
#################################################################################################################

def fitness_mfcc_average(x, y, metric):
    """
    Compare the averages of the mfcc features
    """
    return return_distance(x, y, metric)


def fitness_logfbank_average(x, y, metric):
    """
    Compare the average of the filterbank features
    """
    return return_distance(x, y, metric)


def fitness_twodim_sad(x, y):
    """
    Compare the MFCC features of target and candidate sound.
    """

    s = 0

    for i in range(len(x)):
        for j in range(len(x[i])):
            s += abs(x[i][j] - y[i][j])

    return s


def fitness_twodim_ssd(x, y):
    """
    Compare the MFCC features of target and candidate sound.
    """

    s = 0

    for i in range(len(x)):
        for j in range(len(x[i])):
            s += abs(x[i][j] - y[i][j]) ** 2

    return s
