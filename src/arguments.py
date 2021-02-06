import argparse

def get_user_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-sf", "--soundfile",
                        type=str,
                        default='Primary8.wav',
                        help="sets the filename of the target sound",
                        metavar='')

    parser.add_argument("-ps", "--population_size",
                        type=int,
                        default=20,
                        help="sets the population size",
                        metavar='')

    parser.add_argument("-gs", "--generation_size",
                        type=int,
                        default=2,
                        help="sets the number of generations",
                        metavar='')

    parser.add_argument("-sl", "--selection_type",
                        type=str,
                        default='exponential',
                        help="use to specify GA selection_type type. Choose from 'linear', 'proportional', and 'exponential'",
                        metavar='')

    parser.add_argument("-cr", "--crossover_type",
                        type=str,
                        default="uniform",
                        help="type of crossover for combining genotypes. Choose from 'one_point' or 'uniform'",
                        metavar='')

    parser.add_argument("-mr", "--mutation_rate",
                        type=float,
                        default=0.05,
                        help="sets the rate of mutation",
                        metavar='')

    parser.add_argument("-sd", "--mutation_standard_dev",
                        type=float,
                        default=0.1,
                        help="sets the gaussian distrubutions standard deviation used for mutation",
                        metavar='')

    parser.add_argument("-el", "--elitism",
                        type=bool,
                        default=True,
                        help="Activate the elitism genetic operator",
                        metavar='')

    parser.add_argument("-es", "--elite_size",
                        type=int,
                        default=2,
                        help="Specify number of elite individuals to be kept",
                        metavar='')

    parser.add_argument("-ru", "--runs",
                        type=int,
                        default=10,
                        help="How many repeats of an experiment",
                        metavar='')

    parser.add_argument("-ft", "--fitness_type",
                        type=str,
                        default='formant',
                        help="choose between formant or filterbank",
                        metavar='')

    parser.add_argument("-nf", "--formant_range",
                        type=int,
                        default=3,
                        help="sets the number of formants used for analysis",
                        metavar='')

    parser.add_argument("-fr", "--formant_repr",
                        type=str,
                        default='hz',
                        help="Choose the type of formant fitness function",
                        metavar='')

    parser.add_argument("-dm", "--distance_metric",
                        type=str,
                        default='SSD',
                        help="Choose the type of distance distance_metrics",
                        metavar='')

    parser.add_argument("-lm", "--loudness_measure",
                        type=str,
                        default='none',
                        help="Choose the type of loudness co-efficent",
                        metavar='')

    parser.add_argument("-fb", "--filterbank_type",
                        type=str,
                        default='mfcc_average',
                        help="Choose the type of formant fitness function",
                        metavar='')

    parser.add_argument("-id", "--identifier",
                        type=str,
                        default='2',
                        help="used as random() seed",
                        metavar='')

    parser.add_argument("-pl", "--parallel",
                        type=bool,
                        default=True,
                        help="Flag to enable multiple praat processes. Set to TRUE by default.",
                        metavar='')

    parser.add_argument("-cntk", "--cntk",
                        type=bool,
                        default=False,
                        help="write data to a csv file for use with the CNTK machine learning library",
                        metavar='')
    
    return parser.parse_args()