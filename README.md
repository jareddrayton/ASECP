#### ASECP

**A**rticulatory **S**ynthesis with **E**volutionary **C**omputing in **P**ython (ASECP) is a tool for performing Acoustic to Articulatory Parameter Inversion (AAPI) with Praat and Genetic Algorithms. 

AAPI refers to ascertaining parameters for a physical model of the vocal tract, that match a given target sound.


#### Basic Usage

For an overview of command line arguments navigate to the root of the directory and type 

`python main.py -h` or
`python main.py --help` 

The simplest usage of the program would be to accept the default values and just specify a target sound file 

`python main.py -sf "vowel-01.wav"`

##### Genetic Algorithm Parameters

The default generation size and population size can be overridden by using `-gs` and `-ps` respectively. Also please note that the indexing of generations starts at 0 and is inclusive. Gen0 contains the randomly initialised population and Gen1 contains the first population created by the genetic operators.

`python main.py -sf "vowel-01.wav" -gs 10 -ps 5`

The mutation rate and standard deviation can be overridden by using `-mr` and `-sd` respectively.

`python main.py -sf "vowel-01.wav" -mr 10 -sd 5`

##### Fitness Function

#### Batching Runs 

script_maker