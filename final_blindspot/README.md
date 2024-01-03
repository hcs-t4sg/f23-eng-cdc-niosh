# Scripts

This section is for the scripts which compute blindspots around a truck and display them in CAD.

## Setup

### Requirements
Our software runs partially as a Python script, and partially in FreeCAD. As a result, using the script requires the [installation of FreeCAD](https://www.freecad.org/downloads.php). Also, to be compatible with FreeCAD, we need Python 3.8 on Windows. Additionally, we require some packages in Python, outlined in `requirements.txt`. These can be installed by installing Python and pip, the Python package manager, from online, then running `pip install -r requirements.txt`.

### Constants
There is a file called `constants.py`, where users can define constants such as where the driver is situated, which components of the truck are opaque vs. see through, and also where the folder is located. Please adjust these to each truck file and each user accordingly before running.

Specifically, variables `FREECADPATH` and `ABS_PATH_ROOT` are user-dependent and need only be updated at installation. Variables `FILENAME`, `DRIVER_HEAD`, `TRUCK_NAME`, `FULL_LIST`, and `CAB` are file-dependent and specify the model of the truck, so these should be updated whenever a new model is used. Finally, variables `THETAS` and `PHIS` specify the resolution of our blindspot analysis and should be updated accordingly. 

## Code Overview and Usage

The main product of this project has been split into two files:[^1]

### ```preprocessing.py```
This is the first file to run in the workflow. It exports objects from FreeCAD and uses a package called  ```trimesh``` to verify if a range of sightlines are or are not blocked by them. It then saves the sightlines and the corresponding results (blocked vs unblocked).[^2] To run this script, make sure you have installed the requirements above, and run `python preprocessing.py` in its directory on your terminal. 

### ```visualization.py```
Opening this file and running it in FreeCAD alongside the original truck file should create a visualization of blindspots around the truck. To run this script, open the truck file in FreeCAD and open this file in FreeCAD as well, then run the file as a macro (the green arrow at the top).

[^1]: Unfortunately, [FreeCAD does not support the use of its GUI software in external scripts and the use of third-party packages in its macro scripts](https://github.com/FreeCAD/FreeCAD-documentation/blob/main/wiki/FreeCAD_Scripting_Basics.md). As a result, our process is divided between the component using ```trimesh``` and that using FreeCAD's GUI. 

[^2]: For debugging purposes, file "log.txt" will be generated every time this file is run. 

## Sensors

In addition to the main blindspot visualization, we have begun work on sensors. ```create_sensors.py``` contains code which generates bounding boxes and sensor fields of view given a set of sensor specs and user-defined locations for these sensors. However, these sight lines are currently not included in the blindspot computation.