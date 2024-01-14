PROG = histogram histogram_omp_outer histogram_omp_inner histogram_omp_collapse histogram_omp_reduce histogram_cuda

CFLAGS = -Wall -g -O3 -fopenmp
LDLIBS = -lm

# Specify CUDA-related paths and flags
CUDA_HOME = /opt/nvidia/hpc_sdk/Linux_x86_64/23.9/cuda/11.8
NVCC = /usr/bin/nvcc
NVCFLAGS = -I$(CUDA_HOME)/include

# Specify CUDA-related libraries
CUDANVIDIA = /usr/lib/nvidia
LDFLAGS_CUDA = -L$(CUDA_HOME)/lib64 -L$(CUDANVIDIA)

.phony: all clean

all: $(PROG)

clean:
	rm -fv $(PROG) *.o

# Compilation rule for CUDA source files
%.o: %.cu
	$(NVCC) $(NVCFLAGS) -c -o $@ $<

# Linking rule for CUDA programs
histogram_cuda: histogram_cuda.o
	$(NVCC) $(LDFLAGS_CUDA) -o $@ $^ $(LDLIBS)

