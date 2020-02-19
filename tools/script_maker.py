import os

# Set the directory for where target sounds are located
sounds_path = 'Vowels'

# Creates a list of filenames contained within the sounds path 
vowels = os.listdir(sounds_path)

# Print the list of vowels
print(vowels)

# Specify the Genetic Algorithm parameters
no_of_runs = 1
gen_size = '4'
pop_size = '10'
mutationrate = '0.2'
standard_dev = '0.2'
selection = 'linear'

# specify fitness type ['formant' or 'filterbank']
fitnesstype = 'filterbank'

GA_PARAMS = '-gs={} -ps={} -mr={} -sd={} -ft={}'.format(gen_size,
                                                        pop_size,
                                                        mutationrate,
                                                        standard_dev,
                                                        fitnesstype)

prefix = 'python main.py'

########################################################################
# Options for formant based fitness function

# choose from ["hz", "mel", "cents", "bark", "erb", "brito"]
features = ["hz"]# "mel", "cents", "bark", "erb", "brito"]

# choose from ["SSD", "SAD", "EUC", "MSE", "MAE"]
distance_metrics = ["SSD"] # "SAD" "EUC", "MSE", "MAE"]

# choose from ["both", "rms", "intensity", "none"]
loudness = ["none"] #  "both", "rms", "intensity", "none"]

#########################################################################
# options for filterbank fitness function

# choose from ["mfcc_average", "logfbank_average", "mfcc_sad", "mfcc_ssd", "logfbank_sad", "logfbank_ssd"]
filterbank_type = ["mfcc_average", "logfbank_average", "mfcc_sad", "mfcc_ssd", "logfbank_sad", "logfbank_ssd"]

#########################################################################

if fitnesstype == 'formant':
    for vowel in vowels:
        for f in features:
            if f == 'brito':
                for l in loudness:
                    for n in range(no_of_runs):
                        with open('batch.cmd', 'a') as t:
                            t.write("{} {} {} -fr={} -lm={} -id={!s} \n".format(prefix,
                                                                    vowel,
                                                                    GA_PARAMS,
                                                                    f,
                                                                    l,
                                                                    n))
            else:
                for d in distance_metrics:
                    for l in loudness:
                        for n in range(no_of_runs):
                            with open('batch.cmd', 'a') as t:
                                t.write("{} {} {} -fr={} -dm={} -lm={} -id={!s} \n".format(prefix,
                                                                        vowel,
                                                                        GA_PARAMS,
                                                                        f,
                                                                        d,
                                                                        l,
                                                                        n))
elif fitnesstype == 'filterbank':
    for vowel in vowels:
        for f in filterbank_type:
            for n in range(no_of_runs):
                with open('batch.cmd', 'a') as t:                      
                    t.write("{} {} {} -fb={} -id={!s} \n".format(prefix,
                                                         vowel,
                                                         GA_PARAMS,
                                                         f,
                                                         n))

# Add optional arguments here