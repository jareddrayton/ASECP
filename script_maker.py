import os

# Set the directory for where target sounds are located
sounds_path = 'Vowels'

# Creates a list of filenames contained within the sounds path 
vowels = os.listdir(sounds_path)

# Print the list of vowels
print(vowels)

# Specify the Genetic Algorithm parameters
no_of_runs = 1
gen_size = '10'
pop_size = '4'
mutationrate = '0.2'
standard_dev = '0.2'
selection = 'linear'

GA_PARAMS = ' -g={} -ps={} -mr={} -sd={}'.format(gen_size,
                                                 pop_size,
                                                 mutationrate,
                                                 standard_dev)

sounds_path = 'python main.py' + GA_PARAMS

print(sounds_path)

# specify fitness type 'formant' or 'filterbank'
fitnesstype = 'formant'

# choose from ["hz", "mel", "cents", "bark", "erb", "brito"]
features = ["cents"]

# choose from ["SSD", "SAD", "EUC", "MSE", "MAE"]
distance_metrics = ["SSD"] # "MSE", "MAE"]

# choose from ["both", "rms", "intensity", "none"]
loudness = ["both"]

# choose mfcc_average, logfbank_average, mfcc_sad, mfcc_ssd, logfbank_sad, logfbank_ssd

for v in vowels:
    for f in features:
        for d in distance_metrics:
            for l in loudness:
                for n in range(no_of_runs):
                    with open('batch.cmd', 'a') as t:
                        t.write("python main.py {!s} {!s} {!s} {!s} {!s}\n".format(v, f, d, l, n))


# choose mfcc_average, logfbank_average, mfcc_sad, mfcc_ssd, logfbank_sad, logfbank_ssd