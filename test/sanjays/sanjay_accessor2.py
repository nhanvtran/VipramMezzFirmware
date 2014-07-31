import os
import sys
import ctypes

import uhal
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

from optparse import OptionParser

import random
############################################
#            Job steering                  #
############################################
ROW_MAX = 128
COL_MAX = 32
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
    inputFile = file("10kPatterns_sec27_0DC_lowPT_0DC.txt", "r+")
    data = inputFile.readlines()
    rowNum = 0
    colNum = 0
    rowNums = []
    #rowCount = 0
    #colCount = 0
    for i in range(1, len(data)):
        strNums = data[i].split(" - ")
        inputPattern.loadSinglePattern(rowNum, colNum, [int(strNums[0]), int(strNums[1]), int(strNums[2]), int(strNums[3])], 1)
        #rowCount += 1
        #colCount += 1
        colNum += 1
        rowNums.append(rowNum)
        if (colNum == COL_MAX):
            rowNum += 1
            #rowCount = 0
            colNum = 0
        if (rowNum == ROW_MAX):
            print "Reached maximum number of rows. Done loading data."
            break
        
    inputPattern.initializeRunPhase( [1,0,0,0] );
    inputPattern.readOutMode();
    for j in range(0, 5):
        randInt = random.randint(0, len(data)-1)
        strsRand = data[randInt].split(" - ")
        inputPattern.checkPattern([int(strsRand[0]), int(strsRand[1]), int(strsRand[2]), int(strsRand[3])], rowNums[randInt])
    #inputPattern.doRowChecker(9);
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
    for a in range(blockSize-1,-1,-1):
        
        if iSteps%100 == 0: print "iSteps = ", a, iSteps
        
        ## cycle through all inputs
        for i in range(nInputs):
            ## cycle through 32 bit increments of a particular input
            curword = [];
            for j in range(iSteps,fSteps):
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
        curBlock = hw.getNode("VipMEM."+registers[i]).readBlock( blockSize );
        hw.dispatch();
#        if "Out" in registers[i]: outMem.append( flipList(curBlock) );
#        else: outMem.append( curBlock );
        outMem.append( curBlock );
        #print "input #",i," = ",registers[i]," and value = ", '{0:032b}'.format(curBlock[1023]), '{0:032b}'.format(curBlock[1022])

    fno = os.path.splitext( pattern1.getFilename() )[0]+"_f.txt";
    fout = open(fno,'w');
    timeCtr = 0;
    for a in range(blockSize-1,-1,-1):
        if a%100 == 0: print a
    #for a in range(blockSize):
        #if a < 1010: break;
        for i in range(stepIncrement):
            thisTimeSlice = [];
            for j in range(len(outMem)): # no checkData bit
                #print nInputs,",",j,",",a,",",len(outMem[j])
                blockPiece     = '{0:032b}'.format(outMem[j][a])
                blockPiece_opp = '{0:032b}'.format(outMem[j][1023-a])
                
                if j <= 31: thisTimeSlice.append( blockPiece_opp[stepIncrement-i-1] );
                else: thisTimeSlice.append( blockPiece[i] );
        
            #fout.write( ''.join(thisTimeSlice)+'\n' );
            if timeCtr < totalTimeSlices: fout.write( ''.join(thisTimeSlice)+'\n' );
            if timeCtr > totalTimeSlices: break;
            timeCtr+=1;
        if timeCtr > totalTimeSlices: break;




