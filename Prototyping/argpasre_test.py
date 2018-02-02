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

parser.add_argument()

parser.add_argument("-pl","--parallel", 
					type=bool,
					default=True,
					help="used to enable multiple praat processes")



args = parser.parse_args()

soundfile = args.soundfile
populationsize = args.populationsize
generations = args.generations + 1


print(type(args.soundfile))
print(args.soundfile)
print(type(soundfile))
print(soundfile)

print(generations)



