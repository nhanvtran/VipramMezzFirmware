import random
import numpy as np
import sys
from pVIPRAM_inputBuilderClass import *

def arrayNotProcessed(array):
    for a in array:
        if (int(a) == 0):
	    return True
    return False

def GenerateInputs1(filename):
    inputP = inputBuilder("root/" + filename + ".root")
    rows = np.zeros(4)
    startRow = int(sys.argv[1])
    #while (arrayProcessed(rows)):
        #index = 0
	#for i in range(0, 128):
            #if rows[i] == 0:
                #index = rows[i]
		#break
    for index in range(0, 4):
        cols = np.zeros(32)
	while (arrayNotProcessed(cols)):
	    indexC = 0
	    for j in range(0, 32):
		if int(cols[j]) == 0:
		    indexC = j
		    break
	    inputP.initializeLoadPhase()
	    inputArr = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
	    inputP.loadSinglePattern(index+startRow, indexC, inputArr, 12)
	    inputP.initializeRunPhase([1, 0, 0, 0])
	    for k in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index+startRow)
	    inputP.checkPattern(inputArr, index+startRow)
	    for k1 in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index+startRow)
	    inputP.doRowChecker(index+startRow)
	    for k2 in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index+startRow)
	    cols[indexC] = 1
	    print "Finished Column: " + str(indexC) + " in Row: " + str(index+startRow)
	#rows[index] = 1
    inputP.close()
    return inputP

def GenerateInputs(filename):
    inputP = inputBuilder("root/" + filename + ".root")
    for c in range(int(sys.argv[1]), int(sys.argv[1])+1):
	rows = np.zeros(128)
    	while (arrayNotProcessed(rows)):
	    index = 0
	    for i in range(0, 128):
		if (int(rows[i]) == 0):
		    index = i
		    break
	    print "here"
	    inputP.initializeLoadPhase()
	    inputArr = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
	    inputP.loadSinglePattern(index, c, inputArr, 12)
	    inputP.initializeRunPhase([1, 0, 0, 0])
	    for k in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index)
	    inputP.checkPattern(inputArr, index)
	    for k1 in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index)
	    inputP.doRowChecker(index)
	    for k2 in range(0, 10):
		inputP.checkPattern([32767, 32767, 32767, 32767], index)
	    rows[index] = 1
	    print "Finished Row: " + str(index) + " in Column: " + str(c)
	#rows[index] = 1
    inputP.close()
    return inputP

