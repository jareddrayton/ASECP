import multiprocessing as mp
import pathlib
import subprocess
import sys
from concurrent import futures
from itertools import repeat


def worker(directory, current_generation, individual_id):

    praat_path = pathlib.Path.cwd().parent / 'synthesisers' / 'praat_deterministic' / 'praat'

    praat_script_path = '{}/Generation{!s}/Individual{!s}.praat'.format(directory, current_generation, individual_id)

    if sys.platform.startswith('win32'):
        subprocess.call([praat_path,
                         '--run',
                         '--ansi',
                         praat_script_path], stdout=subprocess.DEVNULL)
    else:
        subprocess.call([praat_path,
                         '--run',
                         praat_script_path], stdout=subprocess.DEVNULL)


def synthesise_artwords_threadpool(directory, CURRENT_GEN, populationsize):

    ex = futures.ThreadPoolExecutor(max_workers=mp.cpu_count()-1)
    ex.map(worker, repeat(directory), repeat(CURRENT_GEN), [i for i in range(populationsize)])
    ex.shutdown()
