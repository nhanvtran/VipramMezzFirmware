import random
import sys
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
	
	# frequency
	# mult = (int(sys.argv[3])/10)+1
	mult = (int(freq)/10)+1;

	print "Multiplier = ", mult

	# n rows
	#nrows = 128;
	nrows = 6;
	ncols = 32;
        npatterns = nrows * ncols;
        nBankSize = 100000;
        nTruePatterns = 5;

        f = open('../../../patterns_612_SLHC6_MUBANK_lowmidhig_sec16_ss32_cov40.dat', 'r');
        line = f.readlines();        

	#infoFile = open("NewStressInfoFile.txt", "a")
	infoList = [];
        data   = [None]*4;

        l0hits = [];
        l1hits = []
        l2hits = [];
        l3hits = [];
             
	## ---------------------------------
	## Load mode
	print "RUNNING LOAD MODE!!"
	for row in range(nrows):
		for col in range(0, ncols):
                    x = random.randint(1, nBankSize);
                    columns = line[x].split()
                    data = [int(columns[0]), int(columns[2]), int(columns[4]), int(columns[6])];
                    inputP.loadSinglePattern(row, col, data, mult)

                    if ((row ==0) and (col<nTruePatterns)):
                        l0hits.append(int(columns[0]));
                        l1hits.append(int(columns[2]));
                        l2hits.append(int(columns[4]));
                        l3hits.append(int(columns[6]));
                    
 
	## ---------------------------------
	## test hits
    
        
        nHitsPerLayer = 33;
	for hit in range(nHitsPerLayer-nTruePatterns):
            x = random.randint(1, nBankSize);
            columns = line[x].split()
            l0hits.append(int(columns[0]));
            x = random.randint(1, nBankSize);
            columns = line[x].split()
            l1hits.append(int(columns[2]));
            x = random.randint(1, nBankSize);
            columns = line[x].split()
            l2hits.append(int(columns[4]));
            x = random.randint(1, nBankSize);
            columns = line[x].split()
            l3hits.append(int(columns[6]));

        print l0hits;   
        print l1hits;
        print l2hits;
        print l3hits;


	print "RUN CHECK MODE!!"
        inputP.initializeRunPhase([1, 0, 0, 0])
        for i in range(nHitsPerLayer): inputP.checkPattern( [l0hits[i], l1hits[i], l2hits[i],  l3hits[i]] ,0);
        inputP.doRowChecker(0)
	
        print "done"
	inputP.close();
	return inputP;



def dummy():
	print "hello world"
