#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS #

# Relative path to executables
BINARY_PATH = "../../stencil/"

# CSV output file
DATA_DIRECTORY = "../data"
DATA_FILE = "stencil_avx2.csv"

# Number of repetitions for each experience
repetitions = 10

# Parameters for the simulation :
# as kernels, versions and sizes are tables,
# the simulation is going to make an experience
# with each combination of these parameters
parameters = {
    "kernels": ["stencil_avx2", "stencil"],
    "mesh-width": [5*i for i in range(1,11)] + [100, 1000, 2000],
    "mesh-width": [5*i for i in range(1,11)] + [100, 1000, 2000],
}
#-----------------------#

f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
f.write("kernel,mesh_width,mesh_height,nb_iterations,nb_repeat,rep,timing,check_status\n")
f.close()

print("Starting simulation...")

for kernel in parameters["kernels"]:
    for width in parameters["mesh-width"]:
        for height in parameters["mesh-height"]:
            command = BINARY_PATH + str(kernel) + " --mesh-width " + str(width) + " --mesh-height " + str(height) + " --nb-repeat " + str(repetitions)
            print(command)
            output = os.popen(command).read()
            lines = output.splitlines()
            del lines[0]
            for line in lines:
                newline = str(kernel) + "," + line
                f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
                f.write(newline + "\n")
                f.close()
print("Simulation done.")