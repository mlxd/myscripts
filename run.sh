#!/bin/bash

# Create a hostfile to set the number of MPI processes we want 
# to create (allows us to oversubscribe MPI processes to cores)
# the number of which are passed as an argument to ./run.sh
echo "localhost slots=$1" > hostfile

#Make sure mpi4py is installed before running
mpirun --hostfile ./hostfile -n $1 python2 ./mpi_reduce_time.py > reduce_timing.dat

sh ./plot_mpi_timing.sh ./reduce_timing.dat
