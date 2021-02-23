import random

import numpy as np

import fitness_functions
import praat_control
import stats
from CONSTANTS import PRT_PARAMETER_DEFS, VTL_PARAMETER_DEFS


class Individual_PRT:
    def __init__(self, name, target_info, directory):

        self.name = name

        self.target_info = target_info

        self.directory = directory

        self.current_generation = 0

        # Initialise fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.selection_probability = 0

        # List for holding the real valued genotype values
        self.values = []

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


    def evaluate_formants(self):

        file_path = self.directory / 'Generation{}'.format(self.current_generation)
        
        self.formants = praat_control.write_formant_table(file_path, self.name)
        self.voice_report = praat_control.voice_report(file_path, self.target_info['target_length'], self.name)

        self.mean_pitch, self.frac_frames, self.voice_breaks = self.voice_report

        self.voiced = self.mean_pitch != False and self.voice_breaks == 0 and self.frac_frames < 0.1 and self.mean_pitch < 175

        if self.mean_pitch == False or self.mean_pitch > 175 or self.frac_frames > 0.1 or self.voice_breaks > 0:
            self.formants = [4500 + x for x in self.target_info['target_formants']]

        self.raw_fitness = fitness_functions.fitness_a1(self.formants[:3], self.target_info['target_formants'][:3], self.target_info['distance_metric'])
        
        self.absolutefitness = fitness_functions.fitness_a1(self.formants[:3], self.target_info['target_formants'][:3], self.target_info['distance_metric'])
 
        self.write_out_formants()

        if self.voiced and self.target_info['scikit']:
            self.write_formants_scikit()

        if self.voiced and self.target_info['scikit']:
            self.write_formants_scikit()


    def write_out_formants(self):

        stats.write_formants(self.name,
                             self.directory,
                             self.current_generation,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)


    def write_formants_scikit(self):
        """
        Writes the formant feature and praat parameter value pairs as comma seperated values.
        """

        with open('labelled_data.txt', 'a') as self.cntk:
            self.cntk.write('{},{}\n'.format(','.join(str(x) for x in self.values), ','.join(str(x) for x in self.formants)))


    def write_filterbank_cntk(self):
        
        self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, self.directory, self.current_generation)

        with open('cntk_mfcc_data.txt', 'a') as self.cntk:
            # append a new pair of features and labels
            self.cntk.write('|labels {} '.format(" ".join(str(x) for x in self.values)))
            self.cntk.write('|features {} \n'.format(" ".join(str(x) for x in self.mfcc_average)))



    def voiced_penalty(self):
        """
        Instance method for ascertaining whether an individual is voiced or not.
        
        """
        # Assigns True or False to self.voiced, based on whether praat can calculate pitch 
        self.voiced = praat_control.get_individual_pitch(self.name, self.directory, self.current_generation)

        # If a pitch is detected the formants are calculated and assigned to self.formants
        
        if self.voiced == True:
            #self.formants = praat_control.get_individual_formants(self.name, self.directory, self.current_generation, self.target_info['target_sample_rate'])
            file_path = self.directory / 'Generation{}'.format(self.current_generation)
            self.formants = praat_control.write_formant_table(file_path, self.name)
        else:
            self.formants = [self.target_info['target_sample_rate'] / 2 for x in range(5)]

        self.formants = self.formants[0:self.target_info['formant_range']]

        # This acts as a baseline fitness attribute to compare different fitness functions
        self.absolutefitness = fitness_functions.fitness_a1(self.formants, self.target_info['target_formants'], "SAD")


    def evaluate_formant(self):

        self.voiced_penalty()

       # Calls the relevant fitness function based on cmd line argument
        if self.target_info['formant_repr'] == 'hz':
            self.raw_fitness = fitness_functions.fitness_a1(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == 'mel':
            self.raw_fitness = fitness_functions.fitness_a2(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == 'cent':
            self.raw_fitness = fitness_functions.fitness_a3(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == 'bark':
            self.raw_fitness = fitness_functions.fitness_a4(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        elif self.target_info['formant_repr'] == 'erb':
            self.raw_fitness = fitness_functions.fitness_a5(self.formants, self.target_info['target_formants'], self.target_info['distance_metric'])
        
        elif self.target_info['formant_repr'] == 'brito':
            self.raw_fitness = fitness_functions.fitness_brito(self.formants, self.target_info['target_formants'])

        # Apply a penalty of the sound is not voiced
        if self.voiced == False:
            self.raw_fitness = self.raw_fitness * 10

        # Extract loudness features
        self.intensity = praat_control.get_individual_intensity(self.name, self.directory, self.current_generation, self.target_info['target_intensity'])
        self.rms = praat_control.get_individual_RMS(self.name, self.directory, self.current_generation, self.target_info['target_rms'])

        # Apply loudness co-efficents
        if self.target_info['loudness_measure'] == "rms":
            self.raw_fitness = self.raw_fitness * self.rms
        elif self.target_info['loudness_measure'] == "intensity":
            self.raw_fitness = self.raw_fitness * self.intensity
        elif self.target_info['loudness_measure'] == "both":
            self.raw_fitness = self.raw_fitness * ((self.rms + self.intensity) / 2.0)
        elif self.target_info['loudness_measure'] == "none":
            pass

        ###########################################################################################
        # Write feature information to a csv file
        

        ###########################################################################################
        # Call the write_formants_cntk method if a sound is voiced

        if self.voiced and self.target_info['cntk']:
            self.write_formants_cntk()

    def evaluate_filterbank(self):
        # MFCC and filterbank based fitness functions
        
        self.voiced_penalty()

        if self.target_info['filterbank_type'] == "mfcc_average":
            self.mfcc_average = praat_control.get_individual_mfcc_average(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_mfcc_average(self.target_info['target_mfcc_average'], self.mfcc_average, self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "logfbank_average":
            self.logfbank_average = praat_control.get_individual_logfbank_average(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_logfbank_average(self.target_info['target_logfbank_average'], self.logfbank_average, self.target_info['distance_metric'])

        elif self.target_info['filterbank_type'] == "mfcc_sad":
            self.mfcc = praat_control.get_individual_mfcc(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(self.target_info['target_mfcc'], self.mfcc)

        elif self.target_info['filterbank_type'] == "mfcc_ssd":
            self.mfcc = praat_control.get_individual_mfcc(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(self.target_info['target_mfcc'], self.mfcc)

        elif self.target_info['filterbank_type'] == "logfbank_sad":
            self.logfbank = praat_control.get_individual_logfbank(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_sad(self.target_info['target_logfbank'], self.logfbank)

        elif self.target_info['filterbank_type'] == "logfbank_ssd":
            self.logfbank = praat_control.get_individual_logfbank(self.name, self.directory, self.current_generation)
            self.raw_fitness = fitness_functions.fitness_twodim_ssd(self.target_info['target_logfbank'], self.logfbank)
        
        stats.write_formants(self.name,
                             self.directory,
                             self.current_generation,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
        
        if self.voiced and self.target_info['cntk']:
            self.write_filterbank_cntk()





class Individual_VTL:
    def __init__(self, name, target_info, directory):


        self.name = name

        self.target_info = target_info

        self.directory = directory

        self.current_generation = 0

        # Initialise fitness score variables
        self.raw_fitness = 0
        self.scaled_fitness = 0
        self.selection_probability = 0

        # List for holding the real valued genotype values
        self.values = []

        # Load parameter definition from the CONSTANTS module
        self.parameters = VTL_PARAMETER_DEFS['ALL']

        # Initialise the genotype with random values for the first generation
        if self.current_generation == 0:
            self.values = [round(random.uniform(y, z), 2) for _, y, z in self.parameters]

    def create_synth_params(self):
        sample_rate = 44100
        target_time = 1.0
        fold_type = 'Geometric glottis'
        step_size = 110  # assume 44100 sample rate.
        target_pressure = 10000
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
    
    def evaluate_formants(self):

        file_path = self.directory / 'Generation{}'.format(self.current_generation)
        
        self.formants = praat_control.write_formant_table(file_path, self.name)
        self.voice_report = praat_control.voice_report(file_path, self.target_info['target_length'], self.name)

        self.mean_pitch, self.frac_frames, self.voice_breaks = self.voice_report

        self.voiced = self.mean_pitch != False

        if self.mean_pitch == False or self.mean_pitch > 200 or self.frac_frames > 0.1 or self.voice_breaks > 0:
            self.formants = [4500 + x for x in self.target_info['target_formants']]

        self.raw_fitness = fitness_functions.fitness_a1(self.formants[:3], self.target_info['target_formants'][:3], self.target_info['distance_metric'])
        
        self.absolutefitness = fitness_functions.fitness_a1(self.formants[:3], self.target_info['target_formants'][:3], self.target_info['distance_metric'])

        self.write_out_formants()


    def write_out_formants(self):

        stats.write_formants(self.name,
                             self.directory,
                             self.current_generation,
                             self.formants,
                             self.raw_fitness,
                             self.voiced,
                             self.absolutefitness)
