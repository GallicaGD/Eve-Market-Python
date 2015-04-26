#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Gallica
#
# Created:     13/04/2015
# Copyright:   (c) Gallica 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

##from eveData import *
import math
import itertools

def main():
##    eve = eveData()

    nlist = list(range(8))

    size = 10
    iter = math.ceil(len(nlist) / size)
    start = 0
    stop = start + size
    print('It: {0}'.format(iter))

    for s in range(iter):
        print('Iter: {0}, Start: {1} Stop: {2}'.format(s, start, stop))
        x = []
        for n in itertools.islice(nlist, start, stop):
            x.append(n)
            print('iSpot: {0}'.format(n))
##        for i in range(start, stop):
##            print('Spot: {0}'.format(nlist[i]))

        print(x)
        start += size
        stop = start + size


    print('DONE!')

if __name__ == '__main__':
    main()
