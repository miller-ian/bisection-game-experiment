# Bisection Search Experiment
6.804 Final Project 2020 (Ian Miller and Quilee Simeon)

## Table of Contents
- [Getting Started](#getting-started)
    - [Activating the Environment](#activating-the-environment)
    <!-- - [Windows Setup](#windows-setup)
    - [Mac Setup](#mac-setup)
    - [Linux Setup](#linux-setup) -->
- [Overview](#overview)
## Getting Started

### Activating the Environment
While in the directory, run the following to 
```
conda env create -f environment.yml
conda activate bisection_game
```

### Launching the Experiment
Executing the following will open a psychopy window and let you play the experiment as a respondent.
```
python3 main_lastrun.py
```

## Overview

This experiment is intended to measure human respondents' error in decision-making in a simple bisection-search game. 

For simple games like this one, there is a mathematically optimal decision to make at every decision point. We intend to speculate on why it is that humans make locally suboptimal decisions. 

Respondents' input and data is saved and stored in the "data" directory. Currently, an example run is stored there. The log file is the easiest to read.