#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS #

# Relative path to executables
BINARY_PATH = "../../stencil/"

# CSV output file
DATA_DIRECTORY = "../data"
DATA_FILE = "stencil_avx2_energy.csv"

# Number of repetitions for each experience
repetitions = 10

# Parameters for the simulation :
# as kernels, versions and sizes are tables,
# the simulation is going to make an experience
# with each combination of these parameters
parameters = {
    "kernels": ["stencil_avx2", "stencil"],
    "mesh-width": [5*i for i in range(1,11)] + [100, 1000, 2000],
    "mesh-height": [5*i for i in range(1,11)] + [100, 1000, 2000],
}
#-----------------------#

f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
f.write("kernel,mesh_width,mesh_height,nb_repeat,cores,dram\n")
f.close()

print("Starting simulation...")

for kernel in parameters["kernels"]:
    for width in parameters["mesh-width"]:
        for height in parameters["mesh-height"]:
            command = BINARY_PATH + str(kernel) + " --mesh-width " + str(width) + " --mesh-height " + str(height) + " --nb-repeat " + str(repetitions)
            likwid = "likwid-perfctr -c 0,1 -g PWR_PKG_ENERGY:PWR0,PWR_DRAM_ENERGY:PWR3 \"" + command + "\""
            print(likwid)
            output = os.popen(likwid).read()
            # print(output)
            lines = output.splitlines()
            cores_line = lines[22]
            dram_line = lines[23]
            # print(cores_line)
            # print(dram_line)
            cores_energy = (float)(cores_line.split("|")[3]) + (float)(cores_line.split("|")[4])
            dram_energy = (float)(dram_line.split("|")[3]) + (float)(dram_line.split("|")[4])
            newline = str(kernel) + "," + str(width) + "," + str(height) + "," + "10" + "," + str('%.5f' % cores_energy) + "," + str('%.5f' % dram_energy)
            f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
            f.write(newline + "\n")
            f.close()
print("Simulation done.")