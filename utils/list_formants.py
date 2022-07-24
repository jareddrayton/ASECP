import pandas as pd
import glob
import sys
import os.path
import pathlib

sys.path.append('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\src')

from praat_control import write_target_formant_table

input_folder = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\target_sounds\\*.wav'

empty_dict = {}

for path in glob.glob(input_folder):
    print(os.path.basename(path))
    print(os.path.dirname(path))

    formants = write_target_formant_table(pathlib.Path(os.path.dirname(path)), os.path.basename(path))

    formants = [str(round(x)) if x else None for x in formants]
    print(formants)
    empty_dict[os.path.basename(path)] = formants


print(pd.DataFrame(empty_dict).add(' hz').T.to_latex())
