import os
import sys

import uhal
import ROOT

from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

############################################################

def GenerateInputs(testname):

    inputPattern = inputBuilder("root/"+testname+".root");
    inputPattern.initializeLoadPhase();
    inputPattern.loadUniformPatterns(9, 9, 27, 1); 
    inputPattern.loadUniformPatterns(9, 11, 37, 1); 
    inputPattern.loadUniformPatterns(9, 13, 47, 1); 
    inputPattern.close();
    return inputPattern;

if __name__ == '__main__':

    # ------------------------------------------------
    # generate the patterns
    pattern1 = GenerateInputs("tmp1");
    print "file = ", pattern1.getFilename();

    visualizer1 = inputVisualizer( pattern1.getFilename() );
    #visualizer1.textVisualizer();
    
    # this gives you a list of each time slices
    bits = visualizer1.writeToText( os.path.splitext( pattern1.getFilename() )[0]+".txt" );
    
    #print "N time slices = ", len(bits);
    #for i in range(len(bits)):
    #    print len(bits[i]);

    # ------------------------------------------------
    # dump it into the memory
    manager = uhal.ConnectionManager("file://vipram_connections.xml")
    hw = manager.getDevice("Mezz1")

    #print "identity: ",hw.getNode("VipMEM.Ident").read()
    ident = hw.getNode("VipMEM.Ident").read();
    hw.dispatch();
    print "ident = ", hex(ident);
    


