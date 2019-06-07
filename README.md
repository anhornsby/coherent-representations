# How Decisions and the Desire for Coherency Shape Subjective Preferences Over Time
Adam Hornsby & Brad Love, 2019

[![Travis Build Status](https://travis-ci.com/anhornsby/coherent-representations.svg?token=9tuLsSyJNE9sSECQ4whU&branch=master)](https://travis-ci.com/anhornsby/coherent-representations)

[![Docker](https://img.shields.io/badge/Docker-Open%20in%20DockerHub-blue.svg)](https://cloud.docker.com/repository/docker/adamnhornsby/coherent-representations/general)

[![OSF](https://img.shields.io/badge/OSF-View%20data%20on%20OSF-lightgrey.svg)](https://osf.io/5bvmp/)


This repository contains all code files necessary to recreate the analyses and plots in the paper. 

There is also an accompanying Docker container, which can be used to be recreate the results in a controlled environment.

## Codes

There were three main parts of analyses:

1. `simulation` - A simulation to demonstrate how the intrinsic desire to maximize coherency can elicit strong subjective preferences in retrospect of one's choices.
2. `robots` - Code for recreating analyses in Experiment, and the replication documented in the supplemental.
3. `politics` - Codes to analyse the results from the political beliefs experiment.

Please see the paper for more information.

## Running the codes

You can either choose to run these codes with or without the Docker container. Only running with guarantees reproducibility. 

### Running the analyses with Docker

If you are using Docker, pull the container using:

```
docker pull adamnhornsby/coherent-representations
```

#### Running the analyses

Note that all of the following commands will output plots to your current working directory

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

### Running the analyses without Docker

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