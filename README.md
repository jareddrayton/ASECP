#### Introduction

**A**rticulatory **S**ynthesis with **E**volutionary **C**omputing in **P**ython (ASECP) is a tool for performing Acoustic to Articulatory Parameter Inversion (AAPI) with Praat and Genetic Algorithms. 

AAPI refers to ascertaining parameters for a physical model of the vocal tract, that match a given target sound.


#### Basic Usage

For an overview of command line arguments navigate to the root of the directory and type 

`python main.py -h` or
`python main.py --help` 

The simplest usage of the program would be to accept the default values and just specify a target sound file 

`python main.py -sf "vowel-01.wav"`

#### Genetic Algorithm Parameters

The default generation size and population size can be overridden by using `-gs` and `-ps` respectively. Also please note that the indexing of generations starts at 0 and is inclusive. Gen0 contains the randomly initialised population and Gen1 contains the first population created by the genetic operators.


`python main.py  -gs 10 -ps 5`

**Elitism**

Elitism is not enabled by default but can enabled and the number of top indiviudals to be kept for the next generation with the following commands.

`python main.py -el True -es 4`

**Selection**

Linear, exponential, fitness proportional.

`python main.py -sl 'linear'`

**Sampling**

To sample the probability distribution three sampling methods are available.

- Stochastic Universal Sampling 
- Roullete Wheel Sampling
- Tournament. 

Stochastic Universal Sampling is the default sampling method. Currently, if RWS, or Tournament are required the call to the respective function needs to be changed within the crosover functions. 

**Crossover**

A choice between one point crossover and uniform crossover is available.

`python main.py -cr 'one_point'`

`python main.py -cr 'uniform'`

**Mutation**

The mutation rate and standard deviation for the gaussian distribution can be overridden by using `-mr` and `-sd` respectively. The mutation rate should be set between 1.0 and 0.0.

`python main.py -mr 0.05 -sd 0.1`

---

#### Fitness Function



#### Batching Runs 

Can use `script_maker.py` to batch runs. Run with `cmd.exe /k ..\batch_scripts\batch.bat`