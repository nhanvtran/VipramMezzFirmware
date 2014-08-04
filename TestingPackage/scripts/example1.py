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
	nrows = 16;
	ncols = 32;

	#infoFile = open("NewStressInfoFile.txt", "a")
	infoList = [];
	## ---------------------------------
	## Load mode
	print "RUNNING LOAD MODE!!"
	for row in range(nrows):
		tmpInfoList = [];
		for col in range(0, ncols):
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
				for i in range(0, 10):
					inputP.checkPattern([21845, 21845, 21845, 21845], row)
				inputP.doRowChecker(row,col)
				for i in range(0, 10):
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

def dummy():
	print "hello world"
