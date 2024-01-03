# Scripts

This section is for the scripts which compute blindspots around a truck and display them in CAD.

## Setup

### Requirements
Our software runs partially as a Python script, and partially in FreeCAD. As a result, using the script requires the [installation of FreeCAD][https://www.freecad.org/downloads.php]. Additionally, we require some packages in Python, outlined in `requirements.txt`. These can be installed by installing Python and pip, the Python package manager, from online, then running `pip install -r requirements.txt`

### Constants
There is a file called `constants.py`, where users can define constants such as where the driver is situated, which components of the truck are opaque vs. see through, and also where the folder is located. Please adjust these to each truck file and each user accordingly before running.

## Code Overview and Usage

The main product of this project is found in three files:

### ```exportMesh.py```
This is the first file to run in the workflow, and it takes as input a .FCStd file or similar FreeCAD input file (any CAD file should work when opened in FreeCAD) and converts all objects in the file into Python (Numpy) objects. These can then be used externally, as there are some issues with more complex operations in FreeCAD. These files are then stored locally. To run this script, open the truck file in FreeCAD and open this file in FreeCAD as well, then run the file as a macro (the green arrow at the top).

### ```checkIntersection.py```
This is the second file in the workflow. It checks over all of the converted files about the truck, which are now more Python-operable, and uses a package called  ```trimesh``` to verify if a range of sightlines are or are not blocked by them. It then saves the sightlines and the corresponding results (blocked vs unblocked).

### ```visualIntersect.py```
This is the final file in the workflow. After running the previous two files, opening this file and running it in FreeCAD alongside the original truck file should create a visualization of blindspots around the truck. 