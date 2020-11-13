'''
Created on November 12, 2020
@author: Ruhar 
'''
#IMPORTING ALL THE REQUIRED MODULES and loading data from file
#! /usr/local/bin/env python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import matplotlib as mpl
data=pd.read_csv('ares4.dat', sep='\s*', header=None)
x=data[0]
y=data[1]
z=data[2]
xq=np.linspace(np.min(x), np.max(x))
yq=np.linspace(np.min(y), np.max(y))
[X, Y] = np.meshgrid(xq, yq)
Z=griddata((x,y),z,(X,Y),method='cubic')

#Plotting free energy surface
fig=plt.figure(1, figsize=(12,9))
ax = fig.add_subplot(111, projection='3d')
surf=ax.plot_trisurf(x,y,z,cmap=cm.jet,linewidth=0, antialiased=False)
ax.set_xlim3d(-180, 180)
ax.set_ylim3d(-180, 180)
ax.set_zlim3d(0, max(z))
plt.xlabel('Phi')
plt.ylabel('Psi')
cbar  =fig.colorbar(surf, shrink=0.5)
cbar.set_label('Free Energy (kJ/Mol)',size=15,fontname='Times New Roman')
plt.tick_params(axis='both',which='minor',labelsize=20,length=20)
cbar.ax.tick_params(labelsize=15,length=20)

#To save the figure in jpg format
fig.savefig('AlaFree_energySurface.jpg')
plt.show()

#Plotting Contour Plot
fig = plt.figure()
ax=plt.subplot(111)
levels = np.linspace(0,14,7)
Z=np.clip(Z, 1, 14)
cf = ax.contourf(X, Y, Z,vmax=np.max(Z), vmin=np.min(Z),levels=levels)
cbar  =fig.colorbar(cf)
cbar.set_label('Free Energy (kJ/Mol)',size=15,fontname='Times New Roman')
plt.xlabel('Phi')
plt.ylabel('Psi')
plt.xticks(size='15')
plt.yticks(size='15')
plt.show()

#To save the figure in jpg format
fig.savefig('AlaFree_energyContour.jpg')
plt.show()
