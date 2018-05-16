#!/bin/bash

# Create a hostfile to set the number of MPI processes we want 
# to create (allows us to oversubscribe MPI processes to cores)
# the number of which are passed as an argument to ./run.sh
if [[ $(python -c "from mpi4py import MPI; v = MPI.get_vendor(); print 'mpich' in v[0].lower()") == "True" ]];
then
  echo "localhost:$1" > hostfile
else
  echo "localhost slots=$1" > hostfile
fi
ranks=$1

#Make sure mpi4py is installed before running
which python2 &> /dev/null
if ! [[ $? -eq 0 ]];then
    echo "python2 not found. Please ensure it is installed and available on your path."
fi
if [[ $# -gt 0 && "${ranks}" -gt 1 ]];then
    mpirun --hostfile ./hostfile -n ${ranks} python2 ./mpi_reduce_time.py > reduce_timing.dat
    sh ./plot_mpi_timing.sh ./reduce_timing.dat
else echo "Please provide the number of MPI ranks >2 ( e.g. ./run.sh 4 )"
fi

