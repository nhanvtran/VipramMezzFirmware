import random
from pVIPRAM_inputBuilderClass import *
from conditionsTester import *
def GenerateInputs(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	
	row = 0
	correctArr = []
	for c in range(0, 32):
		correctArr.append([random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)])
		inputP.loadSinglePattern(row, c, correctArr[c], 10)
	
	#Only Miss0
	inputP.initializeRunPhase([1, 0, 0, 0])	
	#All Matches
	for c in range(0, 32):
		noneWrong(correctArr[c], inputP, row)
	#All Misses
	#for c in range(0, 32):
		oneWrong(correctArr[c], inputP, row)
		twoWrong(correctArr[c], inputP, row)
		threeWrong(correctArr[c], inputP, row)
		allWrong(correctArr[c], inputP, row)
	
	#EVENT REARM
	
	#Only Miss1
        	inputP.initializeRunPhase([0, 1, 0, 0])
        #All Matches:
        	oneWrong(correctArr[c], inputP, row)
        #All Misses:
        	noneWrong(correctArr[c], inputP, row)
        	twoWrong(correctArr[c], inputP, row)
        	threeWrong(correctArr[c], inputP, row)
        	allWrong(correctArr[c], inputP, row)

	#EVENT REARM

	#Only Miss2
        	inputP.initializeRunPhase([0, 0, 1, 0])
        #All Matches:
        	twoWrong(correctArr[c], inputP, row)
        #All Misses:
        	noneWrong(correctArr[c], inputP, row)
        	oneWrong(correctArr[c], inputP, row)
        	threeWrong(correctArr[c], inputP, row)
        	allWrong(correctArr[c], inputP, row)

	#EVENT REARM
	#Only RequireLayerA
	
		inputP.initializeRunPhase([0, 0, 0, 1])
        #A Match:
        	inputP.checkPattern([correctArr[c][0], random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)], row)
        #Some Misses:
       		inputP.checkPattern([1+correctArr[c][0], random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)], row)

	#Miss0 and Miss1
        	inputP.initializeRunPhase([1, 1, 0, 0])
        #All Matches:
        	noneWrong(correctArr[c], inputP, row)
        	oneWrong(correctArr[c], inputP, row)
        #All Mismatches:
        	twoWrong(correctArr[c], inputP, row)
        	threeWrong(correctArr[c], inputP, row)
        	allWrong(correctArr[c], inputP, row)
	
	#Miss0 and Miss2
        	inputP.initializeRunPhase([1, 0, 1, 0])
        #All Matches:
        	noneWrong(correctArr[c], inputP, row)
        	twoWrong(correctArr[c], inputP, row)
        	#All Mismatches:
        	oneWrong(correctArr[c], inputP, row)
        	threeWrong(correctArr[c], inputP, row)
        	allWrong(correctArr[c], inputP, row)

	#Miss0 and Miss1 and Miss2
        	inputP.initializeRunPhase([1, 1, 1, 0])
        #All Matches:
        	noneWrong(correctArr[c], inputP, row)
        	oneWrong(correctArr[c], inputP, row)
        	twoWrong(correctArr[c], inputP, row)
        #All Mismatches:
        	threeWrong(correctArr[c], inputP, row)
        	allWrong(correctArr[c], inputP, row)

	#Miss0 and RequireLayerA
        	inputP.initializeRunPhase([1, 0, 0, 1])
        #All Matches:
        	noneWrong(correctArr[c], inputP, 8)
        #Some Mismatches:
        	for i in range(0, 2):
        	        for j in range(0, 2):
        	                for k in range(0, 2):
        	                        for m in range(0, 2):
        	                                if (i == correctArr[c][0] and j == correctArr[c][1] and k == correctArr[c][2] and m == correctArr[c][3]):
        	                                        continue
        	                                else:
        	                                        checkPattern([i, j, k, m], 8)
	
	inputP.close()
	return inputP
