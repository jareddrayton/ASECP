import csv
import glob
import json

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import imageio

glob_string = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\multi_model_comparison\\Primary*.wav.PRT*'
glob_string_2 = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\pop_gen_size\\Primary*.wav.PRT.Gen40*'

vtl_glob = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\thesis_data\\chapter_5_ii\\multi_model_comparison\\Primary*.wav.VTL*'

prt_paths = sorted(glob.glob(glob_string) + glob.glob(glob_string_2))
vtl_paths = sorted(glob.glob(vtl_glob))

columns = ['vowel', 'run', 'synth', 'f1', 'f2', 'f3']


def add_rows(generation, paths, syn):
    store_rows = []
    for path in paths:
        # read best
        with open(path + '\\Best.txt', 'r') as f:
            best_individual_id = int(f.readlines()[generation])

        with open(path + '\\arguments.json', 'r') as f:
            arguments = json.loads(f.read())

        # generation = arguments['generation_size']
        vowel = arguments['soundfile']
        identifier = arguments['identifier']
        synthesiser = arguments['synthesiser']

        with open(path + f'\\Generation{generation}\\individual_info_table.csv', 'r') as f:
            new_data = csv.reader(f, delimiter=' ')

            for i, row in enumerate(new_data):
                if i == best_individual_id:
                    best_individual_data = row

        formants_ind = [float(x.strip()) for x in best_individual_data[5:8]]
        # formants_abs = list(map(lambda x, y: x-y, formants_ind, target_vowel_data[vowel][:3]))
        row_data_formatted = [vowel, identifier, synthesiser] + formants_ind

        row_data = dict(zip(columns, row_data_formatted))

        store_rows.append(row_data)

    new_df = pd.DataFrame.from_records(store_rows)
    print(new_df)
    create_plots(new_df, generation, syn)


def create_plots(new_df, generation, syn):
    sns.set_theme(style="whitegrid")
    sns.set(font_scale=1.75, rc={
            "lines.linewidth": 3.4, 'figure.figsize': (13.7, 8.27)})

    g = sns.scatterplot(data=new_df, x="f1", y="f2",
                        hue="vowel", palette="deep", s=40)
    sns.move_legend(g, "upper left", bbox_to_anchor=(1, 1))
    g.set_title(f"Generation {generation}")
    plt.ylim(800, 2000)
    plt.xlim(225, 700)
    plt.savefig(f'./frames/img_{syn}_{generation}.png', bbox_inches='tight')
    plt.clf()


def create_gif(syn):
    frames = []
    for t in range(0, 41):
        image = imageio.v2.imread(f'./frames/img_{syn}_{t}.png')
        frames.append(image)

    imageio.mimsave(f'./scatter_{syn}.gif', frames, duration=225, loop=0)


for paths, syn in [(prt_paths, "prt"), (vtl_paths, "vtl")]:
    for generation in range(0, 41):
        add_rows(generation, paths, syn)
    create_gif(syn)
