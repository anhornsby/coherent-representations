# How Decisions and the Desire for Coherency Shape Subjective Preferences Over Time
Adam Hornsby & Brad Love, 2019

This repository contains all code files necessary to recreate the analyses and plots in the paper. 

There is also an accompanying Docker container, which can be used to be recreate the results in a controlled environment.

## Codes

There were three main parts of analyses:

1. `simulation` - A simulation to demonstrate how the intrinsic desire to maximize coherency can elicit strong subjective preferences in retrospect of one's choices.
2. `robots` - We provide code capable of analysing results from the two experiments. Chiefly, the experiment reported in the main text. Also, the re-run, which was the same, with the added political question at the end (see supplemental of paper for details).
3. `politics` - Codes to analyse the results from the political beliefs experiment.

## Running the codes

You can either choose to run these codes with or without the Docker container. Only running with guarantees reproducibility. 

### Preparing Docker

If you are using Docker, pull the container using:

```
docker pull adamnhornsby/coherent-representations
```

#### Running the analyses in container

**Note that all of the following commands will output plots to your current working directory**

The main reported results will be printed to stdout.

To run the simulation, please run:

```shell
docker run -v ${PWD}:/usr/local/data/ -it adamnhornsby/coherent-representations simulation /usr/local/data/
```

To run the robot experiments results:

```shell
docker run -v ${PWD}:/usr/local/data/ -it adamnhornsby/coherent-representations robots /usr/local/data/
```

To run the robot experiment re-run:

```
docker run -v ${PWD}:/usr/local/data/ -it adamnhornsby/coherent-representations robots_rerun /usr/local/data/
```

To run the politics experiment analyses (note this also requires R and the Rfit package):

```
docker run -v ${PWD}:/usr/local/data/ -it adamnhornsby/coherent-representations politics /usr/local/data/

python ~/data/politics/effect_size_plot.py

Rscript ~/politics/anova.R ~/data/politics/politics_data.csv /usr/local/data/
```

### Environment preparation when not running 

If you are not using Docker, please:

1. Install the Python 2.7 requirements in `requirements.txt`
2. Clone this code repository
2. Download the data for the three experiments from https://osf.io/5bvmp/ and put it in a folder called `data` within this directory.

#### Running the analyses

**Note that all of the following commands will output plots to your current working directory**

The main reported results will be printed to stdout.

To run the simulation, please run:

```shell
python simulation/ /path/to/output/plots/
```

To run the robot experiments results:

```shell
python robots/ data/robots/robots-first/robots_results.csv n /path/to/output/plots/
```

To run the robot experiment re-run:

```
python robots/ data/robots/robots-rerun/robots_rerun_results.csv y /path/to/output/plots/
```

To run the politics experiment analyses:

```
Rscript politics/anova.R data/politics/politics_data.csv /path/to/output/plots
python politics/ data/politics/politics_data.csv /path/to/output/plots
```

# Contact

If you have any questions, please contact adam.hornsby.10@ucl.ac.uk