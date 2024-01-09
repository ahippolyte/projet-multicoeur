PROG = histogram histogram_omp_outer histogram_omp_inner histogram_omp_collapse histogram_omp_reduce

CFLAGS = -Wall -g -O3 -fopenmp
LDLIBS = -lm

.phony: all clean

all: $(PROG)

clean:
	rm -fv $(PROG)
