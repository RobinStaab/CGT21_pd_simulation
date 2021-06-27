# Repeated and Infinite Spatial Prisoner's dilemma - CGT21
This repository contains an RSPD and ISPD implementation for the course "Controversies in Game Theory 2021".

## Setup
We recommend setting up a Python 3 conda environment. All dependencies of the project are listed in the ```requirements.txt``` file. 

To install via conda use

```shell
conda env create --name cgt -f requirements.txt
conda activate cgt
```

otherwise you can install requirements via pip using

```
python3 -m pip install -r requirements.txt
```

## Usage

The simulator can be used in one of two ways:

1. In a web dashboard that allows quick adjustments of strategies, hyperparameters, and live updates on all statistics and the board state.
2. A console-based application that enables a user to run multiple thousands of experiments without supervision and receive aggregated results.

### Web dashboard

In order to start the dashboard, simply execute the following from the root directory of the project

```shell
python3 main\_dash.py
```

afterward open a browser at ```127.0.0.0.8050``` or the address that is presented in your console. On the webpage you can dynamically setup experiments and get live results. There is currently no switch to run the ISPD in the web dashboard.

### CLI Experiment runner

You can specify one or multiple experiments in a file called ```experiments.csv```. We included several example setups in the ```report_experiments``` folder. After specification you can execute all experiments by running

```shell
python3 run\_experiments.py
```

which will automatically put the results in the ```data``` folder with labelling.

#### Experiment Format
Experiments in experiments.csv can handle two special cases:
1. sets of the form a:b:c -> one experiment for each of the values
2. ranges of the form a;b;c -> one experiment for each of the values in range(a,b,c) where a is the start b is the end and c is the step size

## Credits