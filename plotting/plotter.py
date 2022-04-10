import csv, math
import matplotlib.pyplot as plt
from matplotlib import animation


def read_all_csv(metric, ff, vowel, color):
        
    scale = 60

    for i in range(1,6):
        directory = ("vowel-%s-mono.wav Gen 20 Pop 75 Mut 0.15 SD 0.15 %s %s 0%d" % (vowel, ff, metric, i))
        with open('%s\\Generation20\\Stats.csv' % directory, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
            for row in spamreader:
                plt.scatter(row[0],row[1], c=color, s=scale, alpha=0.5, edgecolors='none')

def formant_all_plot(metric, ff):
    """ Plots the F1 and F2 information of all individuals of a given generation from n runs"""
        
    generation = "20"
        
    vowels = [("e","steelblue"),("o","lightgreen"),("a","darkred")]

    scale = 100

    for s in vowels:
        read_all_csv(metric, ff, *s)

    plt.scatter(760, 1179, c="darkred", s=scale, label = "/a/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target[a]", (760,1179))

    plt.scatter(519,830, c="lightgreen", s=scale, label = "/o/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target[o]", (519,830))

    plt.scatter(319,1944, c="steelblue", s=scale, label = "/e/", marker="o", alpha=1.0, edgecolors='none')
    plt.annotate("Target[e]", (319,1944))

    plt.axis([200, 900, 400, 2400])
        
    plt.xlabel('F1 Hz')
    plt.ylabel('F2 Hz')
        
    plt.title("Generation %s" % generation)
    plt.legend()
    plt.grid(True)
    plt.savefig(("%s_%s_All.pdf" % (ff,metric)), format='pdf')
    plt.clf()

###################################################################################################
###################################################################################################
# Scatter Plots

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
        
    generation = "20"
        
    vowels =[("e","steelblue"),("o","lightgreen"),("a","darkred")]

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


###################################################################################################
###################################################################################################
# LaTeX Table Generator


metrics = ["EUC","SAD", "SSD"]
ffs = ["A1", "A2", "A3"]
vowels = ["a", "o", "e"]


def all(metric, ff, vowel):
    # This function outputs a .csv

    VUV_Rate = []
        
    uF1 = []
    uF2 = []
    oF1 = []
    oF2 = []
        
    percentage = []
        
    if vowel == "a":
        freq = (760, 1179)
    elif vowel == "o":
        freq = (519, 830)
    elif vowel == "e":
        freq = (319,1944)

    for i in range(1,6):
        
        directory = ("vowel-%s-mono.wav Gen 20 Pop 75 Mut 0.15 SD 0.15 %s %s 0%d" % (vowel, ff, metric, i))
        
        with open('%s\\Generation20\\Stats.csv' % directory, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        
            for row in spamreader:
                if row[3] == "True":
                    VUV_Rate.append(row[3])
                    uF1.append(float(row[0]))
                    uF2.append(float(row[1]))

    if len(uF1) == 0:
        uF1 = "N/A"
        oF1 = "N/A"
    else:
        for i in range(len(uF1)):
            oF1.append((uF1[i]-freq[0]) ** 2)
        
        oF1 = str(round(math.sqrt(sum(oF1)/len(oF1)),1))
        uF1 = str(round(sum(uF1) / len(uF1), 1))

    if len(uF2) == 0:
        uF2 = "N/A"
        oF2 = "N/A"
    else:
        for i in range(len(uF2)):
            oF2.append((uF2[i]-freq[1]) ** 2)
        
        oF2 = str(round(math.sqrt(sum(oF2)/len(oF2)),1))        
        uF2 = str(round(sum(uF2) / len(uF2), 1))
        
    percentage.append(metric)
    percentage.append(ff)
    percentage.append(vowel)
    percentage.append(round(len(VUV_Rate) / (75.0 * 5.0) * 100, 2))

    with open('all.csv','a') as csvfile:
        
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(percentage)

    if ff == "A1":
        ff = "Hz"
    elif ff == "A2":
        ff = "Mel"
    elif ff == "A3":
        ff = "Cents"

    with open("latex_table.txt", "a") as table:
        table.seek(0, 2)
        table.write("$%s$  & %s & /%s/ & %s & %s & %s & %s & %s\\%%  \\\\ \r\n" % (ff, metric,vowel, 
            uF1, oF1, uF2, oF2, percentage[3]))
        table.close()

for ff in ffs:
    for metric in metrics:
        #formant_average_plot(metric,ff)
        #formant_all_plot(metric,ff)
        for vowel in vowels:
            all(metric, ff, vowel)
