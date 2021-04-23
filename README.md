# MRI-SI Visualization
> View and Interact with Si-29 MRI Images

## General info
This project is courtesy of [Dr. Farach-Carson's](https://www.researchgate.net/profile/Mary_Farach-Carson) UT-Health Research Laboratory. This module aids
in overlaying Si-29 MRI images over traditional H MRI images.


## Technologies
* Choose, Processes and Visualize co-registered 1H and 29Si files using a Python3 GUI built completely using PyQt5.

## Setup
To install, simply clone this repository to your computer and navigate to that folder.
(alternatively, download the code as a .zip and extract it)

**Detailed installation and usage tutorials can be found at my YouTube Page:**
[Tutorials](https://www.youtube.com/watch?v=qvJPAI6tzg8)

* Dependencies:
This code requires the Python 3 and following dependencies:
* PyQt5
* Numpy
* Pillow
* Matplotlib
* Pandas (including xlrd functionality)

If the code fails, please ensure these packages are installed using the `pip3` command.
Depending on the way Python was installed, users might need to install these packages
as `sudo`.

## Code Examples
This module contains three files:

* `main.py` - run this script in order to choose, process, and view H/Si MRI files. This script is best run through the command line in case of errors.

**WARNING** - the main.py file makes os system calls to the view_files.py and main_window_6_23.py scripts. This means all three files must remain in the same folder.

* `view_files.py` - this script contains the interactive matplotlib code used to visualize processed images. This script is **NOT DESIGNED** to be run separately.

* `GUI_Window.py` - this script contains the PyQt5 implementation of the GUI.


## Features
* Interactively load, process, and view co-registered 1H and 29Si images.
* Save images as .pkl files to a timestamped folder for later use

To-do list:
* General Bug Fixes
* Improve Documentation

## Status
Project is still in progess as of 7/1/2020.

## Inspiration
This project is courtesy of Dr. Farach-Carson's UT-Health Research Laboratory.
## Contact
Created by Duncan Salmon. I am a EE graduating from Rice University in 2021 - feel free to contact me at drs3@rice.edu!
