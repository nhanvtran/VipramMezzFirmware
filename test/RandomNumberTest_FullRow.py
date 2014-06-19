import os
import sys
import ctypes
import time

import uhal
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

from optparse import OptionParser

import os
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
#from matplotlib.ticker import MultipleLocator
from matplotlib import colors
import random

############################################
#            Job steering                  #
############################################
parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--go', action='store_true', dest='go', default=False, help='go!')
parser.add_option('--reset', action='store_true', dest='reset', default=False, help='go!')

(options, args) = parser.parse_args()
############################################

############################################################

def GenerateInputs(testname):

    inputPattern = inputBuilder("root/"+testname+".root");
    
    row = int(sys.argv[1])
    		
    for col in range(32):
    
    	inputPattern.initializeLoadPhase()
		
    	data1 = random.randint(0,32767)
    	data2 = random.randint(0,32767)
    	data3 = random.randint(0,32767)
    	data4 = random.randint(0,32767)
	
    	print "\nTesting Row:"+str(row)+" Column: "+str(col)+"\n"    
    	inputPattern.loadSinglePattern(row, col,[data1,data2,data3,data4], 10)
	    
    	print "-Loaded Data:", data1, "in Row:", row," Col:", col, "layerA"
    	print "-Loaded Data:", data2, "in Row:", row," Col:", col, "layerB"
    	print "-Loaded Data:", data3, "in Row:", row," Col:", col, "layerC"
    	print "-Loaded Data:", data4, "in Row:", row," Col:", col, "layerD"

    	inputPattern.initializeRunPhase( [1,0,0,0] )
    	inputPattern.checkPattern( [21845, 21845, 21845, 21845] ,row)
    	inputPattern.checkPattern( [data1,data2,data3,data4] ,row)
    
    	for i in range(10):
    	    inputPattern.checkPattern( [21845, 21845, 21845, 21845] ,row)
    	inputPattern.doRowChecker(row)
    	for i in range(10):
	    inputPattern.checkPattern( [21845, 21845, 21845, 21845] ,row)

#    inputPattern.initializeLoadPhase()
#    inputPattern.loadUniformPatterns(row,col,0,1)
#    inputPattern.initializeRunPhase( [1,0,0,0] )
    
    inputPattern.close()
    return inputPattern



############################################################

def flipList( list ):
    newlist = [];
    for i in range(len(list)-1,-1,-1):
        newlist.append(list[i]);

if __name__ == '__main__':

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # generate the patterns
    pattern1 = GenerateInputs("tmp1");
    print "file = ", pattern1.getFilename();

    visualizer1 = inputVisualizer( pattern1.getFilename() );
    #visualizer1.textVisualizer();
    
    # this gives you a list of each time slices
    bits = visualizer1.writeToText( os.path.splitext( pattern1.getFilename() )[0]+"_i.txt", True );
    
    print "N time slices = ", len(bits);
    for i in range(len(bits)):
        print bits[i]," and ", len(bits[i])

    #exit()

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # dump it into the memory
    manager = uhal.ConnectionManager("file://vipram_connections.xml")
    hw = manager.getDevice("Mezz1")
    uhal.setLogLevelTo( uhal.LogLevel.NOTICE )

    #print "identity: ",hw.getNode("VipMEM.Ident").read()
    ident = hw.getNode("VipMEM.Ident").read();
    vers  = hw.getNode("VipMEM.FWver").read();
    hw.dispatch();
    print "Firmware identity = ", hex(ident), ", firmware version = ", vers;
    
    iSteps = 0;
    fSteps = 32;
    stepIncrement = 32;
    blockSize = 1024;

    ###################
    ## define registers
    registers = [];
    registers.append( 'CheckData' ); # CheckData
    for i in range(32-1,-1,-1): registers.append( 'Out'+str(i) );
    registers.append( 'ReqL0' );
    registers.append( 'Miss2' );
    registers.append( 'Miss1' );
    registers.append( 'Miss0' );
    registers.append( 'RunMode' );
    registers.append( 'Primary' );
    registers.append( 'Latch' );
    registers.append( 'EvRearm' );
    for i in range(7): registers.append( "RA"+str(i) );
    for i in range(5): registers.append( "CA"+str(i) );

    for i in range(1,16): registers.append( "A"+str(i) );
    registers.append( "A0" );
    for i in range(1,16): registers.append( "B"+str(i) );
    registers.append( "B0" );
    for i in range(1,16): registers.append( "C"+str(i) );
    registers.append( "C0" );
    for i in range(1,16): registers.append( "D"+str(i) );
    registers.append( "D0" );
    print "registers size = ", len(registers);
    ###################

    totalTimeSlices = len(bits);
    nInputs = len(registers);

    print "total time slices = ", totalTimeSlices
    print "the nInputs = ", nInputs
    dicedBits = [None]*nInputs;
    dicedBitsBinary = [None]*nInputs;
    for i in range(len(dicedBits)): dicedBits[i] = [None]*blockSize ;
    for i in range(len(dicedBitsBinary)): dicedBitsBinary[i] = [None]*blockSize ;

    #while len(bits) > iSteps+1:
    for a in range(blockSize):
        
        if iSteps%100 == 0: print "iSteps = ", a, iSteps
        
        ## cycle through all inputs
        for i in range(nInputs):
            ## cycle through 32 bit increments of a particular input
            curword = [];
            for j in range(fSteps,iSteps,-1):
                if j+1 < totalTimeSlices and not options.reset: curword.append( str(bits[j][i]) );
                elif j+1 >= totalTimeSlices and not options.reset:
                    ## set extra time slices to all zeroes
                    # curword.append("0");
                    ## set it to the last step
                    curword.append( str( bits[totalTimeSlices-1][i]))
                elif options.reset:
                    curword.append("0");
                else:
                    raise Exception("Something weird is going on..." );
                    
            stringword = ''.join(curword);
            dicedBits[i][a] = ctypes.c_uint32(int(stringword,2)).value;
            dicedBitsBinary[i][a] = stringword;

        ## go on to the next 32 bits!
        iSteps += stepIncrement;
        fSteps += stepIncrement;

    for i in range(nInputs):
        ## put the 32 bit word into memory
        if 'Out' in registers[i] or 'CheckData' in registers[i]: continue;
        hw.getNode("VipMEM."+registers[i]).writeBlock( dicedBits[i] );
        hw.dispatch();
        #print "input #",i," = ",registers[i]," and value = ", dicedBitsBinary[i][1023], dicedBitsBinary[i][1022]
        

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # go!
    if options.go:
        hw.getNode("VipMEM.Go").write(1);
        hw.dispatch();

    time.sleep(0.1);    
    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # get the output registers
    outMem = [];
    
    for i in range(nInputs):
        ## put the 32 bit word into memory
        if 'CheckData' in registers[i]: continue;
        curBlock = hw.getNode("VipMEM."+registers[i]).readBlock( blockSize );
        hw.dispatch();
