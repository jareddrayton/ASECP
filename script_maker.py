import os
import itertools

# scan this directory for sounds
path = 'vowels'

# creates a list containing the filenames contained in the given 
vowels = os.listdir(path)

# print(vowels)


# identify number of formants from each 


# choose from hz, mel, cents, bark, erb, brito
features = ["hz", "mel"]  # "cents", "bark", "erb", "brito"]

# choose from "SSD", "SAD", "EUC"
distance_metrics = ["SSD"]

# choose from "both", "rms", "intensity",
loudness = ["both"]

# specify the ga parameters

no_of_runs = 2

gen_size = '4 '
pop_size = '10 '
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
