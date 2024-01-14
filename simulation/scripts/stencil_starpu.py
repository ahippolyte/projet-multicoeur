#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS #

# Relative path to executables
BINARY_PATH = "../../stencil/"

# CSV output file
DATA_DIRECTORY = "../data"
DATA_FILE = "stencil_starpu.csv"

# Number of repetitions for each experience
repetitions = 10

# Parameters for the simulation :
# as kernels, versions and sizes are tables,
# the simulation is going to make an experience
# with each combination of these parameters
parameters = {
    "kernels": ["stencil", "stencil_starpu"],
    "mesh-size": [2**i for i in range(9, 13)]
}
#-----------------------#

f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
f.write("kernel,nb_partitions,mesh_width,mesh_height,nb_iterations,nb_repeat,rep,timing,check_status\n")
f.close()

print("Starting simulation...")

for kernel in parameters["kernels"]:
    if kernel == "stencil":
        for size in parameters["mesh-size"]:
            command = BINARY_PATH + str(kernel) + " --mesh-width " + str(size) + " --mesh-height " + str(size) + " --nb-repeat " + str(repetitions)
            print(command)
            output = os.popen(command).read()
            lines = output.splitlines()
            del lines[0]
            for line in lines:
                newline = str(kernel) + ",1," + line
                f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
                f.write(newline + "\n")
                f.close()
    else :
        for size in parameters["mesh-size"]:
            nb_partitions = [2**i for i in range(1, int(np.log2(size)))] + [size-2]
            for partitions in nb_partitions:
                command = BINARY_PATH + str(kernel) + " --nb-partitions " + str(partitions) + " --mesh-width " + str(size) + " --mesh-height " + str(size) + " --nb-repeat " + str(repetitions)
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