#        if "Out" in registers[i]: outMem.append( flipList(curBlock) );
#        else: outMem.append( curBlock );
        outMem.append( curBlock );
        if "Out31" in registers[i]: 
            for k in range(1024): 
                print "Out31:", '{0:032b}'.format(curBlock[k]);
                print  '{0:032b}'.format(outMem[len(outMem)-1][k])
#        print "input #",i," = ",registers[i]," and value = ", '{0:032b}'.format(curBlock[1023]), '{0:032b}'.format(curBlock[1022])

    fno = os.path.splitext( pattern1.getFilename() )[0]+"_f.txt";
    fout = open(fno,'w');
    timeCtr = 0;
    for a in range(blockSize):
        if a%100 == 0: print a
    #for a in range(blockSize):
        #if a < 1010: break;
        for i in range(stepIncrement):
            thisTimeSlice = [];
            for j in range(len(outMem)): # no checkData bit
                #print nInputs,",",j,",",a,",",len(outMem[j])
                blockPiece     = '{0:032b}'.format(outMem[j][a])
                thisTimeSlice.append( blockPiece[stepIncrement-i-1] );                
               
            fout.write( ''.join(thisTimeSlice)+'\n' );
            #if timeCtr < totalTimeSlices: 
            #fout.write( ''.join(thisTimeSlice)+'\n' );
            #if timeCtr > totalTimeSlices: break;
            timeCtr+=1;
        if timeCtr > totalTimeSlices+500: break;
    
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


    if np.array_equal(outputPattern_cumulative, expected_outputPattern_cumulative):
    	print "Everything Works!!", "Total number of hits =", int(np.sum(outputPattern_cumulative))
	bounds=[0,1,2,3]
        norm = colors.BoundaryNorm(bounds, cmap.N)

#    	plt.figure()
#    	plt.imshow(outputPattern,cmap=cmap1, norm = norm, interpolation = 'Nearest',aspect='auto')
#    	plt.grid("on")
#	plt.xticks([i for i in range(0,32)])
#	yr= [4*i for i in range(-1,32)]
#	yr.append(127)
#	plt.yticks(yr)
#    	plt.title("protoVIPRAM 2D \n Test: Real Hits = Expected Hits, number of hits :" + str(int(np.sum(outputPattern))))
#    	plt.xlabel("Columns")
#   	plt.ylabel("Rows")
    
    
    else:
    	print "Expected number of hits :", int(np.sum(expected_outputPattern_cumulative))
        print "Actual number of hits :", int(np.sum(outputPattern_cumulative))
	
#    	bounds=[0,1,2,3]
#    	norm = colors.BoundaryNorm(bounds, cmap.N)
#    	plt.figure()
#    	plt.imshow(outputPattern,cmap='Reds', norm = norm, interpolation = 'Nearest',aspect='auto')
#    	#plt.text(col,row,"CAM")
#    	plt.grid("on")
#	plt.xticks([i for i in range(32)])
#	yr= [4*i for i in range(32)]
#	yr.append(127)
#	plt.yticks(yr)
#    	plt.title("protoVIPRAM 2D")
#    	plt.xlabel("Columns")
#    	plt.ylabel("Rows")
    
#    	plt.figure()
#    	plt.imshow(expected_outputPattern,cmap='Blues', norm = norm, interpolation = 'Nearest',aspect='auto')
#    	#plt.text(col,row,"CAM")
#    	plt.grid("on")
#	plt.xticks([i for i in range(32)])
#	yr= [4*i for i in range(32)]
#	yr.append(127)
#	plt.yticks(yr)
#    	plt.title("protoVIPRAM 2D : Expected Output Patterns")
#    	plt.xlabel("Columns")
#    	plt.ylabel("Rows")    

    print "------------------------","\n";
    
#    print "Close plot to continue"

#    plt.show()
        
             
        

    


