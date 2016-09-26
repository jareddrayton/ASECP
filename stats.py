import csv
import matplotlib.pyplot as plt
from numpy.random import rand


def performance_graph():
	""" Generate a performance Graph of a run """

	pass

def performance_graph_animated():
	""" Generate an animated performance graph """

	pass

#################################################################################################################
#################################################################################################################

def formant_single_plot():
	""" Plots the F1 and F2 information of the individuals """

	directorya = "Target[a].wav Gen 20 Pop 75 Mut 0.15 SD 0.15 B3 EUC 04"
	directoryu = "Target[u].wav Gen 20 Pop 75 Mut 0.15 SD 0.15 B3 EUC 04"
	
	scale = 60

	with open('%s\\Generation20\\Stats.csv' % directorya, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
		for row in spamreader:
			plt.scatter(row[1],row[2], c="red", s=scale, alpha=0.3, edgecolors='none')

	with open('%s\\Generation20\\Stats.csv' % directoryu, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
	
		for row in spamreader:
			plt.scatter(row[1],row[2], c="blue", s=scale, alpha=0.3, edgecolors='none')


	plt.scatter(784, 1211, c="red", s=scale, label = "[a]", marker=">", alpha=1.0, edgecolors='none')
	plt.annotate("Target[a]", (805,1211))

	plt.scatter(295,750, c="blue", s=scale, label = "[u]", marker="<", alpha=1.0, edgecolors='none')
	plt.annotate("Target[u]", (305,750))

	plt.axis([200, 900, 400, 2400])
	plt.xlabel('F1 Hz')
	plt.ylabel('F2 Hz')
	
	plt.title("Generation 20")
	plt.legend()
	plt.grid(True)
	plt.savefig("Formant Plots 04 Single\\B3_EUC_04.pdf",format='pdf')
	plt.savefig("Formant Plots 04 Single\\B3_EUC_04.png",format='png')
	#plt.show()

def formant_plot_animated():
	""" Plot an animated formant plot """

	pass


def write_formants(name, directory, currentgeneration, individualfrequencies, fitness, voiced):

	
	csvdata = individualfrequencies
	csvdata.append(fitness)
	csvdata.append(voiced)
	print(csvdata)

	with open('%s\\Generation%d\\Stats.csv' % (directory, currentgeneration), 'a') as csvfile:
	
		spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(csvdata)


#################################################################################################################
#################################################################################################################

def probability_distrubution():
	pass



#################################################################################################################
#################################################################################################################
