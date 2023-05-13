import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from CONSTANTS import target_vowel_data

glob_string_1 = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_i\\distance_metric_feature_representation\\Primary*.wav.PRT.Gen20.Pop150.Mut0.1.Sd0.2.cent.SAD*'
glob_string_2 = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\selection_operator\\linear\\Primary*'
glob_string_3 = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\selection_operator\\proportional\\Primary*'

paths = []

for glob_string in [glob_string_1, glob_string_2, glob_string_3]:
    paths += glob.glob(glob_string)


columns = ['vowel', 'run', 'sel', 'f1', 'f2', 'f3']
type = "abs"
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
    sel = arguments['selection_type']

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
    row_data_formatted = [vowel, identifier, sel] + formants_abs

    row_data = dict(zip(columns, row_data_formatted))
    store_rows.append(row_data)


new_df = pd.DataFrame.from_records(store_rows)

def create_plots(new_df):
    formants = ["f1", "f2", "f3"]
    for formant in formants:
        sns.set_theme(style="whitegrid")
        sns.set(font_scale=1.75)
        g = sns.catplot(x="sel", y=formant, col="vowel",
                        errwidth=5.0, capsize=0.3, palette="YlGnBu_d", height=14, aspect=0.5,
                        kind="point", data=new_df, dodge=False)
        g.despine(left=True)

    plt.show()


create_plots(new_df)
