import ROOT
import sys
import uhal
import ctypes
import time
import os

import datetime

sys.path.insert(0, '../interface')
from pVIPRAM_inputBuilderClass import *
from pVIPRAM_inputVisualizerClass import *

class VipramCom:

    def __init__(self,name,go=True,freq=100,odir="blah"):
        
        self._name = name;
        self._go = go;
        self._freq = freq;
        self._odir = odir;

        self._manager = uhal.ConnectionManager("file://../data/vipram_connections.xml");
        self._hw = self._manager.getDevice("Mezz1")
        uhal.setLogLevelTo( uhal.LogLevel.ERROR )
        self._ident = self._hw.getNode("VipMEM.Ident").read();
        self._vers  = self._hw.getNode("VipMEM.FWver").read();
        self._hw.dispatch();
        print "Firmware identity = ", hex(self._ident), ", firmware version = ", self._vers;

        self._iSteps = 0;
        self._fSteps = 32;
        self._stepIncrement = 32;
        self._blockSize = 1024;

        ###################
        ## define registers
        self._registers = [];
        self._registers.append( 'CheckData' ); # CheckData
        for i in range(32-1,-1,-1): self._registers.append( 'Out'+str(i) );
        self._registers.append( 'ReqL0' );
        self._registers.append( 'Miss2' );
        self._registers.append( 'Miss1' );
        self._registers.append( 'Miss0' );
        self._registers.append( 'RunMode' );
        self._registers.append( 'Primary' );
        self._registers.append( 'Latch' );
        self._registers.append( 'EvRearm' );
        for i in range(7): self._registers.append( "RA"+str(i) );
        for i in range(5): self._registers.append( "CA"+str(i) );

        for i in range(1,16): self._registers.append( "A"+str(i) );
        self._registers.append( "A0" );
        for i in range(1,16): self._registers.append( "B"+str(i) );
        self._registers.append( "B0" );
        for i in range(1,16): self._registers.append( "C"+str(i) );
        self._registers.append( "C0" );
        for i in range(1,16): self._registers.append( "D"+str(i) );
        self._registers.append( "D0" );

        print "registers size = ", len(self._registers);
        ###################

        # power numbers
        self._i_dvdd = [];
        self._i_vdd = [];
        self._i_prech = [];
        self._difftimes = [];

    def runTest(self, bits, reset=False):

        self._instructions = bits;
        self._matchCtr = 0;
        self._checkDataDtr = 0;
        self.denom = 0;
        self.numer = 0;

        self._currentMemoryBlock = 0;
        curbits = [];

        # input text file
        f1 = open(self._odir+'/'+self._name+'_i.txt','r');
        list1 = f1.read().split()

        print "list1 lenghth = ", len(list1), " and bits length = ", len(bits)

        memoryBlocksNeeded = len(bits)/(1024*32) + 1;
        print "memoryBlocksNeeded = ",memoryBlocksNeeded
        outputfiles = [];
        for i in range(memoryBlocksNeeded):
            fno = self._odir+'/'+self._name+"_tmpi_"+str(i)+".txt";
            if os.path.exists(fno):
                os.remove(fno)
            outputfiles.append( open(fno,'w') ); 

        for i in range(len(bits)):
            curbits.append(bits[i]);
            #print i
            outputfiles[self._currentMemoryBlock].write( list1[i]+'\n' );

            if (((i+1) % (1024*32) == 0) and (i > 0)) or (i == len(bits)-1):
                print "[VipramCom: runTest] On memory block ",str(self._currentMemoryBlock);
                self.sendInstructions(curbits,reset);
                self.retrieveRegisters(curbits);

                outputfiles[self._currentMemoryBlock].close();

                self.compareOutput(); ## how to do the comparison, make internal txt files?
                    
                curbits[:] = []; #clear the list
                self._currentMemoryBlock += 1;

                if reset: break;

    def runPowerTest(self, bits, cycles, isPower = False, nPowerCycles = 1, reset=False):

        self._instructions = bits;
        self._matchCtr = 0;
        self._checkDataDtr = 0;

        self._currentMemoryBlock = 0;
        curbits = [];

        # input text file
        f1 = open(self._odir+'/'+self._name+'_i.txt','r');
        list1 = f1.read().split()

        print "list1 lenghth = ", len(list1), " and bits length = ", len(bits)

        memoryBlocksNeeded = len(bits)/(1024*32) + 1;
        print "memoryBlocksNeeded = ",memoryBlocksNeeded
        outputfiles = [];
        for i in range(memoryBlocksNeeded):
            fno = self._odir+'/'+self._name+"_tmpi_"+str(i)+".txt";
            if os.path.exists(fno):
                os.remove(fno)
            outputfiles.append( open(fno,'w') ); 

        for a in range(cycles):
            
            for i in range(len(bits)):
                curbits.append(bits[i]);
                #print i
                outputfiles[self._currentMemoryBlock].write( list1[i]+'\n' );

                if (((i+1) % (1024*32) == 0) and (i > 0)) or (i == len(bits)-1):
                    print "[VipramCom: runTest] On memory block ",str(self._currentMemoryBlock);
                    self.sendInstructions(curbits,reset,isPower,nPowerCycles);     
                    self.retrieveRegisters(curbits);

                    outputfiles[self._currentMemoryBlock].close();                    

                    curbits[:] = []; #clear the list
                    self._currentMemoryBlock += 1;

                    if reset: break;   

    def sendInstructions(self, curbits, reset=False,isPower=False,nPowerCycles=1):

        bits = curbits;
        registers = self._registers;
        blockSize = self._blockSize;

        totalTimeSlices = len(bits);
        nInputs = len(registers);

        print "total time slices = ", totalTimeSlices
        dicedBits = [None]*nInputs;
        dicedBitsBinary = [None]*nInputs;
        for i in range(len(dicedBits)): dicedBits[i] = [None]*blockSize ;
        for i in range(len(dicedBitsBinary)): dicedBitsBinary[i] = [None]*blockSize ;

        iSteps = 0;
        fSteps = 32;
        stepIncrement = 32;

        #while len(bits) > iSteps+1:
        print "[VipramCom:sendInstructions] Translating instructions..."
        for a in range(blockSize):
            
            #if iSteps%100 == 0: print "iSteps = ", a, iSteps
            
            ## cycle through all inputs
            for i in range(nInputs):
                ## cycle through 32 bit increments of a particular input
                curword = [];
                for j in range(fSteps,iSteps,-1):
                    if j+1 < totalTimeSlices and not reset: curword.append( str(bits[j][i]) );
                    elif j+1 >= totalTimeSlices and not reset:
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

        print "[VipramCom:sendInstructions] Writing instructions to registers..."
        for i in range(nInputs):
            ## put the 32 bit word into memory
            if 'Out' in registers[i] or 'CheckData' in registers[i]: continue;
            self._hw.getNode("VipMEM."+registers[i]).writeBlock( dicedBits[i] );
            self._hw.dispatch();
            #print "input #",i," = ",registers[i]," and value = ", dicedBitsBinary[i][1023], dicedBitsBinary[i][1022]
            
        lengthOfBurst = 32768./float(self._freq)/1.e6;

        #go!
        if self._go:

            curtime = -99
            prevtime = -999.;
            for a in range(nPowerCycles):
                self._hw.getNode("VipMEM.Go").write(1);
                self._hw.dispatch();
                prevtime = curtime;
                curtime = time.time()
                difftime = curtime - prevtime;
                    
                sleeptime = 0;
                if lengthOfBurst > difftime: 
                    sleeptime = lengthOfBurst - difftime + 0.00005;
                    time.sleep(sleeptime);
                if a > 0: self._difftimes.append(sleeptime);
                #print "difftime = %.20f" % difftime;



                #sleepytime = float(32768./self._freq/1.e6);
                #print "sleepytime = ", sleepytime;
                #time.sleep(sleepytime);

                ################
                # if isPower:

                # reg0 = self._hw.getNode("VipMEM.V_DVDD").read()
                # reg1 = self._hw.getNode("VipMEM.V_VDD").read()
                # reg2 = self._hw.getNode("VipMEM.V_VPRECH").read()

                ireg0 = self._hw.getNode("VipMEM.I_DVDD").read()
                ireg1 = self._hw.getNode("VipMEM.I_VDD").read()
                ireg2 = self._hw.getNode("VipMEM.I_VPRECH").read()

                # vccreg = self._hw.getNode("VipMEM.V_VCC3V3").read()
                # tmpreg = self._hw.getNode("VipMEM.Temperature").read()
                # ltcreg = self._hw.getNode("VipMEM.LTC2991").read()

                self._hw.dispatch();

                # if a % 10000 == 0: 

                #     print "---------------"
                #     print "cycle = ",a

                    #print '{0:032b}'.format(reg0)
                    # print "V_DVDD = ",round(reg0*305.18/1.e6,3),"V"
                    # print "V_VDD = ",round(reg1*305.18/1.e6,3),"V"
                    # print "V_VPRECH = ",round(reg2*305.18/1.e6,3),"V"

                    # print "I_DVDD = ",round(ireg0*95.375,3),"uA"
                    # print "I_VDD = ",round(ireg1*95.375,3),"uA"
                    # print "I_VPRECH = ",round(ireg2*95.375,3),"uA"

                    # print "VCC3V3 = ", round(2.5+vccreg*305./1.e6,3),"V"
                    # print "Temperature = ", round(float(str(tmpreg))*0.0625,3),"C"
                    # print "LTC2991 = ", ltcreg

                self._i_dvdd.append( round(ireg0*95.375,3) );
                self._i_vdd.append( round(ireg1*95.375,3) );
                self._i_prech.append( round(ireg2*95.375,3) );

                ################

        # wait before trying to do any retrieving...
        time.sleep(0.1);    

    def retrieveRegisters(self,curbits):

        # get the output registers
        outMem = [];
        bits = curbits
        registers = self._registers;
        blockSize = self._blockSize;
        
        totalTimeSlices = len(bits);
        nInputs = len(registers);
        stepIncrement = 32;

        print "total time slices written out = ", min(1024*32,totalTimeSlices+500)

        print "[VipramCom:retrieveRegisters] Getting registers..."
        for i in range(nInputs):
            ## put the 32 bit word into memory
            if 'CheckData' in registers[i]: continue;
            curBlock = self._hw.getNode("VipMEM."+registers[i]).readBlock( blockSize );
            self._hw.dispatch();
            outMem.append( curBlock );
            # if "Out31" in registers[i]: 
            #     for k in range(1024): 
            #         print "Out31:", '{0:032b}'.format(curBlock[k]);
            #         print  '{0:032b}'.format(outMem[len(outMem)-1][k])

        fno = self._odir+'/'+self._name+"_tmpf_"+str(self._currentMemoryBlock)+".txt";
        fout = open(fno,'w');
        timeCtr = 0;

        print "[VipramCom:retrieveRegisters] Write out to file..."
        for a in range(blockSize):
            if a%100 == 0: print "Processed ", round(float(a)*100./float(blockSize),2), "% of the blocks";
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
        fout.close()

    def compareOutput(self):

        f1 = open(self._odir+'/'+self._name+'_tmpi_'+str(self._currentMemoryBlock)+'.txt','r');
        f2 = open(self._odir+'/'+self._name+'_tmpf_'+str(self._currentMemoryBlock)+'.txt','r');

        list1 = f1.read().split()
        list2 = f2.read().split()

        print "list1 lenghth = ", len(list1);
        print "list2 lenghth = ", len(list2);

        for i in range(len(list1)):

            checkData = list1[i][0];
            comp1 = list1[i][1:33]
            comp2 = list2[i][:32]
            row = int(list1[i][41:48][::-1],2);
            col = int(list1[i][48:53][::-1],2);

            #print list1[i], "check data = ", checkData
            #print list2[i]

            if int(checkData) == 1:
                self._checkDataDtr += 1;
                #print "time slice: ", i, ", checkData = ", checkData, ", row = ", row, ", col = ", col;
                if comp1 == comp2: self._matchCtr += 1;

                for bitctr in range(32):
                    if (comp1[bitctr:bitctr+1]== "1"): 
                        self.denom += 1;
                        if (comp2[bitctr:bitctr+1]== "1"): self.numer += 1;
            
        if (self._checkDataDtr !=0): print "test results: match eff = ",self._matchCtr,"/",self._checkDataDtr," = ",float(self._matchCtr)*100./float(self._checkDataDtr),"%"

        if (self.denom !=0): print "REAL test results: match eff = ",self.numer,"/",self.denom," = ",float(self.numer)*100./float(self.denom),"%"

                #print comp1, "check data = ", checkData
                #print comp2

 

    def changeClockFrequency(self, clock, M, delay):
        
         if M%2==0:
             ht = M /2; 
             lt = M/2;
             ed = 0;
         else:
             ht = M//2;
             lt  = M//2 + 1;
             ed = 1
         print ht," ",lt," ",ed;    

         Status = self._hw.getNode("VipMEM.Status").read();
         self._hw.dispatch();
         time.sleep(0.1);

         print "clockStatus = ", '{0:032b}'.format(Status);
         self._hw.getNode("VipMEM.Status").write(Status+1);
         self._hw.dispatch();
         time.sleep(0.1);

         self._hw.getNode("VipMEM.CLKPOWER").write(0xffff);
         self._hw.dispatch();
         time.sleep(0.1);
         clkpower = self._hw.getNode("VipMEM.CLKPOWER").read();
         self._hw.dispatch();
         print "CLKPOWER = "'{0:032b}'.format(clkpower);
         time.sleep(0.1);

         blockSize =2;

         CLKOUT   = [None]*2;
         if clock == "vco":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKFBOUT_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKFBOUT_2").read();
         elif clock == "clock0":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT0_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT0_2").read();
         elif clock == "clock1":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT1_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT1_2").read();
         elif clock == "clock2":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT2_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT2_2").read();
         elif clock == "clock3":    
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT3_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT3_2").read();
         else: 
             print "unknown clock";
         self._hw.dispatch();
             
         time.sleep(0.1);
      
         CLKREG   = [None]*2;
         CLKREG[0]  = '{0:032b}'.format(CLKOUT[0]);
         stringword = ''.join(CLKREG[0][:20] + '{0:06b}'.format(ht)+'{0:06b}'.format(lt));
         CLKREG[0] = ctypes.c_uint32(int(stringword,2)).value;               
         print "Clock:", clock, '{0:032b}'.format(CLKOUT[0]), " gets replaced by ", '{0:032b}'.format(CLKREG[0]);

         CLKREG[1]  = '{0:032b}'.format(CLKOUT[1]);
         stringword = ''.join(CLKREG[1][:24] + '{0:01b}'.format(ed) + CLKREG[1][25:26] + '{0:06b}'.format(delay));
         CLKREG[1] = ctypes.c_uint32(int(stringword,2)).value;               
         print "Clock:", clock, '{0:032b}'.format(CLKOUT[1]), " gets replaced by ", '{0:032b}'.format(CLKREG[1]);

       
         if clock == "vco":
             print "Writing to VCO";
             self._hw.getNode("VipMEM.CLKFBOUT_1").write(CLKREG[0]);
             self._hw.getNode("VipMEM.CLKFBOUT_2").write(CLKREG[1]);
         elif clock == "clock0":
             print "Writing to clock0";
             self._hw.getNode("VipMEM.CLKOUT0_1").write(CLKREG[0]);
             self._hw.getNode("VipMEM.CLKOUT0_2").write(CLKREG[1]);
         elif clock == "clock1":
             print "Writing to clock1";
             self._hw.getNode("VipMEM.CLKOUT1_1").write(CLKREG[0]);
             self._hw.getNode("VipMEM.CLKOUT1_2").write(CLKREG[1]);
         elif clock == "clock2":
             print "Writing to clock2";
             self._hw.getNode("VipMEM.CLKOUT2_1").write(CLKREG[0]);
             self._hw.getNode("VipMEM.CLKOUT2_2").write(CLKREG[1]);
         elif clock == "clock3":    
             print "Writing to clock3";
             self._hw.getNode("VipMEM.CLKOUT3_1").write(CLKREG[0]);
             self._hw.getNode("VipMEM.CLKOUT3_2").write(CLKREG[1]);
         else: 
             print "unknown clock"
         self._hw.dispatch();
         time.sleep(0.1);


         if clock == "vco":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKFBOUT_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKFBOUT_2").read();
         elif clock == "clock0":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT0_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT0_2").read();
         elif clock == "clock1":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT1_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT1_2").read();
         elif clock == "clock2":
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT2_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT2_2").read();
         elif clock == "clock3":    
             CLKOUT[0] = self._hw.getNode("VipMEM.CLKOUT3_1").read();
             CLKOUT[1] = self._hw.getNode("VipMEM.CLKOUT3_2").read();
         else: 
             print "unknown clock";
         self._hw.dispatch();


         print "After transaction:", clock;  
         print "Reg1:",    '{0:032b}'.format(CLKOUT[0]);
         print "Reg2:",    '{0:032b}'.format(CLKOUT[1]);

         Status = self._hw.getNode("VipMEM.Status").read();
         self._hw.dispatch();
         time.sleep(0.1);
         print "clockStatus = ", '{0:032b}'.format(Status);

         self._hw.getNode("VipMEM.Status").write(Status-1);
         self._hw.dispatch();
         time.sleep(0.1);
         
         Status = self._hw.getNode("VipMEM.Status").read();
         self._hw.dispatch();
         print "clockStatus after clock change= ", '{0:032b}'.format(Status);
         time.sleep(0.1);


