import glob
import os
import random
from pathlib import Path

feature_types = ['_fbank_', '_formant_', '_logfbank_', '_mfcc_']
number_of_samples = [200, 400, 600, 2400]
directory = 'C:\\Users\\Jazz\\VSCODE\\Repo\\ASECP\\data\\new_folder'


def extract_lines(file_list):
    """

    PARAMETERS
    ----------
    file_list : list
        list of filepaths 

    RETURNS
    -------
    lines : list


    """
    lines = []
    for input_file in file_list:
        with open('{}'.format(input_file), 'r') as f:
            lines += f.readlines()

    return lines


def write_out_post_processed_data(data_dict, sample_size, feature):

    lines_to_write = []
    valid = True
    for k, v in data_dict.items():
        new_set = set()
        new_list = []
        for line in v:
            param = ''.join(line.split(',')[0:19])
            if param not in new_set:
                new_set.add(param)
                new_list.append(line)
        if len(new_list) < sample_size:
            print("not enough samples for ")
            valid = False
        else:
            random.shuffle(new_list)
            new_list = new_list[:sample_size]
            lines_to_write += new_list
    
    if valid:
        with open('data_sets\\labelled{}pp_{}.txt'.format(feature, sample_size), 'w') as f:
            f.writelines(lines_to_write)


def process_data(src_directory, feature):
    file_paths = os.listdir(src_directory)

    sounds = set([x.split('.')[0] for x in file_paths])

    new_dict = {}
    
    for sound in sounds:
        input_files = [x for x in file_paths if sound in x]

        new_files = []
        for x in input_files:
            new_files += glob.glob('{}\\{}\\*{}*'.format(src_directory, x, feature))

        #print(new_files)

        new_dict[sound] = extract_lines(new_files)
        #print(len(new_dict[sound]))
    

    for sample_size in number_of_samples:
        write_out_post_processed_data(new_dict, sample_size, feature)

def main():
    for feature in feature_types:
        process_data(directory, feature)

main()