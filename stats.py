import csv

def write_formants(name, directory, currentgeneration, individualfrequencies, fitness, voiced, absolutefitness):
    csvdata = list(individualfrequencies)
    csvdata.append(fitness)
    csvdata.append(voiced)
    csvdata.append(absolutefitness)

    with open('{}/Generation{!s}/Stats.csv'.format(directory, currentgeneration), 'a', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(csvdata)
