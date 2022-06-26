import glob
import os
import sys

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.append('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\src')

from praat_control import run_praat_command

glob_string = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\target_sounds\\*.wav'
target_sounds = glob.glob(glob_string)

ceiling = 4750


def table_to_long_form_df(table_name, algo):
    table = pd.read_csv(table_name, delimiter='\t')
    table = pd.melt(table, id_vars=['time(s)'], value_name='Formants', value_vars=['F1(Hz)', 'F2(Hz)', 'F3(Hz)', 'F4(Hz)', 'F5(Hz)'])
    table = table.replace(to_replace="--undefined--",)
    table['algorithm'] = algo
    return table


for target_sound in target_sounds:
    sound_name = os.path.basename(target_sound).split('.')[0]
    algorithms = ['burg', 'sl']
    data_frames = []
    for algo in algorithms:
        table_path = f"{sound_name}_{algo}.Table"
        with open('praat_script.praat', 'w') as f:
            f.write(f'Read from file: "{target_sound}"\n')
            f.write(f'To Formant ({algo}): 0, 5, {ceiling}, 0.025, 50\n')
            f.write('Down to Table: "no", "yes", 4, "no", 3, "yes", 3, "no"\n')
            f.write(f'Save as tab-separated file: "{table_path}"')

        run_praat_command('praat_script.praat', purge=True)

        data_frames.append(table_to_long_form_df(table_path, algo))
        os.remove(table_path)

    new_table = pd.concat(data_frames)

    sns.set(font_scale=1.4)
    sns.set_palette(sns.dark_palette('Blue'))
    sns.relplot(data=new_table, x="time(s)", y="Formants", hue="variable", col="algorithm", kind="line")

    plt.ylim(0, ceiling)

    plt.savefig(f'figures\\burg_vs_sl_{sound_name}_{ceiling}.pdf')
