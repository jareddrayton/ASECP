import os

# scan this directory for sounds
path = 'Vowels'

# creates a list containing the filenames contained in the given 
vowels = os.listdir(path)

print(vowels)


# identify number of formants from each 


# choose hz, mel, cents, bark, erb, brito,
# choose mfcc_average, logfbank_average, mfcc_sad, mfcc_ssd, logfbank_sad, logfbank_ssd
features = ["cents"]

# choose from "SSD", "SAD", "EUC", "MSE", "MAE"
distance_metrics = ["SSD"] # "MSE", "MAE"]

# choose from "both", "rms", "intensity", "none"
loudness = ["both"]

# specify the ga parameters



no_of_runs = 1
gen_size = '10 '
pop_size = '4 '
mutation = '0.2 '
standard_dev = '0.2'

GA_params = gen_size + pop_size + mutation + standard_dev

for v in vowels:
    for f in features:
        for d in distance_metrics:
            for l in loudness:
                for n in range(no_of_runs):
                    with open('batch.cmd', 'a') as t:
                        t.write("python main.py {!s} {!s} P {!s} {!s} {!s} {!s}\n".format(v, GA_params, f, d, l, n))
