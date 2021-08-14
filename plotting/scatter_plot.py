import os
import csv

import matplotlib.pyplot as plt

# root_directory = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_feature_weighting'
# root_directory = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\comparison_of_feature_transformations'

root_directory = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\thesis_data\\effect_of_selection_operator'

file_paths = os.listdir(root_directory)

metrics = ['SSD'] #['EUC', 'SSD', 'SAD']

metrics2 = ['bark', 'mel', 'cent']

sounds = set([x.split('.wav')[0] for x in file_paths])

target_formants = {'Primary1': (274, 1947, 'steelblue'),
                   'Primary4': (639, 1145, 'lightgreen'),
                   'Primary8': (335, 936, 'darkred')}


def read_all(direcs, metric, color):
    
    scale = 20
    f1 = []
    f2 = []
    print(direcs)
    for directory in direcs:
        print(directory)
        

        with open('{}\\{}\\Generation20\\individual_info_table.csv'.format(root_directory, directory), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
            for row in spamreader:
                if row[-4] == "True":
                    f1.append(float(row[5]))
                    f2.append(float(row[6]))
            
            if len(f1) == 0:
                f1.append(1)
                f2.append(1)
            #a = sum(f1)/len(f1)
            #b = sum(f2)/len(f2)
    print(len(f1))
    plt.scatter(f1,f2, c=color, s=scale, alpha=1, marker="o", edgecolors='none')


def read_average(direcs, metric, color):
    
    scale = 50
    
    print(direcs)
    for directory in direcs:
        print(directory)
        f1 = []
        f2 = []

        with open('{}\\{}\\Generation20\\individual_info_table.csv'.format(root_directory, directory), 'r') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
            for row in spamreader:
                if row[-4] == "True":
                    f1.append(float(row[5]))
                    f2.append(float(row[6]))
            
            if len(f1) == 0:
                f1.append(1)
                f2.append(1)
            a = sum(f1)/len(f1)
            b = sum(f2)/len(f2)

        plt.scatter(a,b, c=color, s=scale, alpha=1, marker="o", edgecolors='none')









def plot_vowel(metric):
    directories = [path for path in file_paths if metric in path]
    
    for sound in sounds:
        new_direcs = [path for path in directories if sound in path]
        color = target_formants[sound][2]
        read_average(new_direcs, metric, color)
    plt.axis([200, 900, 400, 2400])

    for sound in sounds:
        f1, f2, color = target_formants[sound]
        plt.scatter(f1, f2, c=color, s=200, label = sound, marker="*", alpha=1.0, edgecolors='none')
        plt.annotate(sound, (f1, f2))


    plt.xlabel('F1 Hz')
    plt.ylabel('F2 Hz')
    plt.show()

    plt.legend()
    plt.grid(True)
    #plt.savefig(("%s_%s_Average.pdf" % (ff,metric)), format='pdf')
    plt.clf()

    #print(directories)
    print()


def plot_vowel_all(metric):
    directories = [path for path in file_paths if metric in path]
    
    for sound in sounds:
        new_direcs = [path for path in directories if sound in path]
        color = target_formants[sound][2]
        read_all(new_direcs, metric, color)
    plt.axis([200, 900, 400, 2400])

    for sound in sounds:
        f1, f2, color = target_formants[sound]
        plt.scatter(f1, f2, c=color, s=200, label = sound, marker="*", alpha=1.0, edgecolors='none')
        plt.annotate(sound, (f1, f2))

    plt.xlabel('F1 Hz')
    plt.ylabel('F2 Hz')
    plt.show()

    #print(directories)
    print()



for metric in metrics:
    plot_vowel(metric)

for metric in metrics:
    plot_vowel_all(metric)








def read_average_csv(metric, ff, vowel, color):
        
    scale = 100

    for i in range(1,6):
        
        f1 = []
        f2 = []

        directory = ("vowel-%s-mono.wav Gen 20 Pop 75 Mut 0.15 SD 0.15 %s %s 0%d" % (vowel, ff, metric, i))
        with open('%s\\Generation20\\Stats.csv' % directory, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
            for row in spamreader:
                if row[0] == "4000":
                    pass
                else:
                    f1.append(float(row[0]))
                if row[1] == "6000":
                    pass
                else:
                    f2.append(float(row[1]))  
            
            if len(f1) == 0:
                f1.append(1)
                f2.append(1)
            a = sum(f1)/len(f1)
            b = sum(f2)/len(f2)
        
            plt.scatter(a,b, c=color, s=scale, alpha=1, marker="*", edgecolors='none')


def formant_average_plot(metric, ff):
    """ Plots the F1 and F2 information of all individuals of a given 
    generation from n runs"""

    vowels =[("Primary1","steelblue"),("Primary4","lightgreen"),("Primary8","darkred")]

    scale = 100

    for s in vowels:
        read_average_csv(metric, ff, *s)

    plt.scatter(760, 1179, c="darkred", s=scale, label = "/a/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target /a/", (760,1179))

    plt.scatter(519,830, c="lightgreen", s=scale, label = "/o/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target /o/", (519,830))

    plt.scatter(319,1944, c="steelblue", s=scale, label = "/e/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target /e/", (319,1944))

    plt.axis([200, 900, 400, 2400])
        
    plt.xlabel('F1 Hz')
    plt.ylabel('F2 Hz')
        
    plt.title("Generation %s" % generation)
    plt.legend()
    plt.grid(True)
    plt.savefig(("%s_%s_Average.pdf" % (ff,metric)), format='pdf')
    plt.clf()