import csv

#################################################################################################################
#################################################################################################################

def write_formants(name, directory, currentgeneration, individualfrequencies, fitness, voiced):

	
	csvdata = individualfrequencies
	csvdata.append(fitness)
	csvdata.append(voiced)
	print(csvdata)

	with open('%s\\Generation%d\\Stats.csv' % (directory, currentgeneration), 'a') as csvfile:
	
		spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		spamwriter.writerow(csvdata)