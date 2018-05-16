#This file plots the results from the MPI timing runs
import sys
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import matplotlib.markers as mkr

plt_style='ggplot'
plt.rcParams['font.size'] = 11
plt.rcParams['font.family'] = 'serif'
plt.rcParams['axes.labelsize'] = 11
plt.rcParams['axes.labelweight'] = 'bold'
plt.rcParams['xtick.labelsize'] = 9
plt.rcParams['ytick.labelsize'] = 9
plt.rcParams['figure.titlesize'] = 12

#We begin by loading the CSV file of rank pairings and times into the appropriate format
StartStr = str(sys.argv[1])
EndStr = str(sys.argv[2])

start = np.loadtxt(open(StartStr), delimiter=',', dtype={'names': ('A','B','t'), 'formats':('i4','i4','f8')})
end = np.loadtxt(open(EndStr), delimiter=',', dtype={'names': ('A','B','t'), 'formats':('i4','i4','f8')})

ds=[{'%s:%s'%(a,b): (a,b,t) for a,b,t in zip(start['A'],start['B'],start['t']) }]
de=[{'%s:%s'%(a,b): (a,b,t) for a,b,t in zip(end['A'],end['B'],end['t']) }]

#We take note of the starting time over all ranks as a 0 offset
t0 = np.min(start['t'])

#3D Rank A:B vs time diagram
fig = plt.figure()
plt.style.use(plt_style)
fig.clf()
ax = fig.add_subplot(111, projection='3d')
ax.set_zlabel('time [s]')
ax.set_ylabel('Rank To Merge')
ax.set_xlabel('Rank Base')

#Plot the recorded times and connect ranks that have been merged toegther
for a in ds[0].keys():
    ax.scatter( ds[0][a][0], ds[0][a][1], ds[0][a][2]-t0, c='r', marker='o') #Plot start
    ax.scatter( de[0][a][0], de[0][a][1], de[0][a][2]-t0, c='b', marker='x') #Plot end
    ax.plot( [ ds[0][a][0], de[0][a][0] ], [ ds[0][a][1], de[0][a][1] ], [ ds[0][a][2] - t0, de[0][a][2] - t0 ], c='k') #Draw line between start and finish
ax.set_zlim3d([ 0, np.max(end['t']) - t0 ])
ax.set_ylim3d([ np.min([end['A'], end['B']]), np.max([end['A'],end['B']]) ])
ax.set_xlim3d([ np.min([end['A'], end['B']]), np.max([end['A'],end['B']]) ])
plt.show()
#Save the 3D plot output
plt.savefig('3d_%s_%s.pdf'%(StartStr, EndStr))
plt.clf()

plt.style.use( plt_style )
#2D connections diagram
#Draw lines to mark the MPI ranks
for ii in xrange(np.max([start['A'],start['B']])):
  plt.axhline(ii, xmin=0, xmax=1, linewidth=0.5)

#Draw lines between the start and end for reducing 2 data sets
for a in ds[0].keys():
  
  plt.plot( [ ds[0][a][2] - t0, de[0][a][2] - t0] , [ds[0][a][1], de[0][a][0]], linestyle='-', linewidth=0.5, c='k', alpha=0.8)
  plt.scatter( start['t'] - t0, start['B'], marker='x', c='r', alpha=0.8)
  plt.scatter( end['t'] - t0, end['A'], marker='o', c='b', alpha=0.8)

plt.xlabel('time [s]')
plt.ylabel('MPI rank')
plt.title('%s_%s'%(StartStr, EndStr))
plt.xlim([ 0, np.max(end['t']) - t0 ])
plt.ylim([ np.min([end['A'], end['B']]), np.max([end['A'],end['B']]) ])
plt.show()
#Save the 2D plot output
plt.savefig('2d_%s_%s.pdf'%(StartStr, EndStr))
