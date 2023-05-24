# build a html table for a particular experiment
# scan through folder of runs.
# extract list of the best sounds from last generation of each run
# generate html

import shutil
from pathlib import Path

path = Path('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\test')
glob = ""
sounds = ['Primary1.wav', 'Primary4.wav', 'Primary8.wav']
experiment_name = "SAD_HZ"
run_ids = []


Path(Path.cwd() / experiment_name).mkdir()

breakpoint()

print(path)



shutil.copyfile()

runs = list(path.glob('*'))

new_dict = {key: [] for key in sounds}

for sound in sounds:
    print(sound)
    for run in runs:
        if sound in str(run):
            print(new_dict[sound], 'yelp')
            with open(run / 'Best.txt', 'r') as f:
                new_dict[sound].append((run, f.readlines()[-1].strip()))

print(new_dict)

print()
print(new_dict)

def find_best_individual():
    # given a run find the best individual
    # return the full location of the .wav file
    pass


