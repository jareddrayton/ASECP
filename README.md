# ASECP

**A**rticulatory **S**ynthesis with **E**volutionary **C**omputing in **P**ython (ASECP) implements a Genetic Algorithm to find parameters for the PRAAT articulatory synthesiser, to recreate a given target sound. Currently it is only suitable for use with vowels as target sounds. 

## Features

#### Genetic Operators 
- Selection - Fitness Proportional, Linear Ranking
- Crossover - One Point Crossover, Two Point Crossover
- Mutation - Gaussian Distrubution

#### Fitness Function

The fitness function can use a configurable number of features for calculating a individuals fitness. Currently these are

1. Fundamental Frequency (As calculated by PRAAT)
2. The first five formants.

## Requirements

The program uses PRAAT for the articulatory synthesis and signal processing. The PRAAT binaries can be downloaded [here](http://www.fon.hum.uva.nl/praat/).
As well as Python 2.7, NumPy and MatPlotLib are required for 

## Usage

The script is run from the command line with a number of required arguments.
```
python main.py vowel-a-mono.wav 5 20 0.2 0.2 P A3 EUC 01
```

