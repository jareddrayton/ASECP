#!/usr/bin/env python3

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
    # get version / compile date
    #version = ctypes.c_char_p(b'                                ')
    #VTL.vtlGetVersion(version)
    #print('Compile date of the library: "%s"' % version.value.decode())
    
    parent_dir = pathlib.Path.cwd().parent

    root_vtl_directory = parent_dir / 'vocaltractlab'

    if sys.platform == 'win32':
        VTL = ctypes.cdll.LoadLibrary(str(root_vtl_directory / 'VocalTractLabApi.dll'))
    else:
        VTL = ctypes.cdll.LoadLibrary('./VocalTractLabApi.so')
    #print('hey')
    # initialize vtl
    speaker_file_name = ctypes.c_char_p(str(root_vtl_directory / 'JD2.speaker').encode())
    #print('hey2')

    failure = VTL.vtlInitialize(speaker_file_name)
    print(failure)
    if failure != 0:
        print('hey3')
        raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)

    tract = ctypes.c_char_p('tract_seq{}.txt'.format(i).encode())
    audio_f = ctypes.c_char_p('test{}.wav'.format(i).encode())
    failure = VTL.vtlTractSequenceToAudio(tract, audio_f, None, None)
    print(failure)
    #VTL.vtlClose()
    


def worker2():
    # get version / compile date
    #version = ctypes.c_char_p(b'                                ')
    #VTL.vtlGetVersion(version)
    #print('Compile date of the library: "%s"' % version.value.decode())
    
    parent_dir = pathlib.Path.cwd().parent

    root_vtl_directory = parent_dir / 'vocaltractlab'

    if sys.platform == 'win32':
        VTL = ctypes.cdll.LoadLibrary(str(root_vtl_directory / 'VocalTractLabApi.dll'))
    else:
        VTL = ctypes.cdll.LoadLibrary('./VocalTractLabApi.so')
    print('hey')
    # initialize vtl
    speaker_file_name = ctypes.c_char_p(str(root_vtl_directory / 'JD2.speaker').encode())
    #print('hey2')

    failure = VTL.vtlInitialize(speaker_file_name)

    if failure != 0:
        print('hey3')
        raise ValueError('Error in vtlInitialize! Errorcode: %i' % failure)
    
    tract = ctypes.c_char_p('tract_seq2.txt'.encode())
    audio_f = ctypes.c_char_p('test2.wav'.encode())
    failure = VTL.vtlTractSequenceToAudio(tract, audio_f, None, None)
    print(failure)
    #VTL.vtlClose()
    
#worker2()

def synthesise_artwords_threadpool():
    print('Hello')
    ex = futures.ProcessPoolExecutor(max_workers=mp.cpu_count()-1)
    ex.map(worker, [i for i in range(100)])
    ex.shutdown()



if __name__ == '__main__':
    synthesise_artwords_threadpool()








