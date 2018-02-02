import argparse
import configparser

parser = argparse.ArgumentParser()

parser.add_argument("soundfile",
                    type=str,
                    default='Target',
                    help="sets the filename of the target sound")

parser.add_argument("-ps", "--populationsize", 
					type=int,
					default=100,
                    help="sets the population size")

parser.add_argument("-g", "--generations",
					type=int, 
					default=25,
                    help="sets the number of generations")

parser.add_argument("-mr", "--mutationrate",
					type=float, 
					default=0.2,
                    help="sets the rate of mutation")

parser.add_argument("-sd", "--standarddev",
					type=float, 
					default=0.2,
                    help="sets the gaussian standard deviation")

parser.add_argument("-ft", "--fitnesstype",
					type=str,
					default='formant',
					help="choose between formants or filterbanks")

parser.add_argument("-fff", "--ffformants",
					type=str,
					default='hz',
					help="Choose the type of formant fitness function")

parser.add_argument("-dm", "--distancemetric",
					type=str,
					default='SSD',
					help="Choose the type of distance metrics")

parser.add_argument("-lm", "--loudnessmeasure",
					type=str,
					default='rms',
					help="Choose the type of loudness co-efficent")

parser.add_argument("-ffb", "--fffilterbank",
					type=str,
					default='mfcc_average',
					help="Choose the type of formant fitness function")

parser.add_argument("-id", "--identifier", 
					type=str,
					default='01',
					help="used as random() seed")

parser.add_argument("-pl","--parallel", 
					type=bool,
					default=True,
					help="used to enable multiple praat processes")

args = parser.parse_args()

soundfile = args.soundfile
populationsize = args.populationsize
generations = args.generations + 1
mutationrate = args.mutationrate
standarddev = args.standarddev
fitnesstype = args.fitnesstype
ffformants = args.ffformants
metric = args.distancemetric
loudnessmeasure = args.loudnessmeasure
fffilterbank = args.fffilterbank
identifier = args.identifier
parallel = args.parallel
