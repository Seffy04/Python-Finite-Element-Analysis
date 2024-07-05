# Python-Finite-Element-Analysis
This project was made for my computational physics lab in Franklin and Marshall College where I used numerical methods to perform structural analysis on beam bending.

## Files in the most recent build:
Build 3 contains multiple files, each with a certain function:

### Brain_2_no_interface.py 
As the title says, this is the brains of the project. This is a version of the project in which all the varried parameters are varried from within the code. It produces a subplot in a window including 4 (or 5) different plots showing:
- Weight as a function of length
- Shear as a function of length
- Moment as a function of length
- Bending Slope as a function of length
- Bending displacement as a function of length

You'll find comments in the code guiding you as to how to perform changes to the plots. The currently available parameters to vary are:
- Beam Shape
- Support Type (WIP)
- Load type (WIP, will add more types)
- Weight value
- Length of board
- Board mass (if considered)
- Young's modulus, the program will tell you your minimum Young's modulus value to avoid breaking the beam (bending displacement will become larger than the length itself if broken.)

### odeSolvers.py
This module includes a couple of different functions used to solve ordinary differential equations numerically.

### MOI.py
A module containing multiple functions with the purpose of calculating the area moment of inertia based on the beam's shape and dimension. (WIP, will add more shapes)

### Terminal_user_prompt.py
A work in progress for future builds, just a basic prompt asking you for your parameters. Might replace with a tkinter window.

