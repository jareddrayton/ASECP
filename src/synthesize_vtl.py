import ctypes
import multiprocessing as mp
import pathlib
import sys
from concurrent import futures
from itertools import repeat


def worker(directory, current_generation_index, i):

    root_vtl_directory = pathlib.Path.cwd().parent / 'synthesisers' / 'vocaltractlab'

    if sys.platform == 'win32':
        VTL = ctypes.cdll.LoadLibrary(str(root_vtl_directory / 'VocalTractLabApi.dll'))
    else:
        VTL = ctypes.cdll.LoadLibrary('./VocalTractLabApi.so')

    speaker_file_name = ctypes.c_char_p(str(root_vtl_directory / 'JD2.speaker').encode())

    failure = VTL.vtlInitialize(speaker_file_name)

    if failure != 0:
        raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)

    tract = ctypes.c_char_p('{}/Generation{!s}/tract_seq{}.txt'.format(directory, current_generation_index, i).encode())
    audio_f = ctypes.c_char_p('{}/Generation{!s}/Individual{}.wav'.format(directory, current_generation_index, i).encode())
    failure = VTL.vtlTractSequenceToAudio(tract, audio_f, None, None)


def synthesise_tracts_processpool(directory, current_generation_index, population_size):
    ex = futures.ProcessPoolExecutor(max_workers=mp.cpu_count()-1)
    ex.map(worker, repeat(directory), repeat(current_generation_index), [i for i in range(population_size)])
    ex.shutdown()


if __name__ == '__main__':
    synthesise_tracts_processpool()
