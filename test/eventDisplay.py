import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import MultipleLocator
from matplotlib import colors

if __name__ == '__main__':

    f1 = open('root/tmp1_i.txt','r');
    f2 = open('root/tmp1_f.txt','r');

    lastline = "blah"
    ctr = 0;
    outputPattern = np.zeros((128,32))
    expected_outputPattern = np.zeros((128,32))
    
    while True:

        curline1 = f1.readline().rstrip('\n')
        curline2 = f2.readline().rstrip('\n')

        # eof
        if curline1 == "" and curline2 == "": break;

        checkData = curline1[0];
        comp1 = curline1[1:]
        comp2 = curline2

        if int(checkData) == 1:
            print "time slice: ", ctr, ", checkData = ", checkData;
            print comp1
            print comp2
#            row = int(comp2[-76:-69],2)
#            col = int(comp2[-69:-64],2)
	    row = int(comp2[40:47][::-1],2)
            col = int(comp2[47:52][::-1],2)
            outputData = list(comp2[:32])[::-1]
            outputPattern[row] = outputData
	    
	    rowE = int(comp1[40:47][::-1],2)
            colE = int(comp1[47:52][::-1],2)
	    expected_outputData = list(comp1[0:32])[::-1]
	    expected_outputPattern[rowE] = expected_outputData
            
            if comp1 == comp2: 
                print "match!"  
            else: 
                print "no match!"
                
        ctr += 1
    
    cmap = colors.ListedColormap(['white','blue', 'red'])
    cmap1 = colors.ListedColormap(['white','red', 'green'])


    bounds=[0,1,2,3]
    norm = colors.BoundaryNorm(bounds, cmap.N)
    plt.figure()
    plt.imshow(outputPattern,cmap=cmap, norm = norm, interpolation = 'Nearest',aspect='auto')
    #plt.text(col,row,"CAM")
    plt.grid("on")
    plt.title("protoVIPRAM 2D")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    
    plt.figure()
    plt.imshow(expected_outputPattern,cmap=cmap1, norm = norm, interpolation = 'Nearest',aspect='auto')
    #plt.text(col,row,"CAM")
    plt.grid("on")
    plt.title("protoVIPRAM 2D : Expected Output Patterns")
    plt.xlabel("Columns")
    plt.ylabel("Rows")
    
    plt.show()
        
        
