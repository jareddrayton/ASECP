import glob
import scipy.io.wavfile as wav

from scipy.spatial.distance import cosine
from python_speech_features import mfcc
import fastdtw


def compare_sounds(target_name):
    glob_string = '..\\target_sounds\\Primary*'
    sounds = glob.glob(glob_string)
    target_sr, target_sig = wav.read(f'..\\target_sounds\\{target_name}')
    target_mfcc = mfcc(target_sig, samplerate=target_sr, appendEnergy=False)

    for sound in sounds:
        compared_sr, compared_sig = wav.read(sound)
        compared_mfcc = mfcc(compared_sig, samplerate=compared_sr, appendEnergy=False)

        distance, path = fastdtw.fastdtw(target_mfcc, compared_mfcc, dist=cosine)
        print(distance, sound)


compare_sounds("Primary1.wav")
