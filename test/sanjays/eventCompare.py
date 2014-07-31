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
    
#---------------------------------------------------------------------
 
if __name__ == '__main__':

    f1 = open('root/tmp1_i.txt','r');
    f2 = open('root/tmp1_f.txt','r');

    #find offset
    file1 = f1.read();
    file2 = f2.read();    

    list1 = file1.split()
    list2 = file2.split()

    runModeLine1 = -1;
    runModeLine2 = -1;
    for i in range(len(list1)-1):
        
        compL = "".join(['1']*32);
        compR = "".join(['0']*32);

        curout  = list1[i][1:33]
        nextout = list1[i+1][1:33]
        
        if curout == compL and nextout == compR: 
            runModeLine1 = i;
            break;

    for i in range(len(list2)-1):
        
        compL = "".join(['1']*32);
        compR = "".join(['0']*32);

        curout  = list2[i][:32]
        nextout = list2[i+1][:32]
        
        if curout == compL and nextout == compR: 
            runModeLine2 = i;
            break;

    shift = runModeLine2 - runModeLine1;
    
    print "------------------------"
    print "Welcome to comparator..."
    print "calculated Output shift is ",shift
    mismatchCtr = 0;
    matchCtr =0;
    
    shift = 0
    print "Using output shift:", shift
    
    
    
    outputPattern = np.zeros((128,32))
    outputPattern_cumulative = np.zeros((128,32))
    expected_outputPattern = np.zeros((128,32))
    expected_outputPattern_cumulative = np.zeros((128,32))

    for i in range(runModeLine1,len(list1)):
        
        curline1 = list1[i];    
        curline2 = list2[i+shift];
	curline3 = list2[i]
	
        checkData = curline1[0];
        comp1 = curline1[1:33]
        comp2 = curline2[:32]

        if int(checkData) == 1:
	
	    rowE = int(curline1[41:48][::-1],2)
            colE = int(curline1[48:53][::-1],2)
	    expected_outputData = list(comp1)[::-1]
	    expected_outputData = [int(x) for x in expected_outputData]
	    expected_outputPattern[rowE] = expected_outputData	   
	    expected_outputPattern_cumulative[rowE] = np.add(expected_outputPattern_cumulative[rowE],expected_outputData)

	    row = int(curline3[40:47][::-1],2)
            col = int(curline3[47:52][::-1],2)
            outputData = list(comp2)[::-1]
	    
#            outputPattern[row] = outputData
	    outputPattern[rowE] = outputData
	    outputData = [int(x) for x in outputData]
	    outputPattern_cumulative[rowE] = np.add(outputPattern_cumulative[rowE], outputData)
	    
	    Matched_Columns = [ p for p,q in enumerate(expected_outputData) if q == 1]
	    
            if comp1 != comp2: 
                print "--no match for time slice: ", i+1, ", checkData = ", checkData, "row =",rowE, "Column/s Supposed to Match", Matched_Columns
                mismatchCtr += 1;
	    else:
	    	matchCtr += 1;
    
    if mismatchCtr == 0:
        print "No Mismatches!!!,", matchCtr, "matches"
    else:		
        print "There are", mismatchCtr,"mismatches!";
        print "There are", matchCtr,"matches!";
    
    print "------------------------";
    
    cmap = colors.ListedColormap(['white','blue', 'red'])
    cmap1 = colors.ListedColormap(['white','red', 'green'])
    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    if np.array_equal(outputPattern_cumulative, expected_outputPattern_cumulative):
    	print "Everything Works!!", "Total number of hits =", int(np.sum(outputPattern_cumulative))
    	plt.figure()
    	plt.imshow(outputPattern_cumulative,cmap=cmap1, norm = norm, interpolation = 'Nearest',aspect='auto')
    	plt.grid("on")
	plt.xticks([i for i in range(0,32)])
	yr= [4*i for i in range(-1,32)]
	yr.append(127)
	plt.yticks(yr)
    	plt.title("protoVIPRAM 2D \n Test: Real Hits = Expected Hits, number of hits :" + str(int(np.sum(outputPattern))))
    	plt.xlabel("Columns")
   	plt.ylabel("Rows")
    
    
    else:
    	print "Expected number of hits :", int(np.sum(expected_outputPattern_cumulative))
        print "Actual number of hits :", int(np.sum(outputPattern_cumulative))	
    	plt.figure()
    	plt.imshow(outputPattern_cumulative,cmap=cmap1, norm = norm, interpolation = 'Nearest',aspect='auto')
    	#plt.text(col,row,"CAM")
    	plt.grid("on")
	plt.xticks([i for i in range(32)])
	yr= [4*i for i in range(32)]
	yr.append(127)
	plt.yticks(yr)
    	plt.title("protoVIPRAM 2D")
    	plt.xlabel("Columns")
    	plt.ylabel("Rows")
    
    	plt.figure()
    	plt.imshow(expected_outputPattern_cumulative,cmap=cmap, norm = norm, interpolation = 'Nearest',aspect='auto')
    	#plt.text(col,row,"CAM")
    	plt.grid("on")
	plt.xticks([i for i in range(32)])
	yr= [4*i for i in range(32)]
	yr.append(127)
	plt.yticks(yr)
    	plt.title("protoVIPRAM 2D : Expected Output Patterns")
    	plt.xlabel("Columns")
    	plt.ylabel("Rows")    

    print "------------------------","\n";
    
    print "Close plot to continue"

    plt.show()
        
             
        

    


