import random

import numpy as np

import fitness_functions
import praat_control
import stats
from CONSTANTS import PRT_PARAMETER_DEFS, VTL_PARAMETER_DEFS


class Parent_Individual:
    def __init__(self, name, target_info, directory):

        self.name = name

        self.target_info = target_info

        self.directory = directory

        self.current_generation = 0

        # Initialise fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.absolute_fitness = 0
        self.selection_probability = 0

        # List for holding the real valued genotype values
        self.values = []


    def evaluate_fitness(self, fitness_type):
        
        self.evaluate_voice()
        self.evaluate_formants()
        self.evaluate_mfcc()

        if fitness_type == 'formant':
            self.evaluate_formant_fitness()
        elif fitness_type == 'filterbank':
            self.evaluate_mfcc_fitness()

        if self.voiced and self.target_info['scikit']:
            self.write_data_scikit()


    def evaluate_voice(self):

        file_path = self.directory / 'Generation{}'.format(self.current_generation)

        self.voice_report = praat_control.voice_report(file_path, self.target_info['target_length'], self.name)
        self.mean_pitch, self.frac_frames, self.voice_breaks = self.voice_report
        self.voiced = self.mean_pitch != False and self.voice_breaks == 0 and self.frac_frames < 0.1 and self.mean_pitch < 175


    def evaluate_formants(self):

        file_path = self.directory / 'Generation{}'.format(self.current_generation)

        self.formants = praat_control.write_formant_table(file_path, self.name)

        if self.voiced == False:
            self.formants = [4500 + x for x in self.target_info['target_formants']]


    def evaluate_formant_fitness(self):

        self.raw_fitness = fitness_functions.evaluate_fitness(self.formants,
                                                              self.target_info['target_formants'],
                                                              self.target_info['formant_repr'],
                                                              self.target_info['distance_metric'],
                                                              self.target_info['weight_features'])


        self.absolute_fitness = fitness_functions.evaluate_fitness(self.formants,
                                                                   self.target_info['target_formants'],
                                                                   'hz',
                                                                   'SAD',
                                                                   False)


    def loudness_penalty(self):

        # Extract loudness features
        self.intensity = praat_control.get_individual_intensity(self.name, self.directory, self.current_generation, self.target_info['target_intensity'])
        self.rms = praat_control.get_individual_RMS(self.name, self.directory, self.current_generation, self.target_info['target_rms'])

        # Apply loudness co-efficents
        if self.target_info['loudness_measure'] == 'rms':
            self.raw_fitness = self.raw_fitness * self.rms
        elif self.target_info['loudness_measure'] == 'intensity':
            self.raw_fitness = self.raw_fitness * self.intensity
        elif self.target_info['loudness_measure'] == 'both':
            self.raw_fitness = self.raw_fitness * ((self.rms + self.intensity) / 2.0)
        elif self.target_info['loudness_measure'] == 'none':
            pass


    def evaluate_mfcc(self):

        self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, self.directory, self.current_generation)
        self.fbank_average = praat_control.get_individual_fbank_average(self.name, self.directory, self.current_generation)
        self.logfbank_average = praat_control.get_individual_fbank_average(self.name, self.directory, self.current_generation)

    def evaluate_mfcc_fitness(self):

        if self.target_info['filterbank_type'] == 'mfcc_average':
            self.raw_fitness = fitness_functions.return_distance(self.target_info['target_mfcc_average'],
                                                                 self.mfcc_average,
                                                                 self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "fbank_average":
            self.raw_fitness = fitness_functions.return_distance(self.target_info['target_fbank_average'],
                                                                 self.fbank_average,
                                                                 self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "logfbank_average":
            self.raw_fitness = fitness_functions.return_distance(self.target_info['target_logfbank_average'],
                                                                 self.logfbank_average,
                                                                 self.target_info['distance_metric'])


    def write_out_data(self):
        
        stats.write_individual_to_csv(dict(vars(self)), self.directory, self.current_generation)


    def write_data_scikit(self):

        with open(self.directory / 'labelled_formant_data.txt', 'a') as self.cntk:
            self.cntk.write('{},{}\n'.format(','.join(str(x) for x in self.values), ','.join(str(x) for x in self.formants)))

        with open(self.directory / 'labelled_mfcc_data.txt', 'a') as self.cntk:
            self.cntk.write('{},{}\n'.format(','.join(str(x) for x in self.values), ','.join(str(x) for x in self.mfcc_average)))

        with open(self.directory / 'labelled_fbank_data.txt', 'a') as self.cntk:
            self.cntk.write('{},{}\n'.format(','.join(str(x) for x in self.values), ','.join(str(x) for x in self.fbank_average)))

        with open(self.directory / 'labelled_logfbank_data.txt', 'a') as self.cntk:
            self.cntk.write('{},{}\n'.format(','.join(str(x) for x in self.values), ','.join(str(x) for x in self.logfbank_average)))


class Individual_PRT(Parent_Individual):
    def __init__(self, name, target_info, directory):
        super().__init__(name, target_info, directory)

        # Load parameter definition from the CONSTANTS module
        self.parameters = PRT_PARAMETER_DEFS['ALL']

        # Initialise the genotype with random values for the first generation
        if self.current_generation == 0:
            self.values = [round(random.uniform(y, z), 2) for _, y, z in self.parameters]


    def create_synth_params(self):

        with open('{}/Generation{!s}/Individual{!s}.praat'.format(self.directory, self.current_generation, self.name), 'w') as self.artword:

            # Configure speaker type and sound length
            self.artword.write('Create Speaker... Robovox Male 2\n')
            self.artword.write('Create Artword... Individual{} {}\n'.format(self.name, self.target_info['target_length']))

            # Specify Lungs and LevatorPalatini parameter values
            self.artword.write('Set target... 0.0  0.1  Lungs\n')
            self.artword.write('Set target... 0.04  0.0  Lungs\n')
            self.artword.write('Set target... {}  0.0  Lungs\n'.format(self.target_info['target_length']))
            self.artword.write('Set target... 0.00  1 LevatorPalatini\n')
            self.artword.write('Set target... {}  1 LevatorPalatini\n'.format(self.target_info['target_length']))

            # Loop through the parameters and values lists and write these to the artword
            for i in range(len(self.parameters)):
                self.artword.write('Set target... 0.0 {} {}\n'.format(self.values[i], self.parameters[i][0]))
                self.artword.write('Set target... {} {} {}\n'.format(self.target_info['target_length'], self.values[i], self.parameters[i][0]))

            # Set sample rate and synthesise audio
            self.artword.write('select Artword Individual{}\n'.format(self.name))
            self.artword.write('plus Speaker Robovox\n')
            self.artword.write('To Sound... {} 25    0 0 0    0 0 0   0 0 0\n'.format(self.target_info['target_sample_rate']))
            self.artword.write('''nowarn do ("Save as WAV file...", "Individual{}.wav")\n'''.format(self.name))


class Individual_VTL(Parent_Individual):
    def __init__(self, name, target_info, directory):
        super().__init__(name, target_info, directory)

        # Load parameter definition from the CONSTANTS module
        self.parameters = VTL_PARAMETER_DEFS['ALL']

        # Initialise the genotype with random values for the first generation
        if self.current_generation == 0:
            self.values = [round(random.uniform(y, z), 2) for _, y, z in self.parameters]


    def create_synth_params(self):
        sample_rate = int(self.target_info['target_sample_rate'])
        target_time = float(self.target_info['target_length'])
        fold_type = 'Geometric glottis'
        step_size = int((sample_rate / 1000) * 2.5)
        target_pressure = 8000
        number_of_states = int((sample_rate * target_time) // step_size)
        pressure = np.geomspace(1, target_pressure, num=20)
        glottis_params = ['101.594', '0', '0.0102', '0.02035', '0.05', '1.22204', '1', '0.05', '0', '25', '-10']

        with open('{}\\Generation{}\\tract_seq{}.txt'.format(self.directory, self.current_generation, self.name), 'w') as f:
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
                f.write(' '.join(map(str,self.values)) + '\n')
            
            glottis_params[1] = str(target_pressure)

            for _ in range(number_of_states - 20):
                f.write(' '.join(glottis_params) + '\n')
                f.write(' '.join(map(str,self.values)) + '\n')
