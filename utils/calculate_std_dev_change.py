from cgi import test
import glob

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

import random

paths = glob.glob('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\new_deterministic\\*')
random.shuffle(paths)

# Dictionary that holds all the best fitness score for every generation and every run.
best_fitness_data = {}

for run, path in enumerate(paths):
    with open(f"{path}\\Minimum.txt", 'r') as f:
        best_fitness_data[f"{run}"] = [float(line.strip()) for line in f.readlines()]

print(best_fitness_data)

# An empty dictionary to iteratively add data to.
store_data = {}

# An empty dictionary to iteratively add data to.
store_std = {}

# Iterate over the input data
for k, v in best_fitness_data.items():
    # add the run data to the store dictionary loop by loop
    store_data[k] = v
    # create a transposed data frame of the data collated so far,
    df = pd.DataFrame(store_data).T

    # create an empty list to store standar deviation calculations
    store_std[k] = []

    # iterate over the columns which should be generations
    for i in df.columns:
        # for each generation store the standard deviation for that generation
        store_std[k].append(df[i].std())

# Generate a latex table
print(pd.DataFrame(store_std).T.pct_change().iloc[:, range(0, 24, 4)].round(3).to_latex(caption='Percentage change in the standard deviation as the number of runs increases.'))

# Create a plot of the standard
#  deviation of generations 20 as the number of runs increases.
sns.set_theme(style="darkgrid")
sns.set(rc={'figure.figsize': (16, 8)}, font_scale=1.75)
sns.lineplot(data=pd.DataFrame(store_std).T.iloc[:, 20])
plt.savefig("std_chg.pdf", bbox_inches='tight', height=4, aspect=2)
plt.show()
plt.clf()


def sample(input_data, n_bootstrapped):
    # get the best fitness for each run from generation 20
    last_gen_fitness = pd.DataFrame(input_data).T.iloc[:, 20]
    # create a new df to store all the boot strapped samples
    sns.histplot(data=last_gen_fitness, bins=10, kde=True)
    plt.show()

    output_df = pd.DataFrame()

    # sample with replacement from the
    for i in range(n_bootstrapped):
        output_df[f"sample_{i}"] = last_gen_fitness.sample(frac=1, replace=True).reset_index(drop=True)

    # output_df['idd'] = 'experiment'
    # output_df = output_df.melt(id_vars='idd')
    # sns.histplot(data=output_df, bins=10, kde=True)
    # sns.kdeplot(data=output_df)
    # plt.show()
    # store the boot strapped samples as a dictionary
    store_new_std = output_df.T.to_dict(orient='list')

    store_data = {}
    store_std = {}
    for k, v in store_new_std.items():
        store_data[k] = v
        al = pd.DataFrame(store_data).T

        store_std[k] = []
        for i in al.columns:
            store_std[k].append(al[i].std())

    return pd.DataFrame(store_std)


# bootstrapped std deviations of final generation
test_example = sample(store_data, 50)


sns.lineplot(data=test_example.T, legend=False)
plt.savefig("bootstrapped_std_chg.pdf", bbox_inches='tight', height=4, aspect=2)
plt.show()
plt.clf()

test_example_b = sample(store_data, 2000)

test_example_b = test_example_b.iloc[:, 1:]

test_example_b['idd'] = 'experiment'
test_example_b = test_example_b.melt(id_vars='idd')


sns.lineplot(x='variable', y='value', data=test_example_b, err_style='bars', ci=95)
plt.savefig("mean_of_bootstrapped_std_chg.pdf", bbox_inches='tight', height=4, aspect=2)
plt.show()
plt.clf()
