from ROOT import *
ROOT.gROOT.ProcessLine(".L ~/tdrstyle.C")
from ROOT import setTDRStyle
ROOT.setTDRStyle()
ROOT.gStyle.SetPadTopMargin(0.09);
ROOT.gStyle.SetPadLeftMargin(0.16);
ROOT.gStyle.SetHistMinimumZero()

class inputVisualizer:
    
    def __init__(self, fn):
        
        self.file = TFile(fn);
        self.tree = self.file.Get("tree");
        self.cycles = self.tree.GetEntries();
        #        for i in range(self.tree.GetEntries()):
        #            self.tree.GetEntry(i);
        #            print self.tree.counter
    
        #        self.inputPins = ["MLpreCh","RowAdr","ColAdr","RunMode","LatchData","Primary","EventReset",
        #                          "InputA","InputB","InputC","InputD"];
    
        self.inputPins = ["InputD","InputC","InputB","InputA",
                          "ColAdr","RowAdr",
                          "EventReset","RunMode","LatchData","Primary","MLpreCh"]    

    ############################        
    def textVisualizer(self):
        
        print "------------------------"
        print "-----> text out"
        
        l_MLpreCh = []
        l_RowAdr = []
        l_ColAdr = []
        l_RunMode = []        
        l_LatchData = []        
        l_Primary = []                
        l_EventReset = []    
        l_CheckData = []
        l_InputA = []                        
        l_InputA_bit0 = []                                
        l_InputB = []                        
        l_InputB_bit0 = []                                
        l_InputC = []                        
        l_InputC_bit0 = []                                
        l_InputD = []
        l_InputD_bit0 = []  
        
        l_Miss0 = []
        l_Miss1 = []
        l_Miss2 = []
        l_RequireLayerA = []        
        l_DataOut = []
        l_CompareNow = []
                
        for i in range(self.tree.GetEntries()):
            self.tree.GetEntry(i);
            
            l_MLpreCh.append(self.tree.MLpreCh);
            l_Primary.append(self.tree.Primary);
            l_LatchData.append(self.tree.LatchData);
            l_RunMode.append(self.tree.RunMode);
            l_EventReset.append(self.tree.EventReset);
            l_CheckData.append(self.tree.CheckData);
            l_RowAdr.append(self.tree.RowAdr);
            l_ColAdr.append(self.tree.ColAdr);
            l_InputA.append(self.tree.InputA);
            l_InputB.append(self.tree.InputB);
            l_InputC.append(self.tree.InputC);
            l_InputD.append(self.tree.InputD);
            l_InputA_bit0.append(self.tree.InputA_bit0);
            l_InputB_bit0.append(self.tree.InputB_bit0);
            l_InputC_bit0.append(self.tree.InputC_bit0);
            l_InputD_bit0.append(self.tree.InputD_bit0);
            l_Miss0.append(self.tree.Miss0);            
            l_Miss1.append(self.tree.Miss1);            
            l_Miss2.append(self.tree.Miss2);            
            l_RequireLayerA.append(self.tree.RequireLayerA); 
            tmpL = [];
            for k in range(32): tmpL.append( self.tree.DataOut[k] )
            l_DataOut.append(tmpL);
            l_CompareNow.append(self.tree.CompareNow);

#        for i in range(len(l_Miss0)):
#            print l_DataOut[i][0],l_DataOut[i][1]

