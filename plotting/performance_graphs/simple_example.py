import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib.pyplot as plt

data = pd.read_csv('mock_data.csv', delimiter=',')

sns.set_theme()
sns.lineplot(data=data, x='gen', y='meanfitness', hue='fitness')
plt.xticks(np.arange(0, 5, 1))
plt.show()