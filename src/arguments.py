import argparse


def get_user_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-sf", "--soundfile",
                        type=str,
                        required=True,
                        help="Target sound file name.",
                        metavar='')

    parser.add_argument("--sub_directory",
                        type=str,
                        required=False,
                        default=None,
                        help="Specify optional parent subdirectory for experiment.",
                        metavar='')

    parser.add_argument("-ps", "--population_size",
                        type=int,
                        required=True,
                        help="Sets the population size",
                        metavar='')

    parser.add_argument("-gs", "--generation_size",
                        type=int,
                        required=True,
                        help="Sets the number of generations",
                        metavar='')

    parser.add_argument("-sl", "--selection_type",
                        type=str,
                        default='exponential',
                        help="Specify the selection type used. Choose from 'linear', 'proportional', or 'exponential'",
                        metavar='')

    parser.add_argument("-cr", "--crossover_type",
                        type=str,
                        default="one_point",
                        help="Specify the type of crossover used. Choose from 'one_point' or 'uniform'",
                        metavar='')

    parser.add_argument("-mu", "--mutation_type",
                        type=str,
                        default="gaussian",
                        help="Specify the type of distribution used for mutation. Choose from 'gaussian' or 'uniform'",
                        metavar='')

    parser.add_argument("-mr", "--mutation_rate",
                        type=float,
                        default=0.1,
                        help="Specify the chance of mutation",
                        metavar='')

    parser.add_argument("-sd", "--mutation_standard_dev",
                        type=float,
                        default=0.2,
                        help="sets the gaussian distrubutions standard deviation used for mutation",
                        metavar='')

    parser.add_argument("-el", "--elitism",
                        type=int,
                        default=0,
                        help="Activate elitism and specify number of top individuals to carry over.",
                        metavar='')

    parser.add_argument("-ft", "--fitness_type",
                        type=str,
                        default='formant',
                        help="choose between 'formant' or 'filterbank",
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
                        default='SAD',
                        help="Choose the type of distance distance_metrics",
                        metavar='')

    parser.add_argument("-w", "--weight_features",
                        action='store_true',
                        help="Choose whether formant features are weighted",)

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
                        default='01',
                        help="Used to differentiate runs of the same experiment.",
                        metavar='')

    parser.add_argument("-pl", "--parallel",
                        type=bool,
                        default=True,
                        help="Flag to enable multiple praat processes. Set to TRUE by default.",
                        metavar='')

    parser.add_argument("-sn", "--synthesiser",
                        type=str,
                        required=True,
                        help="Choose what synthesiser to use",
                        metavar='')

    parser.add_argument("-sci", "--scikit",
                        action='store_true',
                        help="write data to a csv file for use with the scikit learn machine learning library")

    parser.add_argument("-ov", "--overwrite",
                        action='store_true',
                        help="Overwite existing data if it exists.")

    return parser.parse_args()
