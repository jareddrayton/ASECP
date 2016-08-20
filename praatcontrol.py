import subprocess, time, os, math
import numpy as np
from scipy.io import wavfile

def synthesise_artwords_parallel(currentgeneration, generationsize, directory):
	""" Loops through all PRAAT script in a directory and opens them in the cmd line as separate processes"""
	
	for i in range(generationsize):
		p = subprocess.Popen('Praat.exe --run "%s\Generation%d\Individual%d.praat"' % (directory, currentgeneration, i))

	p.communicate()

	time.sleep(4)

def synthesise_artwords_serial(currentgeneration, generationsize, directory):
	""" Loops through all PRAAT script in a directory and opens them in the cmd line sequentially"""
	
	for i in range(generationsize):
		subprocess.call('Praat.exe --run "%s\Generation%d\Individual%d.praat"' % (directory, currentgeneration, i))
	
	time.sleep(1.5)


def get_time(soundfile):
	"""Find and return the length of the target sound

    returns: returns a string containing soundfile length as string
	"""

	script = open("AnalyseTargetSound.praat", 'wb')
	script.write('Read from file: "%s"\r\n' % soundfile)
	script.write('time = Get total duration\r\n')
 	script.write('writeFileLine: "time.txt", time\r\n')
 	script.close()

 	subprocess.call("Praat.exe --run AnalyseTargetSound.praat")
 	os.remove('AnalyseTargetSound.praat')

	with open("time.txt", "r") as timetxt:
		TargetLength = timetxt.readline().strip()
	os.remove('time.txt')
	
	return TargetLength

def get_target_frequencies(TargetLength, soundfile):
	""" Extract Pitch and Formants of the Target Sound"""

	script = open("GetPitch.praat", 'wb')
	script.write('Read from file: "%s"\r\n' % soundfile)
	script.write('To Pitch: %s, 75, 600\r\n' % TargetLength)
	script.write('Get mean: 0, 0, "Hertz"\r\n')
	script.write('appendFile ("pitch.txt", info$ ())')
 	script.close()

 	subprocess.call("Praat.exe --run GetPitch.praat")
 	os.remove('GetPitch.praat')

	script = open("GetFormants.praat", 'wb')
	script.write('Read from file: "%s"\r\n' % soundfile)
	script.write('To Formant (burg): 0, 5, 5500, %s, 50\r\n' % TargetLength)
	script.write('List: "no", "yes", 6, "no", 3, "no", 3, "no"\r\n')
 	script.write('appendFile ("formants.txt", info$ ())')
 	script.close()

 	subprocess.call("Praat.exe --run GetFormants.praat")
 	os.remove('GetFormants.praat')

	with open("pitch.txt", "r") as pitch:
	
		pitch = pitch.readline().strip()

	pitch = pitch[0:7]
	pitch = float(pitch)
	
	with open("formants.txt", "r") as formants:
	
		lines = formants.readlines()
		values = lines[1].split("\t")
	
	values[0] = pitch
	
	values = map(float, values)

	os.remove('pitch.txt')
	os.remove('formants.txt')
	
	print values
	return values[1:3]

def get_target_intensity(soundfile):

	script = open("GetIntensity.praat", 'wb')
	script.write('Read from file: "%s"\r\n' % soundfile)
	script.write('To Intensity: 100, 0, "yes"\r\n')
	script.write('Get standard deviation: 0, 0\r\n')
 	script.write('appendFile ("intensity.txt", info$ ())')
 	script.close()

 	subprocess.call("Praat.exe --run GetIntensity.praat")
 	os.remove('GetIntensity.praat')

 	with open("intensity.txt", "r") as f:
		
		intensity = f.readline()
		intensity = intensity.strip()
		intensity = intensity.strip("dB")
		intensity = abs(float(intensity))

	os.remove('intensity.txt')

	return intensity

def get_individual_frequencies(name, directory, currentgeneration):
	""" Opens the pitch.txt file generated by PRAAT

	returns: a list of frequencies  
	"""

	with open("%s\Generation%d\\pitch%d.txt" % (directory, currentgeneration, (int(name))), "r") as pitch:
		
		# Sets the canpitch variable to a list containing the first line of the file and strips white space.
		candpitch = pitch.readline().strip()
		candpitch = candpitch.strip('Hz')
		candpitch = candpitch.strip()
		
	# Opens text file with formant information as the var .formants
	with open("%s\Generation%d\\formants%d.txt" % (directory, currentgeneration, (int(name))), "r") as formants:
		# Splits the lines of the text file into items of a list in .lines
		lines = formants.readlines()
		
	# Assigns the second item from .lines to candformants
	candformants = lines[1].split("\t")

	for i in range(len(candformants)):
		
		candformants[i] = candformants[i].strip()
		
		if candformants[i].islower() == True:
			candformants[i] = 10000

	candformants = map(float, candformants)

	VUV = True

	if candpitch.islower() == True:
		candpitch = 2000
		candformants[1] = 10000
		candformants[2] = 10000
		candformants[3] = 8000
		candformants[4] = 10000
		candformants[5] = 12000
		VUV = False

	candformants[0] = candpitch

	os.remove("%s\Generation%d\\pitch%d.txt" % (directory, currentgeneration, int(name)))
	os.remove("%s\Generation%d\\formants%d.txt" % (directory, currentgeneration, int(name)))
	
	return candformants[1:3], VUV

def get_individual_intensity(name, directory, currentgeneration,targetintensity):
	""" Opens the intensity.txt file generated by PRAAT
	Estimates the average intensity 

	returns:
	"""

	with open("%s\Generation%d\\intensity%d.txt" % (directory, currentgeneration, (int(name))), "r") as f:
		intensity = f.readline()
		intensity = intensity.strip()
		intensity = intensity.strip("dB")
		intensity = float(intensity)
		intensity = round(abs(targetintensity - intensity), 1)
		
	os.remove("%s\Generation%d\\intensity%d.txt" % (directory, currentgeneration, int(name)))

	return intensity

def get_individual_RMS(name,directory,currentgeneration):


	t = "%s\Generation%d\\Individual%d.wav" % (directory, currentgeneration, (int(name)))
	
	rate,data = wavfile.read(t, mmap=False)

	total = 0.0

	for i in range(len(data)):

		total += data[i] ** 2

	total = total / len(data)
	
	return math.sqrt(total)


def hz_to_mel(frequencies):
	""" Converts a list of frequencies to mel scale

	returns: a list of frequencies converted to mel
	"""
	
	for i in range(len(frequencies)):
		frequencies[i] = 2595 * math.log10(1+(frequencies[i]/700.0))

	return frequencies

def hz_to_cent(list1,list2):
	""" Takes two lists of frequencies and returns their differences in cents

	returns:
	"""
	
	for i in range(len(frequencies)):
		(math.fabs(1200 * math.log(list2[i] / list1[i], 2)))
	return frequencies