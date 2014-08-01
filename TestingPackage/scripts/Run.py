import os
import sys
import ctypes
import time

import uhal
import ROOT

from optparse import OptionParser
import os
import random

sys.path.insert(0, '../interface')
from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *
from VipramCom import *
from example1 import *

parser = OptionParser()

parser.add_option('-b', action='store_true', dest='noX', default=False, help='no X11 windows')
parser.add_option('--go', action='store_true', dest='go', default=False, help='go!')
parser.add_option('--reset', action='store_true', dest='reset', default=False, help='go!')

parser.add_option('--freq',action="store",type="int",dest="freq",default=10)
parser.add_option('--NStress',action="store",type="int",dest="NStress",default=0)


(options, args) = parser.parse_args()

############################################################

if __name__ == '__main__':

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # generate the patterns
    pattern1 = stressTest("tmp1",options.NStress,options.freq);
    #pattern1 = exampleTest("tmp1");

    print "file = ", pattern1.getFilename();
    visualizer1 = inputVisualizer( pattern1.getFilename() );
    bits = visualizer1.writeToText( os.path.splitext( pattern1.getFilename() )[0]+"_i.txt", True );
    
    # print "N time slices = ", len(bits);
    # for i in range(len(bits)):
    #     print bits[i]," and ", len(bits[i])
    #testFile = open("dat/tmp1_i.txt", True);
    
    print "total time slices = ", len(bits)
    print "total time slices = ", len(bits[0])

    vc1 = VipramCom(bits,"tmp1");
    vc1.sendInstructions();
    vc1.retrieveRegisters();
    vc1.compareOutput();

    # ctr = 0;
    # curbits = [];
    # index = 0
    # for i in range(0, len(bits)):
    #     if (i == len(bits)-1) or (i % 32768 == 0 and i > 0): 
    #         sendRetrieveCompare(curbits, index);
    #         curbits = [];
	   #  index = i
    #     curbits.append( bits[i] )

    


