import os
import pathlib
import subprocess
import time

import ctypes
import sys

import numpy as np
import pandas as pd
import scipy.io.wavfile as wav
import sklearn
from python_speech_features import fbank, logfbank, mfcc
from sklearn.metrics import (confusion_matrix, explained_variance_score,
                             max_error, mean_absolute_error)
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler

from CONSTANTS import PRT_PARAMETER_DEFS

parameter_data = pd.read_csv('data_sets\\labelled_mfcc_pp_2400.txt')

y = parameter_data.iloc[:, 0:19]
X = parameter_data.iloc[:, 19:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPRegressor(hidden_layer_sizes=(38, 38, 38, 38, 38, 38, 38), max_iter=1000, activation='relu', alpha=0.0001)

mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

print('Scores')
print(explained_variance_score(y_test, predictions))
print(mean_absolute_error(y_test, predictions))


#####################################################################
# Read in a list of test vowels
# extract their mfcc features
# plug these into the neural network
# extract predicted values
# make praat script
# make praat run script and output audio file


def get_individual_mfcc_average(sound_file):

    (rate, signal) = wav.read(sound_file)
    print(rate)
    mfcc_features = mfcc(signal, rate, winlen=0.025, winstep=0.025, appendEnergy=False)

    return np.average(mfcc_features, axis=0)

def get_individual_fbank_average(sound_file):

    (rate, signal) = wav.read(sound_file)

    logfbank_features_individual, _ = fbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features_individual, axis=0)

def get_individual_logfbank_average(sound_file):

    (rate, signal) = wav.read(sound_file)

    logfbank_features_individual = logfbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features_individual, axis=0)


def get_individual_mfcc(sound_file='ay.wav'):

    (rate, signal) = wav.read(sound_file)
    print(rate)
    mfcc_features = mfcc(signal, rate, winlen=0.025, winstep=0.025, appendEnergy=False)

    return mfcc_features

################################################################################


def create_synth_params(name, values):
    sample_rate = 44100
    target_time = 1.0
    fold_type = 'Geometric glottis'
    step_size = 110  # assume 44100 sample rate.
    target_pressure = 10000
    number_of_states = int((sample_rate * target_time) // step_size)
    pressure = np.geomspace(1, target_pressure, num=20)
    glottis_params = ['101.594', '0', '0.0102', '0.02035', '0.05', '1.22204', '1', '0.05', '0', '25', '-10']

    with open('tract_seq{}.txt'.format(name), 'w') as f:
        f.write('# The first two lines (below the comment lines) indicate the name of the vocal fold model and the number of states.' + '\n')
        f.write('# The following lines contain the control parameters of the vocal folds and the vocal tract (states)' + '\n')
        f.write('# in steps of 110 audio samples (corresponding to about 2.5 ms for the sampling rate of 44100 Hz).' + '\n')
        f.write('# For every step, there is one line with the vocal fold parameters followed by' + '\n')
        f.write('# one line with the vocal tract parameters.' + '\n')

        f.write('#' + '\n')
        f.write(fold_type + '\n')
        f.write(str(number_of_states) + '\n')
        
        for state in pressure:
            glottis_params[1] = str(state)
            f.write(' '.join(glottis_params) + '\n')
            f.write(' '.join(map(str, values)) + '\n')
        
        glottis_params[1] = str(target_pressure)

        for _ in range(number_of_states - 20):
            f.write(' '.join(glottis_params) + '\n')
            f.write(' '.join(map(str, values)) + '\n')

def make_sound(name):

    root_vtl_directory = parent_dir / 'vocaltractlab'

    if sys.platform == 'win32':
        VTL = ctypes.cdll.LoadLibrary(str(root_vtl_directory / 'VocalTractLabApi.dll'))
    else:
        VTL = ctypes.cdll.LoadLibrary('./VocalTractLabApi.so')

    speaker_file_name = ctypes.c_char_p(str(root_vtl_directory / 'JD2.speaker').encode())

    failure = VTL.vtlInitialize(speaker_file_name)

    if failure != 0:
        raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)

    tract = ctypes.c_char_p('tract_seq{}.txt'.format(name).encode())
    audio_f = ctypes.c_char_p('name_vtl{}.wav'.format(name).encode())
    failure = VTL.vtlTractSequenceToAudio(tract, audio_f, None, None)



parent_dir = pathlib.Path.cwd().parent
root_target_sounds_directory = parent_dir / 'target_sounds'
sound_files = root_target_sounds_directory.glob('*44100.wav')

#print(sound_files)

for sound_file in sound_files:
    test = get_individual_mfcc_average(sound_file)
    #test = get_individual_fbank_average(sound_file)
    #test = get_individual_logfbank_average(sound_file)
    
    test =  test.reshape(1, -1)

    print(test)
    test = scaler.transform(test)

    new_predict = mlp.predict(test)

    print(new_predict[0])

    values = new_predict[0]
    name = sound_file.name
    create_synth_params(name, values)
    make_sound(name)
    time.sleep(3)



