# ASECP

**A**rticulatory **S**ynthesis with **E**volutionary **C**omputing in **P**ython (ASECP) implements a Genetic Algorithm to find parameters for an articulatory synthesiser to recreate a given target sound. Currently it is only for use with vowel sounds as targets. 

## Features

#### Genetic Operators 
Selection - Fitness Proportional, Linear Ranking
Crossover - One Point Crossover, Two Point Crossover
Mutation - Gaussian Distrubution


## Usage

#### Requirements
The program uses PRAAT for the articulatory synthesis and signal processing. The PRAAT binaries can be downloaded [here](http://www.fon.hum.uva.nl/praat/).
As well as Python 2.7, NumPy and MatPlotLib are required for 

The script is run from the command line.
```
python main.py vowel-a.wav 5 20 0.2 0.2 P A1 EUC 01
```

