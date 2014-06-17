from ROOT import *
from array import array

class inputBuilder:

    def __init__(self, fn):
    
        self.fn = fn;
        self.file = TFile(fn,"RECREATE");
        self.tree = TTree("tree","tree");
        self.cycleCtr = 0;
    
        # internal storage of patterns
        self.iInputA = [];
        self.iInputC = [];
        self.iInputB = [];
        self.iInputD = [];   
        self.iCamStateA = [];
        self.iCamStateB = [];
        self.iCamStateC = [];
        self.iCamStateD = [];           
        self.iDataOut = [];                
        for i in range(128):
            self.iInputA.append( [0]*32 );
            self.iInputB.append( [0]*32 );                
            self.iInputC.append( [0]*32 );                
            self.iInputD.append( [0]*32 );   
            self.iCamStateA.append( [0]*32 );
            self.iCamStateB.append( [0]*32 );                
            self.iCamStateC.append( [0]*32 );                
            self.iCamStateD.append( [0]*32 );   
            self.iDataOut.append( [0]*32 );                        

        # branches
        self.counter = array( 'i', [ 0 ] );             
        
        self.MLpreCh = array( 'i', [ 0 ] );             
        self.RowAdr = array( 'i', [ 0 ] );                     
        self.ColAdr = array( 'i', [ 0 ] );                             
        self.RunMode = array( 'i', [ 0 ] );                                     
        self.LatchData = array( 'i', [ 0 ] );                                             
        self.Primary = array( 'i', [ 0 ] );                                                     
        self.EventReset = array( 'i', [ 0 ] );  
        
        self.InputA = array( 'i', [ 0 ] );  
        self.InputB = array( 'i', [ 0 ] );  
        self.InputC = array( 'i', [ 0 ] );  
        self.InputD = array( 'i', [ 0 ] );  
        self.InputA_bit0 = array( 'i', [ 0 ] );  
        self.InputB_bit0 = array( 'i', [ 0 ] );  
        self.InputC_bit0 = array( 'i', [ 0 ] );  
        self.InputD_bit0 = array( 'i', [ 0 ] );  
    
        self.Miss0 = array( 'i', [ 0 ] );             
        self.Miss1 = array( 'i', [ 0 ] );             
        self.Miss2 = array( 'i', [ 0 ] );             
        self.RequireLayerA = array( 'i', [ 0 ] );                 
        self.majorityLogic = [0,0,0,0];
        
        self.CheckData = array( 'i', [ 0 ] );      
        self.DataOut = array( 'i', [ 0 ]*32 );  
        self.CompareNow = array( 'i', [ 0 ] );      
    
    
        self.tree.Branch("counter", self.counter , "counter/I");
        self.tree.Branch("MLpreCh", self.MLpreCh , "MLpreCh/I");
        self.tree.Branch("RowAdr", self.RowAdr , "RowAdr/I");
        self.tree.Branch("ColAdr", self.ColAdr , "ColAdr/I");
        self.tree.Branch("RunMode", self.RunMode , "RunMode/I");
        self.tree.Branch("LatchData", self.LatchData , "LatchData/I");
        self.tree.Branch("Primary", self.Primary , "Primary/I");
        self.tree.Branch("EventReset", self.EventReset , "EventReset/I");
    
        self.tree.Branch("Miss0", self.Miss0 , "Miss0/I");
        self.tree.Branch("Miss1", self.Miss1 , "Miss1/I");
        self.tree.Branch("Miss2", self.Miss2 , "Miss2/I");
        self.tree.Branch("RequireLayerA", self.RequireLayerA , "RequireLayerA/I");    
    
        self.tree.Branch("InputA", self.InputA , "InputA/I");    
        self.tree.Branch("InputB", self.InputB , "InputB/I");    
        self.tree.Branch("InputC", self.InputC , "InputC/I");    
        self.tree.Branch("InputD", self.InputD , "InputD/I");    
        self.tree.Branch("InputA_bit0", self.InputA_bit0 , "InputA_bit0/I");    
        self.tree.Branch("InputB_bit0", self.InputB_bit0 , "InputB_bit0/I");    
        self.tree.Branch("InputC_bit0", self.InputC_bit0 , "InputC_bit0/I");    
        self.tree.Branch("InputD_bit0", self.InputD_bit0 , "InputD_bit0/I");    
        
        self.tree.Branch("CheckData", self.CheckData , "CheckData/I");        
        self.tree.Branch("DataOut", self.DataOut , "DataOut[32]/I");  
        self.tree.Branch("CompareNow", self.CompareNow, "CompareNow/I");
    
    ##################################################
    # L O A D   M O D E   F U N C T I O N S
    # -------------------
    # initializeLoadPhase
    def initializeLoadPhase(self):
        #print "initializing load phase..."
        
        self.counter[0] = self.cycleCtr;

        self.MLpreCh[0] = 1;
        self.RowAdr[0] = 0; #rows 0-127
        self.ColAdr[0] = 0; #cols 0-31
        self.RunMode[0] = 0;
        self.LatchData[0] = 0;
        self.Primary[0] = 1;
        self.EventReset[0] = 0;
        
        self.InputA[0] = 0;
        self.InputB[0] = 0;
        self.InputC[0] = 0;
        self.InputD[0] = 0;
        self.InputA_bit0[0] = 1;
        self.InputB_bit0[0] = 1;
        self.InputC_bit0[0] = 1;
        self.InputD_bit0[0] = 1;

        self.Miss0[0] = 0;
        self.Miss1[0] = 0;
        self.Miss2[0] = 0;
        self.RequireLayerA[0] = 0;

        self.CheckData[0] = 0;
        self.CompareNow[0] = 0;        
        for i in range(32): self.DataOut[i] = 1;
        
        #print self.DataOut
        
        #fill, ctr++
        self.cycleCtr += 1;
        self.tree.Fill();

    # -------------------
    # loadRandomPatterns
    #def loadRandomPatterns(self, nPatterns):
    #    #print "loading random patterns..."
        
    # -------------------
    # loadUniformPatterns
    def loadUniformPatterns(self, row, col, iVal, multiplicativeFactor = 1, disableInputs = 1):
        # primary
        
        self.counter[0] = self.cycleCtr;
        self.RowAdr[0] = row;
        self.ColAdr[0] = col;
        self.Primary[0] = 1;
        
        self.InputA[0] = iVal;
        self.InputB[0] = iVal;
        self.InputC[0] = iVal;
        self.InputD[0] = iVal;
        
        self.InputD_bit0[0] = disableInputs;

        self.iInputA[row][col] = iVal;
        self.iInputB[row][col] = iVal;
        self.iInputC[row][col] = iVal;
        self.iInputD[row][col] = iVal;
        
        self.LatchData[0] = 0;
        
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();

        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 1;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();

        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 0;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();

        # secondary
        # set ternary bits
        
        self.counter[0] = self.cycleCtr;
        self.Primary[0] = 0;

        ternary_iVal = self.flipTernaryBits(iVal);
        
        #print "----------"
        #print "iVal  = ", iVal
        #print "binary  = ", '{0:015b}'.format(iVal)
        #print "binaryt = ", '{0:015b}'.format(ternary_iVal)
        #print "iValt = ", ternary_iVal
        
        self.InputA[0] = ternary_iVal;
        self.InputB[0] = ternary_iVal;
        self.InputC[0] = ternary_iVal;
        self.InputD[0] = ternary_iVal;
        
        self.LatchData[0] = 0;

        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 1;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 0;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1;
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();

        #print self.DataOut

    # -------------------
    # loadSinglePattern
    def loadSinglePattern(self, row, col, iVal, multiplicativeFactor = 1, disableInputs = 1):
        #print "loading random patterns..."
        
        # primary
        
        self.counter[0] = self.cycleCtr;
        self.RowAdr[0] = row;
        self.ColAdr[0] = col;
        self.Primary[0] = 1;
        
        self.InputA[0] = iVal[0];
        self.InputB[0] = iVal[1];
        self.InputC[0] = iVal[2];
        self.InputD[0] = iVal[3];
        
        self.InputD_bit0[0] = disableInputs;
        
        self.iInputA[row][col] = iVal[0];
        self.iInputB[row][col] = iVal[1];
        self.iInputC[row][col] = iVal[2];
        self.iInputD[row][col] = iVal[3];
        
        self.LatchData[0] = 0;

        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 1;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 0;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1;
	if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill(); 
        
        # secondary
        # set ternary bits
        
        self.counter[0] = self.cycleCtr;
        self.Primary[0] = 0;
        
        ternary_iVal_0 = self.flipTernaryBits(iVal[0]);
        ternary_iVal_1 = self.flipTernaryBits(iVal[1]);
        ternary_iVal_2 = self.flipTernaryBits(iVal[2]);
        ternary_iVal_3 = self.flipTernaryBits(iVal[3]);        
        
        self.InputA[0] = ternary_iVal_0;
        self.InputB[0] = ternary_iVal_1;
        self.InputC[0] = ternary_iVal_2;
        self.InputD[0] = ternary_iVal_3;
        
        self.LatchData[0] = 0;

        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 1;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
        if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        self.counter[0] = self.cycleCtr;            
        self.LatchData[0] = 0;
        ctrMF = 0;
        while ctrMF < multiplicativeFactor:
            self.cycleCtr += 1;
            self.tree.Fill();
            ctrMF += 1; 
	if ctrMF == 0:
            self.cycleCtr += 1;
            self.tree.Fill();
        
        #print self.DataOut

    # -------------------
    # flipTernaryBits
    def flipTernaryBits(self, iVal):
        
        binaryVal = list('{0:015b}'.format(iVal))
        #print "len(binaryVal) = ", len(binaryVal)
        #print binaryVal
        
        if binaryVal[14] == "1": binaryVal[14] = "0";
        else: binaryVal[14] = "1";
        if binaryVal[9] == "1": binaryVal[9] = "0";
        else: binaryVal[9] = "1";
        if binaryVal[4] == "1": binaryVal[4] = "0";
        else: binaryVal[4] = "1";

