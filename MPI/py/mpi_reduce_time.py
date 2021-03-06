from __future__ import division
import sys,time
from time import time as t
from itertools import product
import numpy as np

#Simple class to hold our data
class Data():
    def __init__(self):
        self.a = 0
        self.b = 0
        self.c = 0

        self.d_list = []
        self.e_dict = {}

#User defined MPI reduce operator. Requires 2 data arguments, and a datatype argument
def mpi_reduce_op(data0, data1, datatype):
    print 'MPI_REDUCE START RANK=%d:%d TIME=%f\n'%(data0.rank, data1.rank, t() )
    data0.a += data1.a
    data0.b += data1.b
    data0.c += data1.c

    data0.d_list.extend( data1.d_list )
    data0.e_dict = { key : data0.e_dict.get(key, 0) + data1.e_dict.get(key, 0) for key in set( data0.e_dict.keys() ) | set( data1.e_dict.keys() ) }

    print 'MPI_REDUCE END RANK=%d:%d TIME=%f\n'%(data0.rank, data1.rank, t() )
    return data0

#Run the MPI reduce example
def run():
    from mpi4py import MPI
    comm = MPI.COMM_WORLD
    rank = comm.Get_rank()
    size = comm.Get_size()

    #Create user-defined MPI reduce op
    reduce_op = MPI.Op.Create(mpi_reduce_op, commute=True)

    #Create an empty data object
    data = Data()

    # Create variables with the new data object
    if rank == 0:
        data.a = 1
        data.b = 1.0
        data.c = 1e-12

        data.d_list = ['a','b','c','d']
        data.e_dict = { "".join(x):1.0 for x in product('abcd', repeat=2) } 

    #Send the same data to all other ranks
    data = comm.bcast(data, root = 0)

    #Tag the data object with the MPI rank
    data.rank = rank

    #Call the reduce operation we would like to time
    print "MPI_REDUCE_CALL START RANK=%d:%d TIME=%f#"%(rank,rank, t())
    data = comm.reduce(data, op=reduce_op, root=0)
    print "MPI_REDUCE_CALL END RANK=%d:%d TIME=%f#"%(rank,rank, t())
    comm.Barrier()
    MPI.Finalize()
    if rank==0:
        assert ( data.a == size )
        assert ( np.allclose(data.b, size*1.0) )
        assert ( np.allclose(data.c, size*1e-12) )
        assert ( len(data.d_list) == size*4 )
        assert ( all(np.allclose(v, size*1.0) for v in data.e_dict.values()) )
        print "Value checks passed."
        print "# sum(data.a)=%d     sum(data.b)=%f      sum(data.c)=%e"%(data.a,data.b,data.c)
        print "# Concatenated data.d_list=", data.d_list
        print "# Combined data.e_dict=", data.e_dict

if (__name__ == "__main__"):
    run()
