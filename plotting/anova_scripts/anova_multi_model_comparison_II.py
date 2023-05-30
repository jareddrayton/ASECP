import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from CONSTANTS import target_vowel_data

glob_string_i = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_i\\multi_model_comparison\\Primary*.wav.PRT*'
glob_string_ii = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\multi_model_comparison\\Primary*.wav.PRT*'

columns = ['vowel', 'run', 'mk', 'f1', 'f2', 'f3']

# A list to store each dictioniary that represents a row.
store_rows = []


def add_rows(glob_string, mk):
    paths = glob.glob(glob_string)
    for path in paths:
        # read best
        with open(path + '\\Best.txt', 'r') as f:
            best_individual_id = int(f.readlines()[-1])

        with open(path + '\\arguments.json', 'r') as f:
            arguments = json.loads(f.read())

        final_generation = arguments['generation_size']
        vowel = arguments['soundfile']
        identifier = arguments['identifier']
        synthesiser = mk

        with open(path + f'\\Generation{final_generation}\\individual_info_table.csv', 'r') as f:
            new_data = csv.reader(f, delimiter=' ')

            for i, row in enumerate(new_data):
                if i == best_individual_id:
                    best_individual_data = row

        formants_ind = [float(x.strip()) for x in best_individual_data[5:8]]
        formants_abs = list(map(lambda x, y: x-y, formants_ind, target_vowel_data[vowel][:3]))
        row_data_formatted = [vowel, identifier, synthesiser] + formants_abs

        row_data = dict(zip(columns, row_data_formatted))

        store_rows.append(row_data)


for gs, mk in [(glob_string_i, "i"), (glob_string_ii, "ii")]:
    add_rows(gs, mk)

new_df = pd.DataFrame.from_records(store_rows)


def create_plots(new_df):
    formants = ["f1", "f2", "f3"]
    for formant in formants:
        sns.set_theme(style="whitegrid")
        sns.set(font_scale=1.75, rc={"lines.linewidth": 3.4})
        g = sns.catplot(x="vowel", y=formant,  hue="mk",
                        capsize=0.8, palette="YlGnBu_d",
                        kind="point", data=new_df, join=False, dodge=True, height=10, aspect=2.0, s=15)
        g.despine(left=True)

        plt.show()


create_plots(new_df)
