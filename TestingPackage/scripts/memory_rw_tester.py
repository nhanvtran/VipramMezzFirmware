import os
import random
import sys
import ctypes
import time

import uhal
import ROOT


#from pVIPRAM_inputBuilderClass import *
#from pVIPRAM_inputVisualizerClass import *
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

    manager = uhal.ConnectionManager("file://../data/vipram_connections.xml")
    hw = manager.getDevice("Mezz1")
    uhal.setLogLevelTo( uhal.LogLevel.NOTICE )

    reg0 = hw.getNode("VipMEM.V_DVDD").read()
    reg1 = hw.getNode("VipMEM.V_VDD").read()
    reg2 = hw.getNode("VipMEM.V_VPRECH").read()

    ireg0 = hw.getNode("VipMEM.I_DVDD").read()
    ireg1 = hw.getNode("VipMEM.I_VDD").read()
    ireg2 = hw.getNode("VipMEM.I_VPRECH").read()

    vccreg = hw.getNode("VipMEM.V_VCC3V3").read()
    tmpreg = hw.getNode("VipMEM.Temperature").read()
    ltcreg = hw.getNode("VipMEM.LTC2991").read()

    hw.dispatch();

    print '{0:032b}'.format(reg0)
    print "V_DVDD = ",round(reg0*305.18/1.e6,3),"V"
    print "V_VDD = ",round(reg1*305.18/1.e6,3),"V"
    print "V_VPRECH = ",round(reg2*305.18/1.e6,3),"V"

    #print '{0:032b}'.format(ireg0)
    #print '{0:032b}'.format(ireg1)
    #print '{0:032b}'.format(ireg2)

    print "I_DVDD = ",round(ireg0*95.375,3),"uA"
    print "I_VDD = ",round(ireg1*95.375,3),"uA"
    print "I_VPRECH = ",round(ireg2*95.375,3),"uA"

    print "VCC3V3 = ", round(2.5+vccreg*305./1.e6,3),"V"
    print "Temperature = ", round(float(str(tmpreg))*0.0625,3),"C"
    print "LTC2991 = ", ltcreg

   # get the output registers
    
    # curBlock = [];
    # curBlockC = [];
    # nbuckets=1024
    # #npins=32
    # npins=4

    # hw.getNode("VipMEM.Go").write(0);    
    # hw.dispatch()
    
    # # writing
    # for i in range(1,npins):
    #     xx = [];
    #     for j in range (nbuckets):
    #         #xx.append(randuint32())
    #         xx.append(ctypes.c_uint32(300).value)
    
    #     hw.getNode("VipMEM.Out"+ str(i)).writeBlock( xx )
    #     hw.getNode("VipMEM.C"+ str(i)).writeBlock( xx )
    #     hw.dispatch()
    #     #hw.getNode("VipMEM.Out"+ str(i)).writeBlock( xx )
    #     #hw.getNode("VipMEM.C"+ str(i)).writeBlock( xx )
    #     #hw.dispatch()

    # #time.sleep(5.);
    
    # # reading
    # for i in range(1,npins):

    #     curBlock = hw.getNode("VipMEM.Out"+ str(i)).readBlock( nbuckets )
    #     curBlockC = hw.getNode("VipMEM.C"+ str(i)).readBlock( nbuckets )
    #     hw.dispatch()
    #     #curBlock = hw.getNode("VipMEM.Out"+ str(i)).readBlock( nbuckets )
    #     #curBlockC = hw.getNode("VipMEM.C"+ str(i)).readBlock( nbuckets )
    #     #hw.dispatch()

    #     for j in range (nbuckets):
    #         print i,",",j,",", bin(xx[j])[2:].zfill(32), " ", bin(curBlock[j])[2:].zfill(32), " ", bin(curBlockC[j])[2:].zfill(32)
            



