import os
import sys
import ctypes

import uhal
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

from optparse import OptionParser
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
    inputPattern.initializeLoadPhase();
    inputPattern.loadUniformPatterns(10, 5, 27, 1);
    inputPattern.loadUniformPatterns(10, 6, 47, 1);
    inputPattern.loadUniformPatterns(10, 7, 67, 1);
    inputPattern.initializeRunPhase( [1,0,0,0] );
    for i in range(20): inputPattern.checkPattern( [27,27,27,27] ,10);
    for i in range(20): inputPattern.checkPattern( [47,47,47,47] ,10);
    for i in range(20): inputPattern.checkPattern( [67,67,67,67] ,10);
    for i in range(20): inputPattern.checkPattern( [2,2,2,2] ,10);
    inputPattern.readOutMode();
    inputPattern.doRowChecker(10);

    #inputPattern.initializeLoadPhase();
    #rowrange = [2,3]
    #colrange = [20,30]
    
    #for row in range(rowrange[0], rowrange[1]):
    #    for col in range(colrange[0], colrange[1]):
    #        inputPattern.loadUniformPatterns(row, col, row +1000*col, 1)

    #inputPattern.initializeRunPhase( [1,0,0,0] );
    #for i in range(10): inputPattern.checkPattern( [32767,32767,32767,32767] ,row);

    #for row in range(rowrange[0], rowrange[1]):
    #        for col in range(colrange[0], colrange[1]):
    #            inputPattern.checkPattern( [row+1000*col, row+1000*col, row+1000*col,row+1000*col] ,row)
    #            for i in range(10): inputPattern.checkPattern( [32767,32767,32767,32767] ,row);
                
    #for row in range(rowrange[0], rowrange[1]):
    #        for col in range(colrange[0], colrange[1]):            
    #            inputPattern.doRowChecker(row)

                
    inputPattern.close();
    return inputPattern;


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


    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # get the output registers
    outMem = [];
    
    for i in range(nInputs):
        ## put the 32 bit word into memory
        if 'CheckData' in registers[i]: continue;
        for jj in range(100): curBlock = hw.getNode("VipMEM."+registers[i]).readBlock( blockSize );
        hw.dispatch();
#        if "Out" in registers[i]: outMem.append( flipList(curBlock) );
#        else: outMem.append( curBlock );
        if "Out" in registers[i]: print registers[i], '{0:032b}'.format(curBlock[0])
        outMem.append( curBlock );
        #print "input #",i," = ",registers[i]," and value = ", '{0:032b}'.format(curBlock[1023]), '{0:032b}'.format(curBlock[1022])

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
#        if timeCtr > totalTimeSlices: break;