#        if binaryVal[10] == "1": binaryVal[10] = "0";
#        else: binaryVal[10] = "1";
#        if binaryVal[5] == "1": binaryVal[5] = "0";
#        else: binaryVal[5] = "1";
#        if binaryVal[0] == "1": binaryVal[0] = "0";
#        else: binaryVal[0] = "1";
        
        
        #print binaryVal
        binValString = "".join(binaryVal);
        #print binValString
        return int(binValString,2)
        


    ##################################################
    # R U N   M O D E   F U N C T I O N S
    # -------------------
    # initializeRunPhase
    def initializeRunPhase(self, logic = [1,1,1,1], initialRow = 1):
        #print "initializing run phase..."
        
        self.counter[0] = self.cycleCtr;
        
        self.MLpreCh[0] = 1;
        self.RowAdr[0] = initialRow; #rows 0-127
        self.ColAdr[0] = 0; #cols 0-31
        self.RunMode[0] = 1;
        self.LatchData[0] = 0;
        self.Primary[0] = 0;
        self.EventReset[0] = 1;
        for i in range(128):
            for j in range(32):
                self.iCamStateA[i][j] = 0;
                self.iCamStateB[i][j] = 0;
                self.iCamStateC[i][j] = 0;
                self.iCamStateD[i][j] = 0;
                self.iDataOut[i][j] = 0;

        self.InputA[0] = 0;
        self.InputB[0] = 0;
        self.InputC[0] = 0;
        self.InputD[0] = 0;
        self.InputA_bit0[0] = 0;
        self.InputB_bit0[0] = 0;
        self.InputC_bit0[0] = 0;
        self.InputD_bit0[0] = 0;
        
        self.Miss0[0] = logic[0];
        self.Miss1[0] = logic[1];
        self.Miss2[0] = logic[2];
        self.RequireLayerA[0] = logic[3];
        self.majorityLogic = logic;
        
        self.CheckData[0] = 0;
        self.CompareNow[0] = 0;                
        for i in range(32): self.DataOut[i] = 0;
        
        #fill, ctr++
        self.cycleCtr += 1;
        self.tree.Fill();

        #print self.DataOut

    # -------------------
    # changeLogic
    def changeLogic(self, logic = [1,1,1,1]):
        #print "initializing run phase..."
        
        self.counter[0] = self.cycleCtr;
        
        self.MLpreCh[0] = 1;
        self.RowAdr[0] = 0; #rows 0-127
        self.ColAdr[0] = 0; #cols 0-31
        self.RunMode[0] = 1;
        self.LatchData[0] = 0;
        self.Primary[0] = 0;
        self.EventReset[0] = 0;
        for i in range(128):
            for j in range(32):
                self.iCamStateA[i][j] = 0;
                self.iCamStateB[i][j] = 0;
                self.iCamStateC[i][j] = 0;
                self.iCamStateD[i][j] = 0;
        
        self.InputA[0] = 0;
        self.InputB[0] = 0;
        self.InputC[0] = 0;
        self.InputD[0] = 0;
        self.InputA_bit0[0] = 1;
        self.InputB_bit0[0] = 1;
        self.InputC_bit0[0] = 1;
        self.InputD_bit0[0] = 1;
        
        self.Miss0[0] = logic[0];
        self.Miss1[0] = logic[1];
        self.Miss2[0] = logic[2];
        self.RequireLayerA[0] = logic[3];
        self.majorityLogic = logic;
        
        self.CheckData[0] = 0;
        self.CompareNow[0] = 0;                
        for i in range(32): self.DataOut[i] = 0;
        
        #fill, ctr++
        self.cycleCtr += 1;
        self.tree.Fill();

    #print self.DataOut



    # -------------------
    # checkPattern
    def checkPattern(self, pattern, specificRow = 0):
        if not len(pattern) == 4: 
            print "=========== Error in pattern format!";
            return;
        else:
            self.counter[0] = self.cycleCtr;

            self.MLpreCh[0] = 1;
            self.EventReset[0] = 0;
            
            self.RowAdr[0] = specificRow;            

            if pattern[0] >= 0: self.InputA[0] = pattern[0];
            else: self.InputA[0] = 0;
            if pattern[1] >= 0: self.InputB[0] = pattern[1];
            else: self.InputB[0] = 0;
            if pattern[2] >= 0: self.InputC[0] = pattern[2];
            else: self.InputC[0] = 0;
            if pattern[3] >= 0: self.InputD[0] = pattern[3];
            else: self.InputD[0] = 0;

            if pattern[0] >= 0: self.InputA_bit0[0] = 1;
            else: self.InputA_bit0[0] = 0;
            if pattern[1] >= 0: self.InputB_bit0[0] = 1;
            else: self.InputB_bit0[0] = 0;
            if pattern[2] >= 0: self.InputC_bit0[0] = 1;
            else: self.InputC_bit0[0] = 0;
            if pattern[3] >= 0: self.InputD_bit0[0] = 1;
            else: self.InputD_bit0[0] = 0;
            
            self.CheckData[0] = 0;
            self.CompareNow[0] = 0;                    
            for i in range(32): self.DataOut[i] = 0;

