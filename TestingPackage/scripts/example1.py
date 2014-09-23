import random
import sys
import numpy as np

sys.path.insert(0, '../interface')
from pVIPRAM_inputBuilderClass import *


#########################################################
#########################################################
#########################################################
#########################################################

def exampleTest(filename):
    
    inputPattern = inputBuilder("dat/"+filename+".root");
    inputPattern.initializeLoadPhase();
    inputPattern.loadUniformPatterns(9, 9, 27, 1);
    inputPattern.loadUniformPatterns(9, 11, 37, 1);
    inputPattern.loadUniformPatterns(9, 13, 47, 1);
    inputPattern.loadUniformPatterns(9, 15, 57, 1);
    inputPattern.loadUniformPatterns(9, 17, 67, 1);
    inputPattern.initializeRunPhase( [1,0,0,0] );
    for i in range(20): inputPattern.checkPattern( [01,01,01,01] ,9);
    
    for i in range(10): inputPattern.checkPattern( [27,27,27,27] ,9);
    inputPattern.doRowChecker(9);
    for i in range(10): inputPattern.checkPattern( [37,37,37,37] ,9);
    inputPattern.doRowChecker(9);    
    for i in range(10): inputPattern.checkPattern( [47,47,47,47] ,9);
    inputPattern.doRowChecker(9);

    for i in range(20): inputPattern.checkPattern( [01,01,01,01] ,9);
    #inputPattern.readOutMode();
    inputPattern.close();
    return inputPattern;


def exampleTest1(filename):

    inputPattern = inputBuilder("dat/"+filename+".root");
    inputPattern.initializeLoadPhase();
    for row in range(0, 10):
        for col in range(0, 32):
            inputPattern.loadSinglePattern(row, col, [55,55,55,55], 2);
            #inputPattern.loadUniformPatterns(row, col, 55, 2);

    inputPattern.initializeRunPhase( [1,0,0,0] );

    for i in range(10): inputPattern.checkPattern( [55,55,55,55] ,0);

    for row in range(0,10):
        for i in range(0, 10*5):
            inputPattern.checkPattern([21845, 21845, 21845, 21845], row)
        inputPattern.doRowChecker(row)
        for i in range(0, 10*5):
            inputPattern.checkPattern([21845, 21845, 21845, 21845], row)

    inputPattern.close();
    return inputPattern;

#########################################################
#########################################################
#########################################################
#########################################################
def stressTest(filename, N, freq):

	inputP = inputBuilder("dat/" + filename + ".root")
	inputP.initializeLoadPhase()
	
	# N value
	#prob = int(sys.argv[2]);
	prob = int(N)
	# frequency
	# mult = (int(sys.argv[3])/10)+1
	mult = (int(freq)/10)+1;

	print "N% = ", prob, ", Multiplier = ", mult

	# n rows
	#nrows = 128;
	nrows = 6;
	ncols = 32;

	#infoFile = open("NewStressInfoFile.txt", "a")
	infoList = [];
	## ---------------------------------
	## Load mode
	print "RUNNING LOAD MODE!!"
	for row in range(0,128):
		tmpInfoList = [];
		for col in range(0, 32):
			if (random.randint(1, 100) > prob):
				inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
				#print "Loaded [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
				#infoFile.write(str("N "))
				tmpInfoList.append(0);
			else:
				inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
				#print "Loaded [32767, 32767, 32767, 32767] in Row: " + str(row) + ", Col: " + str(col)
				tmpInfoList.append(1);
		infoList.append( tmpInfoList );

	print "RUN LOAD+CHECK MODE!!"
	## Load + Check
	for row in range(0,nrows):
		print "load + check in row ", row
		for col in range(0,ncols,4):
			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
			#print "Loading and Checking [32766, 32766, 32766, 32766] at Row: " + str(row) + ", Col: " + str(col)
			for iteration in range(0, 1):
				inputP.initializeRunPhase([1, 0, 0, 0])
				inputP.checkPattern([21845, 21845, 21845, 21845], row)
				inputP.checkPattern([32766, 32766, 32766, 32766], row)
				for i in range(0, 10*mult):
					inputP.checkPattern([21845, 21845, 21845, 21845], row)
				inputP.doRowChecker(row,col)
				for i in range(0, 10*mult):
					inputP.checkPattern([21845, 21845, 21845, 21845], row)
			inputP.initializeLoadPhase()
			#print "After Loading [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
			if infoList[row][col] == 0:                
				inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
			else:
				inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult);

	print "done"
	inputP.close();
	return inputP;



