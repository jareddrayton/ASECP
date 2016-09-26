import csv
import matplotlib.pyplot as plt
from matplotlib import animation

def performance_graph():
	""" Generate a performance Graph of a run """

	pass

def performance_graph_animated():
	""" Generate an animated performance graph """

	pass

#################################################################################################################
#################################################################################################################
# Static F1/F2 Plots

metric = "EUC"
ff = "A1"

def read_all_csv(vowel,color):
	
	scale = 60

	for i in range(1,6):
		directory = ("vowel-%s.wav Gen 20 Pop 75 Mut 0.15 SD 0.15 %s %s 0%d" % (vowel, ff, metric, i))
		with open('%s\\Generation20\\Stats.csv' % directory, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
			for row in spamreader:
				plt.scatter(row[0],row[1], c=color, s=scale, alpha=0.5, edgecolors='none')

def formant_all_plot():
	""" Plots the F1 and F2 information of all individuals of a given generation from n runs"""
	
	generation = "20"
	
	vowels =[("e","steelblue"),("o","lightgreen"),("a","darkred")]

	scale = 100

	for s in vowels:
		read_all_csv(*s)

	plt.scatter(760, 1179, c="darkred", s=scale, label = "[a]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[a]", (760,1179))

	plt.scatter(519,830, c="lightgreen", s=scale, label = "[o]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[o]", (519,830))

	plt.scatter(319,1944, c="steelblue", s=scale, label = "[e]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[e]", (319,1944))

	plt.axis([200, 900, 400, 2400])
	
	plt.xlabel('F1 Hz')
	plt.ylabel('F2 Hz')
	
	plt.title("Generation %s" % generation)
	plt.legend()
	plt.grid(True)
	plt.savefig(("%s_%s_All.pdf" % (ff,metric)), format='pdf')
	plt.clf()

formant_all_plot()


def read_average_csv(vowel,color):
	
	scale = 100

	for i in range(1,6):
		
		f1 = []
		f2 = []

		directory = ("vowel-%s.wav Gen 20 Pop 75 Mut 0.15 SD 0.15 %s %s 0%d" % (vowel, ff, metric, i))
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


def formant_average_plot():
	""" Plots the F1 and F2 information of all individuals of a given 
	generation from n runs"""
	
	generation = "20"
	
	vowels =[("e","steelblue"),("o","lightgreen"),("a","darkred")]

	scale = 100

	for s in vowels:
		read_average_csv(*s)

	plt.scatter(760, 1179, c="darkred", s=scale, label = "[a]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[a]", (760,1179))

	plt.scatter(519,830, c="lightgreen", s=scale, label = "[o]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[o]", (519,830))

	plt.scatter(319,1944, c="steelblue", s=scale, label = "[e]", marker="o", alpha=1.0, edgecolors='none')
	plt.annotate("Target[e]", (319,1944))

	plt.axis([200, 900, 400, 2400])
	
	plt.xlabel('F1 Hz')
	plt.ylabel('F2 Hz')
	
	plt.title("Generation %s" % generation)
	plt.legend()
	plt.grid(True)
	plt.savefig(("%s_%s_Average.pdf" % (ff,metric)), format='pdf')
	plt.clf()

formant_average_plot()



#################################################################################################################
# barchart



#################################################################################################################
#################################################################################################################
