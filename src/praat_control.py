import csv
import math
import multiprocessing as mp
import os
import subprocess
import sys
import time
from concurrent import futures
from itertools import repeat

import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import mfcc, fbank, logfbank


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


def get_time(soundfile):
    """
    Return the length of a given audio file in seconds.

    PARAMETERS
    ----------
    soundfile : pathlib Obj
        A pathlib object representing the absolute file path of the audio file

    RETURNS
    -------
    time : str
        A string containing the length of the given audio file
    """

    with open('AnalyseTargetSound.praat', 'w') as script:
        script.write('Read from file: "{}"\n'.format(soundfile))
        script.write('time = Get total duration\n')
        script.write('writeFileLine: "time.txt", time\n')

    subprocess.call(['./praat', '--ansi', '--run', 'AnalyseTargetSound.praat'], stdout=subprocess.DEVNULL)

    with open('time.txt', 'r') as timetxt:
        time = timetxt.readline().strip()

    os.remove('AnalyseTargetSound.praat')
    os.remove('time.txt')

    return time


def get_sample_rate(soundfile):

    (rate, _) = wav.read(soundfile)

    return rate


def get_target_formants(TargetLength, soundfile, NO_FORMANTS):
    """ Extract Pitch and Formants of the Target Sound"""

    script = open("GetPitch.praat", 'w')
    script.write('Read from file: "{!s}"\r\n'.format(soundfile))
    script.write('To Pitch: {!s}, 75, 600\r\n'.format(TargetLength))
    script.write('Get mean: 0, 0, "Hertz"\r\n')
    script.write('appendFile ("pitch.txt", info$ ())')
    script.close()

    subprocess.call(['./praat', '--ansi', '--run', 'GetPitch.praat'], stdout=subprocess.DEVNULL)
    os.remove('GetPitch.praat')

    script = open("GetFormants.praat", 'w')
    script.write('Read from file: "{!s}"\r\n'.format(soundfile))
    script.write('To Formant (sl): 0, 5, 5000, {!s}, 50\r\n'.format(TargetLength))
    script.write('List: "no", "yes", 6, "no", 3, "no", 3, "no"\r\n')
    script.write('appendFile ("formants.txt", info$ ())')
    script.close()

    subprocess.call(['./praat', '--ansi', '--run', 'GetFormants.praat'], stdout=subprocess.DEVNULL)
    os.remove('GetFormants.praat')

    with open("pitch.txt", "r") as pitch:

        pitch = pitch.readline().strip()

    pitch = pitch[0:7]
    pitch = float(pitch)

    os.remove('pitch.txt')

    with open("formants.txt", "r") as formants:

        lines = formants.readlines()
        values = lines[1].split("\t")

    os.remove('formants.txt')

    for i in range(len(values)):

        values[i] = values[i].strip()

        if values[i] == "--undefined--":
            values[i] = 0

    values[0] = pitch

    values = list(map(float, values))

    return values[1:NO_FORMANTS+1]


def get_formants(file_path):
    """
    take in filepath to a formant table
    """

    data = []

    with open(file_path, 'r') as f:
        formant_table = csv.reader(f)
        for row in formant_table:
            data.append(row)

    formant_dict = {'F1': [], 'F2': [], 'F3': [], 'F4': [], 'F5': []}

    data = data[1:]

    f1 = [float(x[1]) if x[1] != '--undefined--' else None for x in data]
    f2 = [float(x[2]) if x[2] != '--undefined--' else None for x in data]
    f3 = [float(x[3]) if x[3] != '--undefined--' else None for x in data]
    f4 = [float(x[4]) if x[4] != '--undefined--' else None for x in data]
    f5 = [float(x[5]) if x[5] != '--undefined--' else None for x in data]

    formants = [f1, f2, f3, f4, f5]

    for key in formant_dict.keys():
        formant_dict[key] = []

    forms = []

    for f in formants:
        # print('Per ', 100 * (1 - f.count(None) / len(f)))
        # print('Mean', np.mean([x for x in f if x != None]))
        # print('Std ', np.std([x for x in f if x != None]))
        # print('')
        forms.append(np.mean([x for x in f if x is not None]))

    os.remove(file_path)

    return forms


