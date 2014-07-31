import os
import sys
import ctypes
import time

from optparse import OptionParser

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.ticker import MultipleLocator
from matplotlib import colors
    
import os

def getMatrix(filename):
    os.system("cat " + filename + " | grep checkData > " + "checkData.txt")
    matrix = np.zeros((128,32))
    checkDataFile = open("checkData.txt", "r+")
    content = checkDataFile.readlines()
    for i in content:
	split1 = i.split(" ")            
	split2 = i.split("[")
	split3 = split2[1].split("]")
	row = int(split1[14])
	col = int(split3[0])
	matrix[row][col] = 1
    return matrix

if __name__ == '__main__':
    
    outputPattern = getMatrix(sys.argv[1])
    
    cmap = colors.ListedColormap(['white','blue', 'red'])
    cmap1 = colors.ListedColormap(['white','red', 'green'])
    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    print "Total number of mismatches =", int(np.sum(outputPattern))
    plt.figure()
    plt.imshow(outputPattern,cmap=cmap1, norm = norm, interpolation = 'Nearest',aspect='auto')
    plt.grid("on")
    plt.xticks([i for i in range(0,32)])
    yr= [4*i for i in range(-1,32)]
    yr.append(127)
    plt.yticks(yr)
    plt.title(sys.argv[1][:-4]+"\nMismatches")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    plt.savefig(sys.argv[1][:-4]+".png")
    print "------------------------","\n";

#    plt.show()
        
             
        

    


