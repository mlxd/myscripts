#!/bin/bash
for ii in MPI_REDUCE MPI_REDUCE_CALL; do
  #Extract the start timing data for the above strings
  echo $ii
  cat $1 \
    | grep "$ii\s" \
    | tr ';' '\n' \
    | grep "$ii\s" \
    | grep " START" \
    | awk '{ print $3,$4}' \
    | sed 's/RANK=//; s/:/,/; s/ TIME=/,/' \
    > ./REDUCE_${ii}_START.csv
  #Extract the end timing data for the above strings
  cat $1 \
    | grep "$ii\s" \
    | tr ';' '\n' \
    | grep "$ii\s" \
    | grep " END" \
    | awk '{ print $3,$4}' \
    | sed 's/RANK=//; s/:/,/; s/ TIME=/,/' \
    > ./REDUCE_${ii}_END.csv
  #Pass the extracted data into the python script to generate the timing plot
  python2 plot_mpi_timing.py REDUCE_${ii}_START.csv REDUCE_${ii}_END.csv
done
