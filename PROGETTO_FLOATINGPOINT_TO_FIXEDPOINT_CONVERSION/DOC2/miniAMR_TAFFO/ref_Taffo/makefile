CC   = taffo
CCBASE = clang
LD   = clang
CPPFLAGS = -I.
CFLAGS = -O3
LDFLAGS =
LDLIBS = -lm

TARGET = miniAMR.x
TARGET_CLEAN = miniAMR.base

# Add MPI flags
MPIFLAGS = $(shell mpicc --showme:compile)
MPILDFLAGS = $(shell mpicc --showme:link)

# Combine MPI flags with existing flags
CFLAGS   += $(MPIFLAGS)
LDFLAGS  += $(MPILDFLAGS)

SRCS := $(wildcard *.c)

.PHONY: all clean

all: $(TARGET)
base: $(TARGET_CLEAN)

$(TARGET): $(SRCS)
	$(CC) $(CFLAGS) $(LDLIBS) $(LDFLAGS) $^ -o $@

$(TARGET_CLEAN): $(SRCS)
	$(CCBASE) $(CFLAGS) $(LDLIBS) $(LDFLAGS) $^ -o $@

clean:
	rm -f $(TARGET)
