import csv

###################################################################################################
###################################################################################################

def write_formants(name, directory, currentgeneration, individualfrequencies, fitness, voiced):
    csvdata = list(individualfrequencies)
    csvdata.append(fitness)
    csvdata.append(voiced)

    with open('{}/Generation{!s}/Stats.csv'.format(directory, currentgeneration), 'a') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(csvdata)
