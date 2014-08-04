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

# tests to run
parser.add_option('--runStressTest', action='store_true', dest='runStressTest', default=False, help='go!')
parser.add_option('--runExampleTest', action='store_true', dest='runExampleTest', default=False, help='go!')

(options, args) = parser.parse_args()

############################################################

if __name__ == '__main__':

    # ------------------------------------------------
    # ------------------------------------------------
    # ------------------------------------------------
    # generate the patterns
    pattern1 = stressTest("tmp1",options.NStress,options.freq);
    #pattern1 = exampleTest("tmp1");

    visualizer1 = inputVisualizer( pattern1.getFilename() );
    bits = visualizer1.writeToText( os.path.splitext( pattern1.getFilename() )[0]+"_i.txt", True );

    vc1 = VipramCom("tmp1");
    vc1.runTest(bits);

    