def write_formant_table(file_path, name, sound_type='Individual'):

    praat_script = file_path / 'WriteFormantTable{}{}.praat'.format(sound_type, name)
    audio_file = file_path / '{}{}.wav'.format(sound_type, name)
    formant_table = file_path / '{}{}.Table'.format(sound_type, name)

    with open(praat_script, 'w') as f:
        f.write('Read from file: "{}"\n'.format(audio_file))
        f.write('To Formant (sl): 0, 5, 4500, 0.025, 50\n')
        f.write('Down to Table: "no", "no", 6, "no", 3, "yes", 1, "no"\n')
        f.write('Save as comma-separated file: "{}"\n'.format(formant_table))

    run_praat_command(praat_script, purge=True)

    return get_formants(formant_table)


def write_target_formant_table(file_path, file_name):

    praat_script = file_path / 'read_target_formants{}.praat'.format(file_name)
    audio_file = file_path / '{}'.format(file_name)
    formant_table = file_path / '{}.Table'.format(file_name)

    with open(praat_script, 'w') as f:
        f.write('Read from file: "{}"\n'.format(audio_file))
        f.write('To Formant (sl): 0, 5, 4500, 0.025, 50\n')
        f.write('Down to Table: "no", "no", 6, "no", 3, "yes", 1, "no"\n')
        f.write('Save as comma-separated file: "{}"\n'.format(formant_table))

    run_praat_command(praat_script)

    return get_formants(formant_table)


def voice_report(file_path, length, name='', sound_type='Individual'):

    praat_script = file_path / 's{}{}.praat'.format(sound_type, name)
    audio_file = file_path / '{}{}.wav'.format(sound_type, name)
    formant_table = file_path / '{}{}.VoiceReport'.format(sound_type, name)

    with open(praat_script, 'w') as f:
        f.write('Read from file: "{}"\n'.format(audio_file))
        f.write('To Pitch: 0, 75, 600\n')
        f.write('selectObject: "Sound {}{}"\n'.format(sound_type, name))
        f.write('plusObject: "Pitch {}{}"\n'.format(sound_type, name))
        f.write('To PointProcess (cc)\n')
        f.write('selectObject: "Sound {}{}"\n'.format(sound_type, name))
        f.write('plusObject: "Pitch {}{}"\n'.format(sound_type, name))
        f.write('plusObject: "PointProcess {}{}_{}{}"\n'.format(sound_type, name, sound_type, name))
        f.write('voiceReport$ = Voice report: 0, 0, 75, 600, 1.3, 1.6, 0.03, 0.45\n')
        f.write('meanpitch = extractNumber (voiceReport$, "Mean pitch: ")\n')
        f.write('fracframes = extractNumber (voiceReport$, "Fraction of locally unvoiced frames: ")\n')
        f.write('voicebreaks = extractNumber (voiceReport$, "Number of voice breaks: ")\n')
        f.write('writeFileLine: "{}", meanpitch\n'.format(formant_table))
        f.write('appendFileLine: "{}", fracframes\n'.format(formant_table))
        f.write('appendFileLine: "{}", voicebreaks\n'.format(formant_table))

    run_praat_command(praat_script, purge=True)

    with open(formant_table, 'r') as f:
        voice_report = [x.strip() for x in f.readlines()]

    if voice_report[0] == '--undefined--':
        voice_report[0] = False
    else:
        voice_report[0] = float(voice_report[0])

    voice_report[1] = float(voice_report[1])
    voice_report[2] = int(voice_report[2])

    os.remove(formant_table)

    return voice_report


def run_praat_command(praat_script, purge=False):
    subprocess.call(['./praat',
                     '--run',
                     '--ansi',
                     praat_script], stdout=subprocess.DEVNULL)

    if purge:
        os.remove(praat_script)


def get_target_intensity(soundfile):
    script = open("GetIntensity.praat", 'w')
    script.write('Read from file: "{!s}"\r\n'.format(soundfile))
    script.write('To Intensity: 100, 0, "yes"\r\n')
    script.write('Get standard deviation: 0, 0\r\n')
    script.write('appendFile ("intensity.txt", info$ ())')
    script.close()

    subprocess.call(['./praat', '--ansi', '--run', 'GetIntensity.praat'], stdout=subprocess.DEVNULL)
    os.remove('GetIntensity.praat')

    with open("intensity.txt", "r") as f:
        intensity = f.readline()
        intensity = intensity.strip()
        intensity = intensity.strip("dB")
        intensity = abs(float(intensity))

    os.remove('intensity.txt')

    return intensity


def get_target_RMS(soundfile):
    t = soundfile

    _, data = wav.read(t, mmap=False)

    total = 0.0

    for i in range(len(data)):
        total += data[i] ** 2

    total = total / len(data)

    return math.sqrt(total)


