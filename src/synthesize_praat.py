import multiprocessing as mp
import subprocess
import sys
import time
from concurrent import futures
from itertools import repeat


def synthesise_artwords_parallel(currentgeneration, generationsize, directory):
    """ Loops through all Praat script in a directory and opens them in the cmd line as separate processes"""

    for i in range(generationsize):
        p = subprocess.Popen(['./praat',
                              '--run',
                              '{}/Generation{!s}/Individual{!s}.praat'.format(directory, currentgeneration, i)])

    p.wait()
    time.sleep(3)


def worker(directory, current_generation, individual_id):

    praat_script_path = '{}/Generation{!s}/Individual{!s}.praat'.format(directory, current_generation, individual_id)

    if sys.platform.startswith('win32'):
        subprocess.call(['./praat',
                         '--run',
                         '--ansi',
                         praat_script_path], stdout=subprocess.DEVNULL)
    else:
        subprocess.call(['./praat',
                         '--run',
                         praat_script_path], stdout=subprocess.DEVNULL)


def synthesise_artwords_threadpool(directory, CURRENT_GEN, populationsize):

    ex = futures.ThreadPoolExecutor(max_workers=mp.cpu_count()-1)
    ex.map(worker, repeat(directory), repeat(CURRENT_GEN), [i for i in range(populationsize)])
    ex.shutdown()