def realisticTest(filename, freq):

	inputP = inputBuilder("dat/" + filename + ".root")
	inputP.initializeLoadPhase()
	
	mult = (int(freq)/10)+1;

	print "Multiplier = ", mult

	# n rows
	#nrows = 128;
	nrows = 128;
	ncols = 32;
        npatterns = nrows * ncols;
        nBankSize = 200000;
        nTruePatterns = 3;

        f = open('/home/ntran/Documents/forSergo/banks/620_SLHC15_lowmidhig_sec26_ss256_cov90_dc0_maxfake0_bin_last4Unique.dat', 'r');
        line = f.readlines();        

        nBankSize = len(line);
        print "Bank Size =", nBankSize;

	infoList = [];
        data   = [None]*4;

        l0hits = [];
        l1hits = []
        l2hits = [];
        l3hits = [];
        
        pattcounter = 0;
        datalist= [];

        for pattcounter in range(0, nBankSize):
            column = line[pattcounter].split();
            dataword = [32767-int(column[0]), 32767-int(column[1]), 32767-int(column[2]), 32767-int(column[3])];
            datalist.append(dataword);
            l0hits.append(32767-int(column[0]));
            l1hits.append(32767-int(column[1]));
            l2hits.append(32767-int(column[2]));
            l3hits.append(32767-int(column[3]));

        random.shuffle(datalist);    
                   

	## ---------------------------------
	## Load mode
        pattcounter = 0;
        realtrack = [5,15,25,35];

	print "RUNNING LOAD MODE!!"
	for row in range(0, 128):
		for col in range(0, 32):
                    data = datalist[pattcounter];
                    #print row, col, data;
                    inputP.loadSinglePattern(row, col, data, mult);                    
                    pattcounter = pattcounter + 1;
                if (row%12==0): inputP.loadSinglePattern(row, random.randint(0,31), realtrack, mult); 
	## ---------------------------------
	## test hits
    
        
        #print l0hits[0:33];   
        #print l1hits[0:33];
        #print l2hits[0:33];
        #print l3hits[0:33];

        for counter in range(10):
          
            random.shuffle(l0hits);    
            random.shuffle(l1hits);    
            random.shuffle(l2hits);   
            random.shuffle(l3hits); 

            #nhl0= np.random.poisson(55);
            #nhl1= np.random.poisson(35);
            #nhl2= np.random.poisson(30);
            #nhl3= np.random.poisson(20);

            nhl0= np.random.poisson(30);
            nhl1= np.random.poisson(20);
            nhl2= np.random.poisson(20);
            nhl3= np.random.poisson(20);

            l0h=list(set(l0hits[0:nhl0]));
            l1h=list(set(l1hits[0:nhl1]));
            l2h=list(set(l2hits[0:nhl2]));
            l3h=list(set(l3hits[0:nhl3]));

            l0h.insert(0,5);
            l1h.insert(0,15);
            l2h.insert(0,25);
            l3h.insert(0,35);

            random.shuffle(l0h);
            random.shuffle(l1h);
            random.shuffle(l2h);
            random.shuffle(l3h);
            
            nHitsPerLayer = max(len(l0h), len(l1h), len(l2h),len(l3h));

            for i in range(nHitsPerLayer-len(l0h)): l0h.append(l0h[len(l0h)-1]);
            for i in range(nHitsPerLayer-len(l1h)): l1h.append(l1h[len(l1h)-1]);
            for i in range(nHitsPerLayer-len(l2h)): l2h.append(l2h[len(l2h)-1]);
            for i in range(nHitsPerLayer-len(l3h)): l3h.append(l3h[len(l3h)-1]);

            print l0h;
            print l1h;
            print l2h;
            print l3h;


            print "RUN CHECK MODE!!"
            inputP.initializeRunPhase([1, 0, 0, 0])
            inputP.checkPattern([21845, 21845, 21845, 21845], 0)
            for i in range(nHitsPerLayer): inputP.checkPattern( [l0h[i], l1h[i], l2h[i],  l3h[i]] ,0);

            for row in range(0,nrows):
                for i in range(0, 10*mult):
                    inputP.checkPattern([21845, 21845, 21845, 21845], row)
                inputP.doRowChecker(row)
                for i in range(0, 10*mult):
                    inputP.checkPattern([21845, 21845, 21845, 21845], row)	

        print "done"
	inputP.close();
	return inputP;



def dummy():
	print "hello world"
