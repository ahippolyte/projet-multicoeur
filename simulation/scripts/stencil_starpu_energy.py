#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS #

# Relative path to executables
BINARY_PATH = "../../stencil/"

# CSV output file
DATA_DIRECTORY = "../data"
DATA_FILE = "stencil_starpu_energy.csv"

# Number of repetitions for each experience
repetitions = 10

# Parameters for the simulation :
# as kernels, versions and sizes are tables,
# the simulation is going to make an experience
# with each combination of these parameters
parameters = {
    "kernels": ["stencil", "stencil_starpu"],
    # "kernels": ["stencil_starpu"],
    "mesh-size": [2**i for i in range(9, 13)]
}
#-----------------------#

f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
f.write("kernel,nb_partitions,mesh_size,nb_repeat,cores,dram\n")
f.close()

print("Starting simulation...")

for kernel in parameters["kernels"]:
    if kernel == "stencil":
        for size in parameters["mesh-size"]:
            command = BINARY_PATH + str(kernel) + " --mesh-width " + str(size) + " --mesh-height " + str(size) + " --nb-repeat " + str(repetitions)
            likwid = "likwid-perfctr -c 0,1 -g PWR_PKG_ENERGY:PWR0,PWR_DRAM_ENERGY:PWR3 \"" + command + "\""
            print(likwid)
            output = os.popen(likwid).read()
            # print(output)
            lines = output.splitlines()
            cores_line = lines[22]
            dram_line = lines[23]
            cores_energy = (float)(cores_line.split("|")[3]) + (float)(cores_line.split("|")[4])
            dram_energy = (float)(dram_line.split("|")[3]) + (float)(dram_line.split("|")[4])
            newline = str(kernel) + ",1," + str(size) + "," + "10" + "," + str('%.5f' % cores_energy) + "," + str('%.5f' % dram_energy)
            f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
            f.write(newline + "\n")
            f.close()
    else :
        for size in parameters["mesh-size"]:
            nb_partitions = [2**i for i in range(1, int(np.log2(size)))] + [size-2]
            rest = [510, 1022, 2046]
            for i in rest:
                if i < size-2 :
                    nb_partitions += [i]
            for partitions in nb_partitions:
                command = BINARY_PATH + str(kernel) + " --nb-partitions " + str(partitions) + " --mesh-width " + str(size) + " --mesh-height " + str(size) + " --nb-repeat " + str(repetitions)
                likwid = "likwid-perfctr -c 0,1 -g PWR_PKG_ENERGY:PWR0,PWR_DRAM_ENERGY:PWR3 \"" + command + "\""
                print(likwid)
                output = os.popen(likwid).read()
                # print(output)
                lines = output.splitlines()
                cores_line = lines[22]
                dram_line = lines[23]
                cores_energy = (float)(cores_line.split("|")[3]) + (float)(cores_line.split("|")[4])
                dram_energy = (float)(dram_line.split("|")[3]) + (float)(dram_line.split("|")[4])
                newline = str(kernel) + "," + str(partitions) + "," + str(size) + "," + "10" + "," + str('%.5f' % cores_energy) + "," + str('%.5f' % dram_energy)
                f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
                f.write(newline + "\n")
                f.close()
print("Simulation done.")