import csv
import numpy as np
import subprocess
import pathlib

def write_formant_table(file_path, name):

    praat_script = file_path / 'Individual{}.praat'.format(name)
    audio_file = file_path / 'Individual{}.wav'.format(name)
    formant_table = file_path / 'Individual{}.Table'.format(name)
        
    with open(praat_script, 'w') as f:
        f.write('Read from file: "{}"\n'.format(audio_file))
        f.write('To Formant (sl): 0, 5, 4500, 0.025, 50\n')
        f.write('Down to Table: "no", "no", 6, "no", 3, "yes", 1, "no"\n')
        f.write('Save as comma-separated file: "{}"\n'.format(formant_table))
    
    print(pathlib.Path.cwd())
    
    run_praat_command(praat_script)



def run_praat_command(praat_script):
    subprocess.call(['./praat',
                     '--run',
                     '--ansi',
                     praat_script], stdout=subprocess.DEVNULL)


a = pathlib.Path.cwd().parent / 'target_sounds'
write_formant_table(a, '1')




def get_formants(file_path):
    
    data = []

    with open(file_path, 'r') as f:
        formant_table = csv.reader(f)
        for row in formant_table:
            data.append(row)

    formant_dict = {'F1': [], 'F2': [], 'F3': [], 'F4': [], 'F5': []}

    data = data[1:]

    f1 = [float(x[1]) if x[1] != '--undefined--' else None for x in data]
    f2 = [float(x[2]) if x[2] != '--undefined--' else None for x in data]
    f3 = [float(x[3]) if x[3] != '--undefined--' else None for x in data]
    f4 = [float(x[4]) if x[4] != '--undefined--' else None for x in data]
    f5 = [float(x[5]) if x[5] != '--undefined--' else None for x in data]

    formants = [f1, f2, f3, f4, f5]

    for key in formant_dict.keys():
        formant_dict[key] = []

    forms = []

    for f in formants:
        print('Per ', 100 * (1 - f.count(None) / len(f)))
        print('Mean', np.mean([x for x in f if x != None]))
        print('Std ', np.std([x for x in f if x != None]))
        print('')
        forms.append(np.mean([x for x in f if x != None]))

    return forms

get_formants('Individual3.Table')
