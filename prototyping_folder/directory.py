import glob
import pathlib
import subprocess

data_folder = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data'

print(pathlib.Path.cwd())

pr = pathlib.Path.cwd().parent / 'praat'
p = pathlib.Path.cwd().parent / 'data'
print(p)

print('{}\\Primary8.wav.Gen5.Pop20.Mut0.05.Sd0.1.hz SSD none 2/Generation{!s}/Individual{!s}.praat'.format(p, '4', '4'))

subprocess.call(['{}/praat'.format(pr), 
                         '--run',
                         #'--ansi',
                         '{}\\Primary8.wav.Gen5.Pop20.Mut0.05.Sd0.1.hz SSD none 2/Generation{!s}/Individual{!s}.praat'.format(p, '4', '4')]) #stdout=subprocess.DEVNULL)