from CONSTANTS import PRT_PARAMETER_DEFS
import sklearn
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import explained_variance_score, confusion_matrix, mean_absolute_error, max_error


parameter_data = pd.read_csv('labelled_data_[1][2].txt')

X = parameter_data.iloc[:, 27:]
y = parameter_data.iloc[:, 0:27]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.1)

scaler = StandardScaler()
scaler.fit(X_train)

X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

mlp = MLPRegressor(hidden_layer_sizes=((27 for i in range(10))), max_iter=1000, activation='relu', alpha=0.0001)

mlp.fit(X_train, y_train)

predictions = mlp.predict(X_test)

print(explained_variance_score(y_test, predictions))
print(mean_absolute_error(y_test, predictions))

test = np.array([274, 2300, 3350, 3800, 4500]).reshape(1, -1)

test = scaler.transform(test)

new_predict = mlp.predict(test)

print(new_predict[0])

parameters = PRT_PARAMETER_DEFS['ALL']
target_length = '1.0'

values = new_predict[0]

with open('out_params_to_sound.praat', 'w') as f:

    # Configure speaker type and sound length
    f.write('Create Speaker... Robovox Male 2\n')
    f.write('Create Artword... Individual {}\n'.format(target_length))

    # Specify Lungs and LevatorPalatini parameter values
    f.write('Set target... 0.0  0.1  Lungs\n')
    f.write('Set target... 0.04  0.0  Lungs\n')
    f.write('Set target... {}  0.0  Lungs\n'.format(target_length))
    f.write('Set target... 0.00  1 LevatorPalatini\n')
    f.write('Set target... {}  1 LevatorPalatini\n'.format(target_length))

    # Loop through the parameters and values lists and write these to the artword
    for i in range(len(parameters)):
        #f.seek(0, 2)
        f.write('Set target... 0.0 {} {}\n'.format(values[i], parameters[i][0]))
        f.write('Set target... {} {} {}\n'.format(target_length, values[i], parameters[i][0]))

    # Set sample rate and synthesise audio
    f.write('select Artword Individual\n')
    f.write('plus Speaker Robovox\n')
    f.write('To Sound... 44100 25    0 0 0    0 0 0   0 0 0\n')
    f.write('''nowarn do ("Save as WAV file...", "Individual.wav")\n''')