#        print "MLpreCh:    ",l_MLpreCh
#        print "RowAdr:     ",l_RowAdr
#        print "ColAdr:     ",l_ColAdr
#        print "RunMode:    ",l_RunMode
#        print "LatchData:  ",l_LatchData
#        print "Primary:    ",l_Primary
#        print "EventReset: ",l_EventReset
#        print "InputA:     ",l_InputA
#        print "InputB:     ",l_InputB
#        print "InputC:     ",l_InputC
#        print "InputD:     ",l_InputD

        print "------------------------"

        #            print "InputD InputC InputB InputA ColAdr RowAdr EventReset LatchData Primary RunMode Miss0 Miss1 Miss2 RequireLayerA CheckData dataExpected compareNow"
        print "InputD_bit0 InputD InputC_bit0 InputC InputB_bit0 InputB InputA_bit0 InputA ColAdr RowAdr EventReset LatchData Primary RunMode Miss0 Miss1 Miss2 RequireLayerA CheckData dataExpected compareNow"
        for i in range(len(l_InputD)):
            oline = "";
            oline += str(l_InputD_bit0[i]) + " "
            oline += str(l_InputD[i]) + " "            
            oline += str(l_InputC_bit0[i]) + " "
            oline += str(l_InputC[i]) + " "
            oline += str(l_InputB_bit0[i]) + " "
            oline += str(l_InputB[i]) + " "
            oline += str(l_InputA_bit0[i]) + " "
            oline += str(l_InputA[i]) + " "
            oline += str(l_ColAdr[i]) + " "
            oline += str(l_RowAdr[i]) + " "
            oline += str(l_EventReset[i]) + " "
            oline += str(l_LatchData[i]) + " "
            oline += str(l_Primary[i]) + " "
            oline += str(l_RunMode[i]) + " "
            oline += str(l_Miss0[i]) + " "  
            oline += str(l_Miss1[i]) + " "  
            oline += str(l_Miss2[i]) + " "  
            oline += str(l_RequireLayerA[i]) + " "  
            oline += str(l_CheckData[i]) + " "
            for j in range(32): oline += str(l_DataOut[i][j])
            oline += " "
            oline += str(l_CompareNow[i]) + " "
            #print oline
            
            olinehex = "";
            olinehex += '{0:01x}'.format(l_InputD_bit0[i]) + " "
            olinehex += '{0:04x}'.format(l_InputD[i]) + " "            
            olinehex += '{0:01x}'.format(l_InputC_bit0[i]) + " "
            olinehex += '{0:04x}'.format(l_InputC[i]) + " "
            olinehex += '{0:01x}'.format(l_InputB_bit0[i]) + " "
            olinehex += '{0:04x}'.format(l_InputB[i]) + " "
            olinehex += '{0:01x}'.format(l_InputA_bit0[i]) + " "
            olinehex += '{0:04x}'.format(l_InputA[i]) + " "
            olinehex += '{0:03x}'.format(l_ColAdr[i]) + " "
            olinehex += '{0:03x}'.format(l_RowAdr[i]) + " "
            olinehex += '{0:01x}'.format(l_EventReset[i]) + " "
            olinehex += '{0:01x}'.format(l_LatchData[i]) + " "
            olinehex += '{0:01x}'.format(l_Primary[i]) + " "
            olinehex += '{0:01x}'.format(l_RunMode[i]) + " "
            olinehex += '{0:01x}'.format(l_Miss0[i]) + " "  
            olinehex += '{0:01x}'.format(l_Miss1[i]) + " "  
            olinehex += '{0:01x}'.format(l_Miss2[i]) + " "  
            olinehex += '{0:01x}'.format(l_RequireLayerA[i]) + " "  
            olinehex += '{0:01x}'.format(l_CheckData[i]) + " "
            for j in range(32): olinehex += '{0:01x}'.format(l_DataOut[i][j])
            olinehex += " "            
