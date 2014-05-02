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
    inputPattern.loadUniformPatterns(9, 9, 27, 1); 
    inputPattern.loadUniformPatterns(9, 11, 37, 1); 
    inputPattern.loadUniformPatterns(9, 13, 47, 1);
    inputPattern.loadUniformPatterns(9, 15, 57, 1);
    inputPattern.loadUniformPatterns(9, 17, 67, 1);
    inputPattern.close();
    return inputPattern;


############################################################

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
    bits = visualizer1.writeToText( os.path.splitext( pattern1.getFilename() )[0]+".txt" );
    
    print "N time slices = ", len(bits);
    for i in range(len(bits)):
        print bits[i]

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
    fSteps = 31;
    stepIncrement = 32;
    nInputs = 85;
    blockSize = 1024;

    ###################
    ## define registers
    registers = [];
    registers.append( 'leaveEMPTY' ); # CheckData
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
    print "total time slices = ", totalTimeSlices
    dicedBits = [None]*nInputs;
    for i in range(len(dicedBits)): dicedBits[i] = [None]*blockSize ;

    #while len(bits) > iSteps+1:
    for a in range(blockSize):
        
        print "iSteps = ", a, iSteps
        
        ## cycle through all inputs
        for i in range(nInputs):
            ## cycle through 32 bit increments of a particular input
            curword = [];
            for j in range(iSteps,fSteps+1):
                if j+1 < len(bits) and not options.reset: curword.append( str(bits[j][i]) );
                else: curword.append("0");
            #print len(curword);
            
            stringword = ''.join(curword);
            dicedBits[i][a] = ctypes.c_uint32(int(stringword,2)).value;
            if a < 5: print registers[i], stringword

        ## go on to the next 32 bits!
        iSteps += stepIncrement;
        fSteps += stepIncrement;

    for i in range(nInputs):
        ## put the 32 bit word into memory
        if registers[i] == 'leaveEMPTY': continue;
        hw.getNode("VipMEM."+registers[i]).writeBlock( dicedBits[i] );
        hw.dispatch();

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # go!
    if options.go:
        hw.getNode("VipMEM.Go").write(1);
        hw.dispatch();







