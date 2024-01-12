PROG = stencil stencil_starpu stencil_starpu_arnaud stencil_avx2

STARPU_VERSION = starpu-1.3
CFLAGS = -Wall -g -O3 -march=native -mavx2
LDLIBS = -lm

CFLAGS += $(shell pkg-config --cflags $(STARPU_VERSION))
LDLIBS += $(shell pkg-config --libs $(STARPU_VERSION))

.phony: all clean

all: $(PROG)

clean:
	rm -fv $(PROG)