def get_target_mfcc_average(soundfile):
    (rate, signal) = wav.read(soundfile)

    mfcc_features_target = mfcc(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(mfcc_features_target, axis=0)


def get_target_logfbank_average(soundfile):
    (rate, signal) = wav.read(soundfile)

    logfbank_features_target = logfbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features_target, axis=0)


def get_target_fbank_average(soundfile):
    (rate, signal) = wav.read(soundfile)

    fbank_features_target, _ = fbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(fbank_features_target, axis=0)


def get_target_mfcc(soundfile):
    (rate, signal) = wav.read(soundfile)

    return mfcc(signal, rate, winlen=0.025, winstep=0.025)


def get_target_logfbank(soundfile):
    (rate, signal) = wav.read(soundfile)

    return logfbank(signal, rate, winlen=0.025, winstep=0.025)


def get_individual_pitch(name, directory, currentgeneration):

    with open("{}/Generation{!s}/pitch{!s}.txt".format(directory, currentgeneration, name), "r") as pitch:
        # Sets the canpitch variable to a list containing the first line of the file and strips white space.
        candpitch = pitch.readline().strip()
        candpitch = candpitch.strip('Hz')
        candpitch = candpitch.strip()

    os.remove("{}/Generation{!s}/pitch{!s}.txt".format(directory, currentgeneration, name))

    if candpitch.islower():
        return False
    else:
        return True


def get_individual_formants(name, directory, currentgeneration, samplerate):
    """ Opens the pitch.txt file generated by PRAAT

    returns: a list of the first five formant frequencies
    """

    # Opens text file with formant information as the var .formants
    with open("{}/Generation{!s}/formants{!s}.txt".format(directory, currentgeneration, name), "r") as formants:
        # Splits the lines of the text file into items of a list in .lines
        lines = formants.readlines()

    # Assigns the second item from .lines to candformants
    candformants = lines[1].split("\t")

    # print('candformants', candformants)

    # Strips whitespace and checks if a formant is undefined and sets this to half the sample rate
    for i in range(len(candformants)):
        candformants[i] = candformants[i].strip()
        if candformants[i].islower():
            candformants[i] = str(samplerate/2)

    # Converts the list of strings to a list of floats
    candformants = list(map(float, candformants))

    # print('candformants', candformants)

    os.remove("{}/Generation{!s}/formants{!s}.txt".format(directory, currentgeneration, name))

    return candformants[1:6]


def get_individual_intensity(name, directory, currentgeneration, targetintensity):
    """ Opens the intensity.txt file generated by PRAAT
    Estimates the average intensity

    returns:
    """

    with open("{}/Generation{!s}/intensity{!s}.txt".format(directory, currentgeneration, name), "r") as f:
        intensity = f.readline()
        intensity = intensity.strip()
        intensity = intensity.strip("dB")
        intensity = float(intensity)

    os.remove("{}/Generation{!s}/intensity{!s}.txt".format(directory, currentgeneration, name))

    intensity = abs((targetintensity / intensity) - 1) + 1

    return round(intensity, 2)


def get_individual_RMS(name, directory, currentgeneration, targetrms):
    t = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    _, data = wav.read(t, mmap=False)

    total = 0.0

    for i in range(len(data)):
        total += data[i] ** 2

    total = total / len(data)
    rms = math.sqrt(total)

    rms = abs((targetrms / rms) - 1) + 1

    return round(rms, 2)


################################################################################################

def get_individual_mfcc_average(name, directory, currentgeneration):
    soundfile = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    (rate, signal) = wav.read(soundfile)

    mfcc_features = mfcc(signal, rate, winlen=0.025, winstep=0.025, appendEnergy=False)

    return np.average(mfcc_features, axis=0)


def get_individual_fbank_average(name, directory, currentgeneration):
    soundfile = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    (rate, signal) = wav.read(soundfile)

    logfbank_features_individual, _ = fbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features_individual, axis=0)


def get_individual_logfbank_average(name, directory, currentgeneration):
    soundfile = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    (rate, signal) = wav.read(soundfile)

    logfbank_features_individual = logfbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features_individual, axis=0)

################################################################################################


def get_individual_mfcc(name, directory, currentgeneration):
    soundfile = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    (rate, signal) = wav.read(soundfile)

    return mfcc(signal, rate, winlen=0.025, winstep=0.025)


def get_individual_logfbank(name, directory, currentgeneration):
    soundfile = "{}/Generation{!s}/Individual{!s}.wav".format(directory, currentgeneration, name)

    (rate, signal) = wav.read(soundfile)

    return logfbank(signal, rate, winlen=0.025, winstep=0.025)
