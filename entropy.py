#! /usr/bin/env python
import argparse
import os,sys
import shutil
import mmap
import timeit
import statistics

def create_parse():
    parser = argparse.ArgumentParser(
        description='file entropy estimator')
    parser.add_argument('filename', help='file to scan')
    return parser

def start():
    begin=timeit.default_timer()
    parser = create_parse()
    args = parser.parse_args()
    filename=args.filename
    f=os.open(filename,os.O_RDONLY)
    mm=mmap.mmap(f,0,access=mmap.ACCESS_READ)
    count=[]
    for i in range(256):
        count.append(0)
    size = 0
    for i in range(len(mm)):
        count[mm[i]] += 1
        size +=1
    mm.close
    os.close(f)
    
    end=timeit.default_timer()
    elapsed=end-begin

    print("Read {:,} bytes in {:.3f} seconds ({:,}/second)".format(size,elapsed,int(size/elapsed)))

    mean = statistics.fmean(count)
    variance = statistics.variance(count,mean)
    stdev = statistics.stdev(count,mean)

#    for i in range(256):
#        if count[i] > 0:
#            print("[{}]: {:,}".format(i,count[i]))

    print("Mean: {:.2f}".format(mean))
    print("Variance: {:.2f}".format(variance))
    print("Std dev: {:.2f}".format(stdev))
    mmax=max(count)
    maxindex=count.index(mmax)
    print("Max: {} [{}]".format(maxindex,count[maxindex]))
    mmin=min(count)
    minindex=count.index(mmin)
    print("Min: {} [{}]".format(minindex,count[minindex]))

if __name__ == '__main__':
    start()
