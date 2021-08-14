# scan through folder of runs.
# extract list of the best sounds from last generation of each run
# generate html
import pathlib


path = pathlib.Path('C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\test')

print(path)

sounds = ['Primary1.wav', 'Primary2.wav', 'Primary3.wav']
target_sounds = pathlib.Path.cwd().parent  / 'target_sounds'



runs = list(path.glob('*'))

new_dict = {key : [] for key in sounds}

for sound in sounds:
    print(sound)
    for run in runs:
        if sound in str(run):
            print(new_dict[sound], 'yelp')
            with open(run/ 'Best.txt', 'r') as f:
                new_dict[sound].append((run, f.readlines()[-1].strip()))


print(new_dict)

        
print()
print(new_dict)

def build_html():
    '''
    <tr>
      <th>Target Sound</th>
      <th>run1</th>
      <th>run2</th>
      <th>run3</th>
      <th>run4</th>
      <th>run5</th>
      <th>run6</th>
      <th>run7</th>
      <th>run7</th>
    </tr>
    '''