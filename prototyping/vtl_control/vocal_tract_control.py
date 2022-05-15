import ctypes
import sys
import pathlib
import multiprocessing as mp
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile

from itertools import repeat
from concurrent import futures

def worker(i):
    parent_dir = pathlib.Path.cwd().parent

    root_vtl_directory = parent_dir / 'vocaltractlab'

    if sys.platform == 'win32':
        VTL = ctypes.cdll.LoadLibrary(str(root_vtl_directory / 'VocalTractLabApi.dll'))
    else:
        VTL = ctypes.cdll.LoadLibrary('./VocalTractLabApi.so')

    speaker_file_name = ctypes.c_char_p(str(root_vtl_directory / 'JD2.speaker').encode())

    failure = VTL.vtlInitialize(speaker_file_name)

    if failure != 0:
        raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)

    tract = ctypes.c_char_p('tract_seq{}.txt'.format(i).encode())
    audio_f = ctypes.c_char_p('test{}.wav'.format(i).encode())
    failure = VTL.vtlTractSequenceToAudio(tract, audio_f, None, None)


def synthesise_tracts_threadpool():
    ex = futures.ProcessPoolExecutor(max_workers=mp.cpu_count()-1)
    ex.map(worker, [i for i in range(100)])
    ex.shutdown()


if __name__ == '__main__':
    synthesise_artwords_threadpool()
