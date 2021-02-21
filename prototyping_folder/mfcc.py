import pathlib

from python_speech_features import logfbank, mfcc


import matplotlib.pyplot as plt

import librosa

import librosa.display
import numpy as np


parent_dir = pathlib.Path.cwd().parent

audio_file = parent_dir / 'target_sounds' / 'Primary1.wav'

signal, sr = librosa.load(audio_file)

mfccs = librosa.feature.mfcc(y=signal, n_mfcc=13, sr=sr)

plt.figure(figsize=(10, 4))
librosa.display.specshow(mfccs, 
                         x_axis="time", 
                         sr=sr)
plt.colorbar(format="%+2.f")
plt.show()
print(mfccs)



