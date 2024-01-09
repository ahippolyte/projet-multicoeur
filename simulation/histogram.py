#!/usr/bin/env python3

import os
import numpy as np
import pandas as pd

# SIMULATION PARAMETERS #

# Relative path to executables
BINARY_PATH = "../histogram/"

# CSV output file
DATA_DIRECTORY = "data"
DATA_FILE = "histogram.csv"

# Number of repetitions for each experience
repetitions = 10

# Parameters for the simulation :
# as kernels, versions and sizes are tables,
# the simulation is going to make an experience
# with each combination of these parameters
parameters = {
    "kernels": ["histogram", "histogram_omp_outer", "histogram_omp_inner", "histogram_omp_collapse", "histogram_omp_reduce"],
    "size": [2**i for i in range(15)],
    "schedule": ["static", "dynamic", "guided"],
    "nb_threads": [i for i in range(1,25,2)]
}
#-----------------------#

f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
f.write("kernel,threads,schedule,array_len,nb_bins,nb_repeat,rep,timing,check_status\n")
f.close()

print("Starting simulation...")

for kernel in parameters["kernels"]:
    if kernel == "histogram":
        for size in parameters["size"]:
            command = BINARY_PATH + "histogram --array-len " + str(size) + " --nb-bins " + str(size) + " --nb-repeat " + str(repetitions)
            print(command)
            output = os.popen(command).read()
            lines = output.splitlines()
            del lines[0]
            for line in lines:
                newline = str(kernel) + "," + "1" + "," + "none" + "," + line
                f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
                f.write(newline + "\n")
                f.close()
    else:
        for threads in parameters["nb_threads"]:
            for schedule in parameters["schedule"]:
                for size in parameters["size"]:
                    command = "OMP_SCHEDULE=" + str(schedule) + " OMP_NUM_THREADS=" + str(threads) + " " + BINARY_PATH + str(kernel) + " --array-len " + str(size) + " --nb-bins " + str(size) + " --nb-repeat " + str(repetitions)
                    print(command)
                    output = os.popen(command).read()
                    lines = output.splitlines()
                    del lines[0]
                    for line in lines:
                        newline = str(kernel) + "," + str(threads) + "," + str(schedule) + "," + line
                        f = open(DATA_DIRECTORY + "/" + DATA_FILE, "a")
                        f.write(newline + "\n")
                        f.close()
print("Simulation done.")