import numpy as np
import vocal_tract_control

def write_tract_sequence_file(identifier):
    sample_rate = 44100
    target_time = 1.0
    fold_type = 'Geometric glottis'
    step_size = 110 # assume 44100 sample rate.
    target_pressure = 8000
    number_of_states = int((sample_rate * target_time) // step_size)
    pressure = np.geomspace(1, target_pressure, num=20)
    glottis_params = ['101.594', '0', '0.0102', '0.02035', '0.05', '1.22204', '1', '0.05', '0',  '25', '-10'] 
    vocal_tract_params = ['0.1667', '-3.9392', '0', '-4.1498', '0.0718', '0.9937', '0.8', '-0.1', '0.1524', '-1.8333', '4.2474', '-1.694', '2.5488', '-0.675', '-2.8371', '-2.9034', '0.2064', '0.0384', '0.1488']


    print(len(glottis_params))
    print(len(vocal_tract_params))

    with open('tract_seq{}.txt'.format(identifier), 'w') as f:
        f.write('# The first two lines (below the comment lines) indicate the name of the vocal fold model and the number of states.' + '\n')
        f.write('# The following lines contain the control parameters of the vocal folds and the vocal tract (states)' + '\n')
        f.write('# in steps of 110 audio samples (corresponding to about 2.5 ms for the sampling rate of 44100 Hz).' + '\n')
        f.write('# For every step, there is one line with the vocal fold parameters followed by' + '\n')
        f.write('# one line with the vocal tract parameters.' + '\n')
        
        f.write('#' + '\n')
        f.write(fold_type + '\n')
        f.write(str(number_of_states) + '\n')
        for state in pressure:
            glottis_params[1] = str(state)
            f.write(' '.join(glottis_params) + '\n')
            f.write(' '.join(vocal_tract_params) + '\n')
        glottis_params[1] = str(target_pressure)
        
        for _ in range(number_of_states - 20):
            f.write(' '.join(glottis_params) + '\n')
            f.write(' '.join(vocal_tract_params) + '\n')


def main():
    vocal_tract_control.synthesise_artwords_threadpool()

if __name__ == '__main__':
    main()