#            #fill, ctr++
#            self.cycleCtr += 1;
#            self.tree.Fill();
        
            #self.MLpreCh[0] = 0;
            #self.counter[0] = self.cycleCtr;
            #self.cycleCtr += 1;
            #self.tree.Fill();

            self.cycleCtr += 1;
                        
            self.setInternalCams( pattern );
            self.checkLogicInternally();

            #print self.DataOut
            for i in range(32): self.DataOut[i] = self.iDataOut[specificRow][i];

            #fill, ctr++
            self.tree.Fill();


    # setInternalCams
    def setInternalCams(self, pattern):
        
        for i in range(128):
            for j in range(32):
                if self.iInputA[i][j] == pattern[0]: self.iCamStateA[i][j] = 1;
                if self.iInputB[i][j] == pattern[1]: self.iCamStateB[i][j] = 1;
                if self.iInputC[i][j] == pattern[2]: self.iCamStateC[i][j] = 1;
                if self.iInputD[i][j] == pattern[3]: self.iCamStateD[i][j] = 1;

    # checkPatternInternally
    def checkLogicInternally(self):
                
        for i in range(128):
            for j in range(32):
                
                missCtr = 0;
                missCtrA = 0;                
                if self.iCamStateA[i][j] == 1: 
                    missCtr += 1;
                    missCtrA += 1;                
                if self.iCamStateB[i][j] == 1: missCtr += 1;
                if self.iCamStateC[i][j] == 1: missCtr += 1;
                if self.iCamStateD[i][j] == 1: missCtr += 1;                
                
                bLogic = False;    
                if (missCtr == 4 and self.majorityLogic[0] == 1) or (missCtr == 3 and self.majorityLogic[1] == 1) or (missCtr == 2 and self.majorityLogic[2] == 1) or (missCtrA == 1 and self.majorityLogic[3] == 1): bLogic = True;
                
                passMiss0 = 0;
                passMiss1 = 0;
                passMiss2 = 0;
                passReqLayA = 0;                    
                if (missCtr == 4 and self.majorityLogic[0] == 1): passMiss0 = 1;
                if (missCtr == 3 and self.majorityLogic[1] == 1): passMiss1 = 1;
                if (missCtr == 2 and self.majorityLogic[2] == 1): passMiss2 = 1;
                if (missCtrA == 1 and self.majorityLogic[3] == 1): passReqLayA = 1;            
                #print "self.cycleCtr = ", self.cycleCtr, " -- ", bLogic,",",i, ",",passMiss0,",",passMiss1,",",passMiss2,",",passReqLayA

                if bLogic: self.iDataOut[i][j] = 1;

    # checkPatternInternally
    #    def checkLogic(self, pattern, iA, iB, iC, iD):
    #        
    #        logic = 0;
    #        
    #        
    #        
    #        missCtr = 0;
    #        missCtrA = 0;
    #        if pattern[0] == iA: 
    #            missCtr += 1;
    #            missCtrA += 1;
    #        if pattern[1] == iB: missCtr += 1;
    #        if pattern[2] == iC: missCtr += 1;
    #        if pattern[3] == iD: missCtr += 1;
    #        
    #        bLogic = False;    
    #        if (missCtr == 4 and self.majorityLogic[0] == 1) or (missCtr == 3 and self.majorityLogic[1] == 1) or (missCtr == 2 and self.majorityLogic[2] == 1) or (missCtrA == 1 and self.majorityLogic[3] == 1): bLogic = True;
    #        
    #        if bLogic: logic = 1;
    #        return logic;

    # loadRowChecker
    def doRowChecker( self, row ):

        self.CheckData[0] = 1;                    
        self.CompareNow[0] = 1;        
        self.RowAdr[0] = row;
        for i in range(32): self.DataOut[i] = self.iDataOut[row][i];

        self.counter[0] = self.cycleCtr;
        self.cycleCtr += 1;
        self.tree.Fill();

        #print self.DataOut
        for i in range(32): self.DataOut[i] = 0;

    ##################################################
    # -------------------
    # readOutMode
    def readOutMode(self):
        for i in range(128): self.doRowChecker(i)

    ##################################################
    # -------------------
    # close
    def close(self):
        #print "closing "+self.fn+"..."
        self.tree.Write();
        self.file.Close();

    # -------------------
    # printInternalPatterns
    def printInternalPatterns(self, row = -1, col = -1):

        if row >= 0 and col >= 0:
            print self.iInputA[row][col]
            print self.iInputB[row][col]
            print self.iInputC[row][col]
            print self.iInputD[row][col]
        
        if col >= 0 and row < 0:
            for i in range(128):
                print "-------- ",i
                print self.iInputA[i][col]
                print self.iInputB[i][col]
                print self.iInputC[i][col]
                print self.iInputD[i][col]        
            
        if col < 0 and row >= 0:
            print self.iInputA[row]
            print self.iInputB[row]
            print self.iInputC[row]
            print self.iInputD[row]
        
        if row < 0 and col < 0:
            for i in range(128):
                print "-------- ",i
                print self.iInputA[i]
                print self.iInputB[i]
                print self.iInputC[i]
                print self.iInputD[i]        

    # -------------------
    # printInternalPatterns
    def drawInternalMatches(self, fn = "testO.eps"):
        
        hist2d = TH2I("hist2d","hist2d",32,0,32,128,0,128);
        for i in range(128):
            for j in range(32):
                hist2d.SetBinContent( j+1, i+1, self.iDataOut[i][j] );
        canO = TCanvas("canO","canO",1600,1600);
        canO.SetGrid();
        hist2d.GetXaxis().SetNdivisions(32,kFALSE);
        hist2d.GetYaxis().SetNdivisions(64,kFALSE);    
        hist2d.GetXaxis().SetLabelSize(0.02);
        hist2d.GetYaxis().SetLabelSize(0.02);
        hist2d.GetXaxis().SetTickLength(0);    
        hist2d.GetYaxis().SetTickLength(0); 
        
        hist2d.Draw("colz");
        canO.SaveAs("testO.eps");
                                   
    # -------------------
    # getFilename
    def getFilename(self):
        return self.fn;






