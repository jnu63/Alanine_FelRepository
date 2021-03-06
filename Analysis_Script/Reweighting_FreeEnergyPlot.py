'''
Created on May 1, 2013

@author: wsinko
'''
#! /usr/bin/env python

import scipy
import numpy as np
import sys
import matplotlib.pyplot as plt
import csv
from argparse import ArgumentParser


print ("2DFreeEnergyPlog.py  RUNNNING!")
print ("Script will process scaled MD data, accelerated MD data, and classical MD data and output 2 Variable Free energy histograms")
print ("Input files required are a 2D variable file, if sMD or aMD was used the a weights file is needed with a weight coorresponding to each data point")
print ("  ")
print ("Author: Bill Sinko")
print (" ")

###########MAIN
def main():
    args = cmdlineparse()   
    
    inputfile=loadfiletoarray(args.input)
    length=inputfile[:,0]
    
    rows = len(length)
    weights = weightparse(rows, args)
    if args.Xdim:
        binsX= assignbins(args.Xdim, args)
    else:
        binsX= assignbins([-180,180], args)  ## Default bin size
    if args.Ydim:
        binsY= assignbins(args.Ydim, args)
    else:
        binsY= assignbins([-180,180], args)  ## Default bin size

##HISTOGRAM EVERYTHING
    hist2, newedgesX, newedgesY = np.histogram2d(inputfile[:,0], inputfile[:,1], bins = (binsX, binsY), weights=weights )
    cb_max=14  ## MAX VALUE TO SET ALL INFINITY VALUES TOO AND TO SET THE COLORBAR TO
    hist2=prephist(hist2, cb_max)
    cbar_ticks=[0, cb_max*.20, cb_max*.40, cb_max*.60, cb_max*.80, cb_max]

###PLOTTING FUNCTION FOR FREE ENERGY FIGURE
    plt.figure(2, figsize=(11,8.5))
    extent = [newedgesX[0], newedgesX[-1], newedgesY[-1], newedgesY[0]]
    print (extent)
    plt.imshow(hist2.transpose(), extent=extent, interpolation='gaussian', cmap='viridis')
    cb = plt.colorbar(ticks=cbar_ticks, format=('% .1f'), aspect=10) # grab the Colorbar instance
    cb.set_label('Free Energy (kJ/Mol)',size=15,fontname='Times New Roman')
    imaxes = plt.gca()
    plt.axes(cb.ax)
    plt.clim(vmin=0,vmax=cb_max)
    plt.yticks(fontsize=18)
    plt.axes(imaxes)
    axis=(min(binsX), max(binsX), min(binsY), max(binsY))
    plt.axis(axis)
    plt.xlabel('Phi', size=15)
    plt.ylabel('Psi', size=15)
    plt.xticks(size='18')
    plt.yticks(size='18')
    plt.savefig('ReweightingFreeEnergy_plot.png',bbox_inches=0)
    print ("FIGURE SAVED ReweightingFreeEnergy_plot.png")
    

########READ datafiles and print weights

def cmdlineparse():
    parser = ArgumentParser(description="command line arguments")
    parser.add_argument("-input", dest="input", required=True, help="2D input file", metavar="<2D input file>")
    parser.add_argument("-job", dest="job", required=True, help="Reweighting method to use: accepted methods are: <noweight>, <weighthist>, <amdweight>", metavar="<Job type reweighting method>")
    parser.add_argument("-weight", dest="weight", required=False, help="weight file", metavar="<weight file>")
    parser.add_argument("-Xdim", dest="Xdim", required=False, nargs="+", help="Xdimensions", metavar="<Xmin Xmax >")
    parser.add_argument("-Ydim", dest="Ydim", required=False, nargs="+", help="Ydimension", metavar="<Ymin Ymax >")
    parser.add_argument("-disc", dest="disc", required=False,  help="Discretization size", metavar="<discretization >")
    args=parser.parse_args()
    return args
    
    
def loadfiletoarray(file):
    loaded=np.loadtxt(file, usecols=[0,1])
    print ("DATA LOADED    "+file)
    return loaded

def weightparse(rows, args):
    if args.weight :
        weights=np.loadtxt(args.weight)
    if args.job == "weighthist":
        weights=weights
    elif args.job == "amdweight":
        weights = np.exp(weights)
    elif args.job == "noweight":
        weights = np.zeros(rows)
        weights = weights + 1
    else:
        print ("ERROR JOBTYPE"+ args.job+ " NOT RECOGNIZED")
        del weights
    return weights

def assignbins(dim, args):

    minimum=float(dim[0])
    maximum=float(dim[1])
    if args.disc:
        disc=float(args.disc)
    else :
        disc = 6
    bins =np.arange(minimum,(maximum+disc),disc)
    return bins

def prephist(hist2, cb_max):
    hist2=.5961*np.log(hist2) ####Convert to free energy in Kcal/mol
    hist2=np.max(hist2)-hist2  ## zero value to lowest energy state
    ##remove infinity values from free energy plot
    temphist=hist2
    #max value to set infinity values to is cb_max
    for y in range(len(temphist[0,:])):
        for x in range(len(temphist[:,0])):
            if np.isinf(temphist[x,y]):
                temphist[x,y]=cb_max
    return temphist



if __name__ == '__main__':
    main()
    
