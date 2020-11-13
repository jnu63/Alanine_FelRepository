'''
Created on Feb 20, 2013

@author: wsinko
'''

import numpy as np
import sys
import math
import csv
import multiprocessing as multiproc
import time
from argparse import ArgumentParser

def cmdlineparse():
    parser = ArgumentParser(description="command line arguments")
    parser.add_argument("-input", dest="input", required=True, help="2D input file", metavar="<N-Dimensional input file>")
    parser.add_argument("-weight", dest="weight", required=True, help="weight output file", metavar="<weight file>")
    parser.add_argument("-lambda", dest="lambdavalue", required=True,  help="lambda value", metavar="<lambda >")
    parser.add_argument("-disc", dest="disc", required=True,  help="Discretization size", metavar="<discretization >")
    parser.add_argument("-nprocs", dest="nprocs", required=False,  help="number of processors", metavar="<nprocs >")
    args=parser.parse_args()
    return args

def main():
    
    print ("Script will process scaled MD data and output weights for use in weighted histograms")
    print ("")
    print ("Author: Bill Sinko")
    print ("")
    
    args=cmdlineparse()
    if not args.nprocs:
        nprocs=10
    else:
        nprocs=int(args.nprocs)    
    ##MAIN ARGS
    start_time = time.time()
    #if len(sys.argv) == 4:
     #   print "ERROR: Run as python program.py pcafile.dat weights.csv <scaling factor> <discretization> "
     #   sys.exit()
    datafile = (sys.argv[1])
    outputfile= (sys.argv[2])
    factor = float(args.lambdavalue) #float(sys.argv[3])
    discretization= float(args.disc)#float(sys.argv[4])
    factor=1.00000000000/factor
    
    ##Import Data and setup data lengths
    datafull = np.loadtxt(args.input, skiprows=0)
    length=datafull[:,0]
    rows = len(length)
    loop = range(rows)
    width=datafull[0,:]

    ##Round to discretization size and convert to integer
    datafull=np.divide(datafull, discretization)
    datafull=np.around(datafull)
    datafull_int=datafull.astype(int)
    print ("data loaded! in:", time.time() - start_time, "seconds")
    start_time = time.time()
    ##Convert from list to string
    str_list=list()
    for x in loop:
        a=str(datafull_int[x,:])
        str_list.append(a)
    unique=list(set(str_list))
    print ("string conversion complete! in:", time.time() - start_time, "seconds")
    
   


###Unique counter string
    index=list()
    number_unique = len(unique)
    print ("unique strings:  ", number_unique, "of total strings:", len(str_list))
    
    def unique_counter(unique_chunk):
        
        weight=[0]*len(str_list)
        for query in unique_chunk:
            index[:]=[]
            count=0
            for x in loop:
                    if unique[query] ==  str_list[x]:
                            count=count+1
                            index.append(x)             
            count_weight=np.power(count, factor)
            count_weight=np.divide(count_weight, count)
            for x in index:
                    weight[x]=count_weight
            if query % 1000 == 0:
                print (query," of ", number_unique, ":     ",unique[query])
        return(weight)

######Multiprocessing function and chunker
    def mp(nprocs):
        def worker(unique_chunk, out_q):
        #""" The worker function invokes a process
            outweight=[0]*len(str_list)
            outweight=unique_counter(unique_chunk)
            out_q.put(outweight)
        
    # Each process will get 'chunksize' nums and a queue to put his out
        out_q = multiproc.Queue()
    
        
        chunksize = int(math.ceil(len(unique)) / float(nprocs))
        chunk_remainder=int(np.subtract(len(unique),(chunksize * nprocs)))  ## add remainder to last chunk
        print (chunk_remainder)
        procs = []
        print ("chunksize   ", chunksize)

        for i in range(nprocs):
            
            if i == (nprocs - 1):
                p = multiproc.Process(
                    target=worker,
                    args=(range(len(unique))[chunksize * i:(chunk_remainder + chunksize * (i + 1))],
                      out_q))
            else:
                p = multiproc.Process(
                    target=worker,
                    args=(range(len(unique))[chunksize * i:chunksize * (i + 1)],
                      out_q))
            print ("Launching process:  ", i, "with ~chunksize:  ", chunksize, "  nprocs:  ", nprocs)
            procs.append(p)
            p.start()

    # Collect all results into a single list
        weight_temp=[0]*len(str_list)
        weight=[0]*len(str_list)
        for i in range(nprocs):
            
            weight_temp=out_q.get()
            weight=np.add(weight, weight_temp)
    # Wait for all worker processes to finish
        for p in procs:
            p.join()

        return weight
   
    ###Call single processor mode
    
    def sp(unique): 
        outweight=[0]*len(str_list)
        
        outweight_temp=[0]*len(str_list)
        for query in range(len(unique)):
            outweight_temp = unique_counter(query)
            outweight=np.add(outweight, outweight_temp)
         
        return outweight
   
    #########################CALL Multiprocessor Function##################
    weight=mp(nprocs)
    #########################Call Single processor function for debugging purposes####
    #weight=sp(unique)
   
    
#####write file############
    
    with open(str(args.weight), 'w') as f:
        writer=csv.writer(f)
        for val in weight:
            writer.writerow([val])
        

    print ("execution time", time.time() - start_time, "seconds")

if __name__ == "__main__":
    main()
