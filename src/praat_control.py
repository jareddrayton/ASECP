import csv
import math
import os
import pathlib
import subprocess

import numpy as np
import scipy.io.wavfile as wav
from python_speech_features import fbank, logfbank, mfcc


def get_time(soundfile):
    """
    Returns the length of a given audio file in seconds.

    PARAMETERS
    ----------
    soundfile : pathlib Object
        A pathlib object representing the absolute file path of the audio file

    RETURNS
    -------
    time : str
        A string containing the length of the given audio file
    """

    script_name = 'AnalyseTargetSound.praat'

    with open(script_name, 'w') as script:
        script.write('Read from file: "{}"\n'.format(soundfile))
        script.write('time = Get total duration\n')
        script.write('writeFileLine: "time.txt", time\n')

    run_praat_command(script_name, True)

    with open('time.txt', 'r') as timetxt:
        time = timetxt.readline().strip()

    os.remove('time.txt')

    return time


def get_sample_rate(soundfile):

    (rate, _) = wav.read(soundfile)

    return rate


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

    praat_script = file_path / \
        'WriteFormantTable{}{}.praat'.format(sound_type, name)
    audio_file = file_path / '{}{}.wav'.format(sound_type, name)
    formant_table = file_path / '{}{}.Table'.format(sound_type, name)

    with open(praat_script, 'w') as f:
        f.write('Read from file: "{}"\n'.format(audio_file))
        f.write('nocheck To Formant (sl): 0, 5, 4500, 0.025, 50\n')
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
        f.write('nowarn To Formant (sl): 0, 5, 4500, 0.025, 50\n')
        f.write('Down to Table: "no", "no", 6, "no", 3, "yes", 1, "no"\n')
        f.write('Save as comma-separated file: "{}"\n'.format(formant_table))

    run_praat_command(praat_script)

    return get_formants(formant_table)


def get_voice_report(file_path, length, name='', sound_type='Individual'):

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


def get_target_intensity(soundfile):

    script_name = "GetIntensity.praat"

    with open(script_name, 'w') as script:
        script.write('Read from file: "{!s}"\r\n'.format(soundfile))
        script.write('To Intensity: 100, 0, "yes"\r\n')
        script.write('Get standard deviation: 0, 0\r\n')
        script.write('appendFile ("intensity.txt", info$ ())')

    run_praat_command(script_name, True)

    with open("intensity.txt", "r") as f:
        intensity = f.readline()
        intensity = intensity.strip()
        intensity = intensity.strip("dB")
        intensity = abs(float(intensity))

    os.remove('intensity.txt')

    return intensity


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

    os.remove("{}/Generation{!s}/intensity{!s}.txt".format(directory,
              currentgeneration, name))

    intensity = abs((targetintensity / intensity) - 1) + 1

    return round(intensity, 2)


def get_target_rms(soundfile):
    t = soundfile

    _, data = wav.read(t, mmap=False)

    total = 0.0

    for i in range(len(data)):
        total += data[i] ** 2

    total = total / len(data)

    return math.sqrt(total)


def get_individual_rms(name, directory, currentgeneration, targetrms):
    t = "{}/Generation{!s}/Individual{!s}.wav".format(
        directory, currentgeneration, name)

    _, data = wav.read(t, mmap=False)

    total = 0.0

    for i in range(len(data)):
        total += data[i] ** 2

    total = total / len(data)
    rms = math.sqrt(total)

    rms = abs((targetrms / rms) - 1) + 1

    return round(rms, 2)


def get_mfcc(soundfile):
    (rate, signal) = wav.read(soundfile)

    return mfcc(signal, rate, winlen=0.025, winstep=0.025)


def get_mfcc_average(soundfile):
    rate, signal = wav.read(soundfile)

    mfcc_features = mfcc(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(mfcc_features, axis=0)


def get_fbank(soundfile):
    rate, signal = wav.read(soundfile)

    fbank_features, _ = fbank(signal, rate, winlen=0.025, winstep=0.025)

    return fbank_features


def get_fbank_average(soundfile):
    rate, signal = wav.read(soundfile)

    fbank_features, _ = fbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(fbank_features, axis=0)


def get_logfbank(soundfile):
    rate, signal = wav.read(soundfile)

    return logfbank(signal, rate, winlen=0.025, winstep=0.025)


def get_logfbank_average(soundfile):
    rate, signal = wav.read(soundfile)

    logfbank_features = logfbank(signal, rate, winlen=0.025, winstep=0.025)

    return np.average(logfbank_features, axis=0)


def run_praat_command(praat_script, purge=False):

    praat_path = pathlib.Path.cwd().parent / 'synthesisers' / 'praat' / 'praat'

    subprocess.call([praat_path,
                     '--run',
                     '--ansi',
                     praat_script], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if purge:
        os.remove(praat_script)
