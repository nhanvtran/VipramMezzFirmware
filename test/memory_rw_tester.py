import os
import random
import sys
import ctypes
import time

import uhal
import ROOT


from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *
from random import randint

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
def randuint32():
    return randint(0, 0xffffffff)

if __name__ == '__main__':

    manager = uhal.ConnectionManager("file://vipram_connections_sj.xml")
    hw = manager.getDevice("Mezz1")
    uhal.setLogLevelTo( uhal.LogLevel.NOTICE )
   # get the output registers
    
    curBlock = [];
    curBlockC = [];
    nbuckets=1024
    #npins=32
    npins=4

    hw.getNode("VipMEM.Go").write(0);    
    hw.dispatch()
    
    # writing
    for i in range(1,npins):
        xx = [];
        for j in range (nbuckets):
            #xx.append(randuint32())
            xx.append(ctypes.c_uint32(300).value)
    
        hw.getNode("VipMEM.Out"+ str(i)).writeBlock( xx )
        hw.getNode("VipMEM.C"+ str(i)).writeBlock( xx )
        hw.dispatch()
        #hw.getNode("VipMEM.Out"+ str(i)).writeBlock( xx )
        #hw.getNode("VipMEM.C"+ str(i)).writeBlock( xx )
        #hw.dispatch()

    #time.sleep(5.);
    
    # reading
    for i in range(1,npins):

        curBlock = hw.getNode("VipMEM.Out"+ str(i)).readBlock( nbuckets )
        curBlockC = hw.getNode("VipMEM.C"+ str(i)).readBlock( nbuckets )
        hw.dispatch()
        #curBlock = hw.getNode("VipMEM.Out"+ str(i)).readBlock( nbuckets )
        #curBlockC = hw.getNode("VipMEM.C"+ str(i)).readBlock( nbuckets )
        #hw.dispatch()

        for j in range (nbuckets):
            print i,",",j,",", bin(xx[j])[2:].zfill(32), " ", bin(curBlock[j])[2:].zfill(32), " ", bin(curBlockC[j])[2:].zfill(32)
            