#            olinehex += '{0:08x}'.format(l_DataOut[i][j]) + " "
#            olinehex += '{0:01x}'.format(l_CompareNow[i]) + " "
            print "--- olinehex =, i: ",i+1,"  ",olinehex

    ############################
    def initializeToNegOne(self,h):
        for i in range(1, h.GetNbinsX()+1):
            for j in range(1, h.GetNbinsY()+1):
                h.SetBinContent(i,j,-1);
    
    ############################
    def visualize(self, fn = "test.eps", init = 0, final = -1):

        if final < 0: final = self.cycles;
        
        cWidth = ((final-init)/10.) * 800
        xlo = init;
        xhi = final;
        ylo = 0;
        yhi = 2*len(self.inputPins)+1;

        print "xhi: ", xhi;
        print "yhi: ", yhi;        
        
        Can = TCanvas( "Can","Can", int(cWidth), 800 );
        Can.SetGrid(1,1);
        Hist = Can.DrawFrame(xlo,ylo,xhi,yhi);
        HistLabels = TH2I("HistLabels","HistLabels", xhi-xlo, xlo, xhi, yhi, ylo, yhi );
        for i in range(1,len(self.inputPins)+1):
            HistLabels.GetYaxis().SetBinLabel(2*i, self.inputPins[i-1]);
        HistLabels.Draw();
        HistLabels.GetXaxis().SetNdivisions(xhi);
        
        h_MLpreCh = TH1I("h_MLpreCh","h_MLpreCh", xhi-xlo, xlo, xhi);
        h_Primary = TH1I("h_Primary","h_Primary", xhi-xlo, xlo, xhi);
        h_LatchData = TH1I("h_LatchData","h_LatchData", xhi-xlo, xlo, xhi);
        h_RunMode = TH1I("h_RunMode","h_RunMode", xhi-xlo, xlo, xhi);
        h_EventReset = TH1I("h_EventReset","h_EventReset", xhi-xlo, xlo, xhi);
        h_MLpreCh.SetLineColor( ROOT.kRed );
        h_Primary.SetLineColor( ROOT.kBlue );
        h_LatchData.SetLineColor( ROOT.kMagenta );
        h_RunMode.SetLineColor( ROOT.kGreen+2 );
        h_EventReset.SetLineColor( ROOT.kOrange );
        h_MLpreCh.SetLineWidth( 2 );
        h_Primary.SetLineWidth( 2 );
        h_LatchData.SetLineWidth( 2 );
        h_RunMode.SetLineWidth( 2 );
        h_EventReset.SetLineWidth( 2 );

        h_RowAdr= TH2I("h_RowAdr","h_RowAdr", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        h_ColAdr= TH2I("h_ColAdr","h_ColAdr", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        h_InputA= TH2I("h_InputA","h_InputA", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        h_InputB= TH2I("h_InputB","h_InputB", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        h_InputC= TH2I("h_InputC","h_InputC", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        h_InputD= TH2I("h_InputD","h_InputD", xhi-xlo, xlo, xhi, yhi, ylo, yhi);        
        self.initializeToNegOne(h_RowAdr);
        self.initializeToNegOne(h_ColAdr);
        self.initializeToNegOne(h_InputA);
        self.initializeToNegOne(h_InputB);
        self.initializeToNegOne(h_InputC);
        self.initializeToNegOne(h_InputD);
        h_RowAdr.SetMinimum(0);
        h_ColAdr.SetMinimum(0);
        h_InputA.SetMinimum(0);
        h_InputB.SetMinimum(0);
        h_InputC.SetMinimum(0);
        h_InputD.SetMinimum(0);

        for i in range(0,final):
            self.tree.GetEntry(i);                
            h_MLpreCh.SetBinContent(i+1, tree.MLpreCh+self.inputPins.index("MLpreCh")*2+1);
            h_Primary.SetBinContent(i+1, tree.Primary+self.inputPins.index("Primary")*2+1);
            h_LatchData.SetBinContent(i+1, tree.LatchData+self.inputPins.index("LatchData")*2+1);
            h_RunMode.SetBinContent(i+1, tree.RunMode+self.inputPins.index("RunMode")*2+1);
            h_EventReset.SetBinContent(i+1, tree.EventReset+self.inputPins.index("EventReset")*2+1);            
            
            h_RowAdr.SetBinContent(i+1,self.inputPins.index("RowAdr")*2+2, tree.RowAdr);
            h_ColAdr.SetBinContent(i+1,self.inputPins.index("ColAdr")*2+2, tree.ColAdr);
            h_InputA.SetBinContent(i+1,self.inputPins.index("InputA")*2+2, tree.InputA);
            h_InputB.SetBinContent(i+1,self.inputPins.index("InputB")*2+2, tree.InputB);
            h_InputC.SetBinContent(i+1,self.inputPins.index("InputC")*2+2, tree.InputC);
            h_InputD.SetBinContent(i+1,self.inputPins.index("InputD")*2+2, tree.InputD);

        h_MLpreCh.Draw("histsames");
        h_Primary.Draw("histsames");
        h_LatchData.Draw("histsames");
        h_RunMode.Draw("histsames");
        h_EventReset.Draw("histsames");

        h_RowAdr.Draw("TEXTsames");
        h_ColAdr.Draw("TEXTsames");
        h_InputA.Draw("TEXTsames");
        h_InputB.Draw("TEXTsames");
        h_InputC.Draw("TEXTsames");
        h_InputD.Draw("TEXTsames");

        Can.SaveAs(fn);

    

    ############################
    def writeToText(self, fn = "test.txt", writeExpectedOutput=False):
        
        print "------------------------"
        print "-----> written to "+fn
        f = open(fn, "w")
        
        self.theBitInstructions = [];
        
        for i in range(self.tree.GetEntries()):
            if i % 100 == 0: "Writing out, cycle: ", i
            self.tree.GetEntry(i);
            
            thisString = ""; 
            
#            thisString += self.flipBits('{0:01b}'.format(self.tree.CompareNow))
            thisString += self.flipBits('{0:01b}'.format(self.tree.CheckData))
            if writeExpectedOutput: 
                for j in range(32-1,-1,-1): thisString += '{0:01b}'.format(self.tree.DataOut[j])

            thisString += self.flipBits('{0:01b}'.format(self.tree.RequireLayerA))
            thisString += self.flipBits('{0:01b}'.format(self.tree.Miss2))
            thisString += self.flipBits('{0:01b}'.format(self.tree.Miss1))
            thisString += self.flipBits('{0:01b}'.format(self.tree.Miss0))
            thisString += self.flipBits('{0:01b}'.format(self.tree.RunMode))            
            thisString += self.flipBits('{0:01b}'.format(self.tree.Primary))
            thisString += self.flipBits('{0:01b}'.format(self.tree.LatchData))
            thisString += self.flipBits('{0:01b}'.format(self.tree.EventReset))
            
            #thisString += ' '
            
#            thisString += self.flipBits('{0:07b}'.format(self.tree.RowAdr))
#            thisString += self.flipBits('{0:05b}'.format(self.tree.ColAdr))
            thisString += self.flipBits('{0:07b}'.format(self.tree.RowAdr))
            thisString += self.flipBits('{0:05b}'.format(self.tree.ColAdr))
    
#            thisString += '{0:015b}'.format(self.tree.InputA)
            thisString += self.flipBits('{0:015b}'.format(self.tree.InputA))

            thisString += self.flipBits('{0:01b}'.format(self.tree.InputA_bit0))
#            thisString += '{0:015b}'.format(self.tree.InputB)
            thisString += self.flipBits('{0:015b}'.format(self.tree.InputB))

            thisString += self.flipBits('{0:01b}'.format(self.tree.InputB_bit0))
#            thisString += '{0:015b}'.format(self.tree.InputC)
            thisString += self.flipBits('{0:015b}'.format(self.tree.InputC))

            thisString += self.flipBits('{0:01b}'.format(self.tree.InputC_bit0))
#            thisString += '{0:015b}'.format(self.tree.InputD)
            thisString += self.flipBits('{0:015b}'.format(self.tree.InputD))

            thisString += self.flipBits('{0:01b}'.format(self.tree.InputD_bit0))

            f.write(thisString+"\n")
            self.theBitInstructions.append(thisString);
                
        print "------------------------"
        return self.theBitInstructions;

    def flipBits(self, theString):

        stringList = list(theString);
        reversedStringList = [];
        for i in range(len(stringList)-1,-1,-1):
            reversedStringList.append(stringList[i]);
        return "".join(reversedStringList)


