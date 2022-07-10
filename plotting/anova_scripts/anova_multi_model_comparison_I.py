import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from CONSTANTS import target_vowel_data

glob_string = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\multi_model_comparison_phase_i\\Primary*'
paths = glob.glob(glob_string)

columns = ['vowel', 'run', 'synthesiser', 'f1', 'f2', 'f3']

# A list to store each dictioniary that represents a row.
store_rows = []

for path in paths:
    # read best
    with open(path + '\\Best.txt', 'r') as f:
        best_individual_id = int(f.readlines()[-1])

    with open(path + '\\arguments.json', 'r') as f:
        arguments = json.loads(f.read())

    final_generation = arguments['generation_size']
    vowel = arguments['soundfile']
    identifier = arguments['identifier']
    synthesiser = arguments['synthesiser']

    with open(path + f'\\Generation{final_generation}\\individual_info_table.csv', 'r') as f:
        new_data = csv.reader(f, delimiter=' ')

        for i, row in enumerate(new_data):
            if i == best_individual_id:
                best_individual_data = row

    formants_ind = [float(x.strip()) for x in best_individual_data[5:8]]
    formants_abs = list(map(lambda x, y: abs(x-y), formants_ind, target_vowel_data[vowel][:3]))
    row_data_formatted = [vowel, identifier, synthesiser] + formants_abs

    row_data = dict(zip(columns, row_data_formatted))

    store_rows.append(row_data)


new_df = pd.DataFrame.from_records(store_rows)


sns.set_theme(style="whitegrid")
sns.set(font_scale=1.75)
g = sns.catplot(x="vowel", y='f3',  hue="synthesiser",
                capsize=0.8, palette="YlGnBu_d",
                kind="point", data=new_df, join=False, dodge=True, height=10, aspect=2.0)
g.despine(left=True)

plt.show()
