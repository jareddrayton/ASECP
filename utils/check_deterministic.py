import hashlib
import random
import subprocess
import os

import matplotlib.pyplot as plt
import pandas as pd
import parselmouth
import seaborn as sns

from scipy.io import wavfile


praat_params = [('Interarytenoid', -1.0, 1.0),
                ('Cricothyroid', -1.0, 1.0),
                ('Vocalis', -1.0, 1.0),
                ('Thyroarytenoid', -1.0, 1.0),
                ('PosteriorCricoarytenoid', -1.0, 1.0),
                ('LateralCricoarytenoid', -1.0, 1.0),
                ('Stylohyoid', -1.0, 1.0),
                ('Sternohyoid', -1.0, 1.0),
                ('Thyropharyngeus', -1.0, 1.0),
                ('LowerConstrictor', -1.0, 1.0),
                ('MiddleConstrictor', -1.0, 1.0),
                ('UpperConstrictor', -1.0, 1.0),
                ('Sphincter', -1.0, 1.0),
                ('Hyoglossus', -1.0, 1.0),
                ('Styloglossus', -1.0, 1.0),
                ('Genioglossus', -1.0, 1.0),
                ('UpperTongue', -1.0, 1.0),
                ('LowerTongue', -1.0, 1.0),
                ('TransverseTongue', -1.0, 1.0),
                ('VerticalTongue', -1.0, 1.0),
                ('Risorius', -1.0, 1.0),
                ('OrbicularisOris', -1.0, 1.0),
                ('TensorPalatini', -1.0, 1.0),
                ('Masseter', -1.0, 1.0),
                ('Mylohyoid', -1.0, 1.0),
                ('LateralPterygoid', -1.0, 1.0),
                ('Buccinator', -1.0, 1.0)]


def write_artword(identifier, start_values):

    with open('Individual_{!s}.praat'.format(identifier), 'w') as artword:

        length = 1.5
        # Configure speaker type and sound length
        artword.write('Create Speaker... Robovox Male 2\n')
        artword.write('Create Artword... Individual_{} {}\n'.format(identifier, length))

        # Specify Lungs and LevatorPalatini parameter values
        artword.write('Set target... 0.00  0.20  Lungs\n')
        artword.write('Set target... 0.10  0.00  Lungs\n')
        artword.write('Set target... {}  0.0  Lungs\n'.format(length))
        artword.write('Set target... 0.00  1 LevatorPalatini\n')
        artword.write('Set target... {}  1 LevatorPalatini\n'.format(length))

        # Loop through the parameters and values lists and write these to the artword
        for i in range(len(praat_params)):
            artword.write('Set target... 0.0 {} {}\n'.format(start_values[i], praat_params[i][0]))
            artword.write('Set target... {} {} {}\n'.format(length, start_values[i], praat_params[i][0]))

        # Set sample rate and synthesise audio
        artword.write('select Artword Individual_{}\n'.format(identifier))
        artword.write('plus Speaker Robovox\n')
        artword.write('To Sound... {} 25    0 0 0    0 0 0   0 0 0\n'.format(10025))
        artword.write('''nowarn do ("Save as WAV file...", "Individual_{}.wav")\n'''.format(identifier))


def run_praat(praat_path, script_name):
    subprocess.call([praat_path,
                     '--run',
                     '--ansi',
                     script_name], stdout=subprocess.DEVNULL)


def synthesise_words(praat_path, praat_type, iterations=8):
    import time
    a = time.time()
    for i in range(0, iterations):
        name = f'Individual_{i}_{praat_type}'
        write_artword(f"{i}_Y", values)
        run_praat(praat_path, f'Individual_{i}_Y.praat')
        _, wav_data = wavfile.read(f'Individual_{i}_Y.wav')
        print(hashlib.md5(wav_data).hexdigest())
        snd = parselmouth.Sound(f'Individual_{i}_Y.wav')
        data["Name"].append(name)
        data["F1"].append(snd.to_formant_burg().get_value_at_time(1, 0.75))
        data["F2"].append(snd.to_formant_burg().get_value_at_time(2, 0.75))
        data["F3"].append(snd.to_formant_burg().get_value_at_time(3, 0.75))
        data["praat_type"].append(praat_type)
        os.remove(f'Individual_{i}_Y.wav')
        os.remove(f'Individual_{i}_Y.praat')
    b = time.time()
    print(b-a)


random.seed(1023)

values = [round(random.uniform(y, z), 2) for _, y, z in praat_params]

data = {"Name": [], "F1": [], "F2": [], "F3": [], "praat_type": []}

synthesise_words('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\synthesisers\\praat\\praat', 'deterministic')
synthesise_words('C:\\Users\\Jazz\\Desktop\\praat', 'non-deterministic')

data = pd.DataFrame(data)
data = data.melt(id_vars=["praat_type", "Name"])

# Seaborn plotting based on this example https://seaborn.pydata.org/examples/grouped_barplot.html
sns.set_theme(style="whitegrid")

g = sns.catplot(
    data=data, kind="bar",
    x="variable", y="value", hue="praat_type",
    ci="sd", palette="dark", alpha=.6, height=6, legend_out=False
)

g.despine(left=True)
g.set_axis_labels("Formant", "Formant Frequency in Hz")
g.legend.set_title("")

plt.show()
