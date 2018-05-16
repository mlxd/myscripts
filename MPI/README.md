# User defined MPI reduce with mpi4py

This is a simple script to create and test a user-defined MPI reduce operation. The output file format will be saved with timing data and ranks, which is then used to generate a plot of the connecting ranks in the reduce ( o <--> x ). While it is not possible to properly time the operations without some inspection and profiling methods, I have defined a simple method to demonstrate the reduce operation in practice, as the rank pairings are recorded.

The code is run as:

```bash
./run.sh <number_of_ranks>
```

where the number of ranks can be more than the cores available (oversubscription of ranks to cores will not give the best performance, but works as a demonstration). Plots in 3D will be displayed (and subsequently saved) of the ranks vs time, with a line drawn connecting the start and end of the process. 2D plots will also be generated which can more easily be used to observe the merging ops (for low rank numbers).
