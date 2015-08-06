import random
import sys
sys.path.insert(0, '../interface')
from pVIPRAM_inputBuilderClass import *

#########################################################
#########################################################
#########################################################
#########################################################

### 32767 = 111111111111111
### 32766 = 111111111111110
### 21845 = 101010101010101
### 10922 = 010101010101010

def stressTest_split(filename, N, freq, odir, loadMode):

	inputP = inputBuilder(odir + "/" + filename + ".root")
	if loadMode: inputP.initializeLoadPhase()
	
	# N value
	#prob = int(sys.argv[2]);
	prob = int(N)
	# frequency
	# mult = (int(sys.argv[3])/10)+1
	mult = (int(freq)/10)+1;

	print "N% = ", prob, ", Multiplier = ", mult

	# n rows
	#nrows = 128;
	nrows = 12;
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
				if loadMode: inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
				#print "Loaded [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
				#infoFile.write(str("N "))
				tmpInfoList.append(0);
			else:
				if loadMode: inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
				#print "Loaded [32767, 32767, 32767, 32767] in Row: " + str(row) + ", Col: " + str(col)
				tmpInfoList.append(1);
		infoList.append( tmpInfoList );

	if not loadMode:
		print "RUN LOAD+CHECK MODE!!"
		##inputP.initializeRunPhase([1, 0, 0, 0],51,[0,0,0,0]);
		
		if prob < 100: inputP.initializeRunPhase([1, 0, 0, 0],51,[16384,16384,16384,16384]);
		else: inputP.initializeRunPhase([1, 0, 0, 0],51,[0,0,0,0]);


		#range original is 10700 changed to 10921
                for i in range(10):
			if i % 1000 == 0: print i;
			for j in range(1): 
				inputP.checkPattern([32767, 32767, 32767, 32767], 51);
		#		#inputP.readOutMode();
		#	
			if prob < 100: inputP.initializeRunPhase([1, 0, 0, 0],51,[16384,16384,16384,16384]);
			else: inputP.initializeRunPhase([1, 0, 0, 0],51,[0,0,0,0]);
		#       #inputP.readOutMode();

		#inputP.initializeRunPhase([1, 0, 0, 0],51,[0,0,0,0]);
		#inputP.initializeRunPhase([1, 0, 0, 0],51,[0,0,0,0]);
                
		inputP.checkPattern([32767, 32767, 32767, 32767], 51);

		##inputP.checkPattern([0, 0, 0, 0], 51);
                
		#inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);
                #inputP.checkPattern([0, 0, 0, 0], 10);

		if prob < 100: inputP.initializeRunPhase_Mod([1, 0, 0, 0],51,[16384,16384,16384,16384]);
		else: inputP.initializeRunPhase_Mod([1, 0, 0, 0],51,[0,0,0,0]);

                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],51,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);
                #inputP.initializeRunPhase_Mod([1, 0, 0, 0],10,[0,0,0,0]);

		inputP.readOutMode_M(freq);





		# ## Load + Check
		# for row in range(0,nrows):
		# 	print "load + check in row ", row
		# 	for col in range(0,ncols,4):
		# 		inputP.initializeLoadPhase()
		# 		inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
		# 		#print "Loading and Checking [32766, 32766, 32766, 32766] at Row: " + str(row) + ", Col: " + str(col)
		# 		for iteration in range(0, 1):
		# 			inputP.initializeRunPhase([1, 0, 0, 0])
		# 			# inputP.checkPattern([21845, 21845, 21845, 21845], row)
		# 			inputP.checkPattern([32766, 32766, 32766, 32766], row)
		# 			for i in range(0, 10*mult):
		# 				inputP.checkPattern([21845, 21845, 21845, 21845], row)
		# 			inputP.doRowChecker(row,col)
		# 			for i in range(0, 10):
		# 				inputP.checkPattern([21845, 21845, 21845, 21845], row)
		# 		inputP.initializeLoadPhase()
		# 		#print "After Loading [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
		# 		if infoList[row][col] == 0:                
		# 			inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
		# 		else:
		# 			inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult);

	print "done"
	inputP.close();
	return inputP;


