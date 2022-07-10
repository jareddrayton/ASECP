import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

target_vowel_data = {'Primary1.wav': [277, 1947, 2629],
                     'Primary4.wav': [639, 1145, 2195],
                     'Primary8.wav': [335, 936, 2200]}

glob_string = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\no_elitism\\Primary*'
paths = glob.glob(glob_string)

glob_string2 = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\distance_metric_feature_representation\\Primary*.wav.PRT.Gen20.Pop150.Mut0.1.Sd0.2.cent.EUC*'
paths2 = glob.glob(glob_string2)

paths += paths2


columns = ['vowel', 'run', 'el', 'formant', 'frequency']

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
    el = arguments['elitism']

    with open(path + f'\\Generation{final_generation}\\individual_info_table.csv', 'r') as f:
        new_data = csv.reader(f, delimiter=' ')

        for i, row in enumerate(new_data):
            if i == best_individual_id:
                best_individual_data = row

    formants_ind = [float(x.strip()) for x in best_individual_data[5:8]]
    formants_abs = list(map(lambda x, y: abs(x-y), formants_ind, target_vowel_data[vowel]))
    row_data_formatted = [vowel, identifier, el]
    formants = ['f1', 'f2', 'f3']
    for label, value in zip(formants, formants_abs):
        row_data = dict(zip(columns, row_data_formatted + [label, value]))
        store_rows.append(row_data)


new_df = pd.DataFrame.from_records(store_rows)


sns.set_theme(style="whitegrid")
sns.set(font_scale=1.75)
g = sns.catplot(x="vowel", y='frequency',  hue="el", col="formant",
                capsize=.2, palette="YlGnBu_d", height=20, aspect=0.4,
                kind="point", data=new_df, dodge=False)
g.despine(left=True)

plt.show()
