import os
import pathlib
import subprocess

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

parameter_data = pd.read_csv('labelled_mfcc_datai.txt')

y = parameter_data.iloc[:, 0:27]
X = parameter_data.iloc[:, 27:]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)
# (54 for i in range(10)
mlp = MLPRegressor(hidden_layer_sizes=(27 for i in range(20)), max_iter=1000, activation='relu', alpha=0.0001)

mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

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

################################################################################


def get_individual_mfcc(sound_file='ay.wav'):

    (rate, signal) = wav.read(sound_file)
    print(rate)
    mfcc_features = mfcc(signal, rate, winlen=0.025, winstep=0.025, appendEnergy=False)

    return mfcc_features


def run_praat_command(praat_script, purge=False):
    subprocess.call(['./praat',
                     '--run',
                     '--ansi',
                     praat_script], stdout=subprocess.DEVNULL)
    
    if purge:
        os.remove(praat_script)

def make_artword(values, name):
    
    parameters = PRT_PARAMETER_DEFS['ALL']
    
    target_length = '1.0'

    script_filepath = 'out_params_to_sound{}.praat'.format(name)
    
    with open(script_filepath, 'w') as f:

        # Configure speaker type and sound length
        f.write('Create Speaker... Robovox Male 2\n')
        f.write('Create Artword... Individual {}\n'.format(target_length))

        # Specify Lungs and LevatorPalatini parameter values
        f.write('Set target... 0.0  0.1  Lungs\n')
        f.write('Set target... 0.04  0.0  Lungs\n')
        f.write('Set target... {}  0.0  Lungs\n'.format(target_length))
        f.write('Set target... 0.00  1 LevatorPalatini\n')
        f.write('Set target... {}  1 LevatorPalatini\n'.format(target_length))

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(parameters)):
            f.write('Set target... 0.0 {} {}\n'.format(values[i], parameters[i][0]))
            f.write('Set target... {} {} {}\n'.format(target_length, values[i], parameters[i][0]))

        # Set sample rate and synthesise audio
        f.write('select Artword Individual\n')
        f.write('plus Speaker Robovox\n')
        f.write('To Sound... 44100 25    0 0 0    0 0 0   0 0 0\n')
        f.write('''nowarn do ("Save as WAV file...", "{}_praat_logfbank.wav")\n'''.format(name))
    
    run_praat_command(script_filepath, True)

def make_artword_mod(values, name):
    
    parameters = PRT_PARAMETER_DEFS['ALL']
    
    target_length = '1.0'

    script_filepath = 'out_params_to_sound{}.praat'.format(name)
    
    with open(script_filepath, 'w') as f:

        # Configure speaker type and sound length
        f.write('Create Speaker... Robovox Male 2\n')
        f.write('Create Artword... Individual {}\n'.format(target_length))

        # Specify Lungs and LevatorPalatini parameter values
        f.write('Set target... 0.0  0.1  Lungs\n')
        f.write('Set target... 0.04  0.0  Lungs\n')
        f.write('Set target... {}  0.0  Lungs\n'.format(target_length))
        f.write('Set target... 0.00  1 LevatorPalatini\n')
        f.write('Set target... {}  1 LevatorPalatini\n'.format(target_length))

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(parameters)):
            f.write('Set target... 0.0 {} {}\n'.format(values[i], parameters[i][0]))
            f.write('Set target... {} {} {}\n'.format(target_length, values[i], parameters[i][0]))

        # Set sample rate and synthesise audio
        f.write('select Artword Individual\n')
        f.write('plus Speaker Robovox\n')
        f.write('To Sound... 44100 25    0 0 0    0 0 0   0 0 0\n')
        f.write('''nowarn do ("Save as WAV file...", "{}_praat_pp.wav")\n'''.format(name))
    
    run_praat_command(script_filepath, True)


parent_dir = pathlib.Path.cwd()
root_target_sounds_directory = parent_dir / 'test_sounds'
sound_files = root_target_sounds_directory.glob('*.wav')


if False:
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
        make_artword(values, name)



if False:
    for i, frame in enumerate(get_individual_mfcc()):
        frame = frame.reshape(1,-1)
        test = scaler.transform(frame)
        new_predict = mlp.predict(test)
        values = new_predict[0]
        make_artword(values, str(i))
