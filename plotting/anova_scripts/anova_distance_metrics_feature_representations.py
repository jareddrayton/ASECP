import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from CONSTANTS import target_vowel_data

# target_vowel_data = {'Primary1.wav': [277, 1947, 2629],
#                      'Primary4.wav': [639, 1145, 2195],
#                      'Primary8.wav': [335, 936, 2200]}

glob_string = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\distance_metric_feature_representation\\Primary*'
paths = glob.glob(glob_string)

columns = ['vowel', 'run', 'dm', 'fr', 'f1', 'f2', 'f3']
type = "cen"
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
    dm = arguments['distance_metric']
    fr = arguments["formant_repr"]

    with open(path + f'\\Generation{final_generation}\\individual_info_table.csv', 'r') as f:
        new_data = csv.reader(f, delimiter=' ')

        for i, row in enumerate(new_data):
            if i == best_individual_id:
                best_individual_data = row

    formants_ind = [float(x.strip()) for x in best_individual_data[5:8]]
    if type == "abs":
        formants_abs = list(map(lambda x, y: abs(x-y), formants_ind, target_vowel_data[vowel]))
    elif type == "cen":
        formants_abs = list(map(lambda x, y: x-y, formants_ind, target_vowel_data[vowel]))
    row_data_formatted = [vowel, identifier, dm, fr] + formants_abs

    row_data = dict(zip(columns, row_data_formatted))
    store_rows.append(row_data)


new_df = pd.DataFrame.from_records(store_rows)

def create_plots(new_df):
    formants = ["f1", "f2", "f3"]
    for formant in formants:
        sns.set_theme(style="whitegrid")
        sns.set(font_scale=1.75)
        g = sns.catplot(x="dm", y=formant, hue="fr", col="vowel",
                        errwidth=5.0, capsize=0.3, palette="YlGnBu_d", height=12, aspect=0.4,
                        kind="point", data=new_df, dodge=False)
        g.despine(left=True)

    plt.show()


create_plots(new_df)
