from pVIPRAM_inputBuilderClass import *
import sys
import random
import numpy as np


#NEW NAND SETTING
nandNew = [12, 11, 10, 9]

nandNewA = [4, 10, 11, 13]
nandNewB = [3, 4, 8, 13]
nandNewC = [4, 9, 12, 13]
nandNewD = [4, 12, 13, 14]
nandNewE = [14-10, 14-11, 14-12, 14-13]
nandNewF = [14-10, 14-11, 14-12, 14-13]

nandNews = [nandNewA, nandNewB, nandNewC, nandNewD, nandNewE, nandNewF, nandNew]

originalNand = [0, 1, 2, 3]

def reshuffleBits(num, nandLocs1, nandLocs2):
    binaryNum = bin(num)[2:]
    while (len(binaryNum) < 15):
	binaryNum = "0" + binaryNum
    for i in range(0, len(nandLocs1)):
	print binaryNum
	temp = binaryNum[nandLocs1[i]]
	tempList = list(binaryNum)
	tempList[nandLocs1[i]] = binaryNum[nandLocs2[i]]
	tempList[nandLocs2[i]] = temp
	binaryNum = ""
	for j in range(len(tempList)):
		binaryNum += tempList[j]
	
    return int(binaryNum, 2)

#Loading
def GenerateInputsLoad(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	interval = 256
	size = 10000
	rowCount = int(sys.argv[2])/32
	colCount = 0
	inputFile = open(sys.argv[1], "r+")
	inputLines = inputFile.readlines()
	#lineNums = np.zeros(size)
	#inputsOut1 = open("CERN Inputs1.txt", "r")
	#inputsOutLines = inputsOut1.readlines()
	#for iol in inputsOutLines:
		#for iol2 in range(0, len(iol1.split(" ")) - 1):
			#lineNums[int(iol1.split(" ")[iol2])] = 1
	#inputsOut2 = open("CERN Inputs1.txt", "a")
	#inputsOut3 = open("CERN InputInfo.txt", "a")
	nandFile = open(sys.argv[3], "r+")
	nandLines = nandFile.readlines()
	for layer in range(0, 4):
		nandNews[layer] = [int(nandLines[layer].split(" ")[0]), int(nandLines[layer].split(" ")[1]), int(nandLines[layer].split(" ")[2]), int(nandLines[layer].split(" ")[3])]
	for il in range(int(sys.argv[2]), int(sys.argv[2])+interval):
		#randLine = random.randint(1, size)
		#while (lineNums[randLine] == 1):
			#randLine = random.randint(1, size)
		#inputsOut2.write(str(randLine) + " ")
		#inputsOut3.write(str(rowCount) + " " + str(colCount) + " ")
		strConstituents = inputLines[il].split(" - ")
		nums = []
		for sc in range(0, len(strConstituents)-1):
			nums.append(int(strConstituents[sc]))
			#nums[sc] = reshuffleBits(nums[sc], originalNand, nandNew)
			nums[sc] = reshuffleBits(nums[sc], originalNand, nandNews[sc])
			#inputsOut3.write(str(nums[sc]) + " ")
		#inputsOut3.write("\n")
		inputP.initializeLoadPhase()
		#100 MHz:
		#inputP.loadSinglePattern(rowCount, colCount, [nums[0], nums[1], nums[2], nums[3]], 12)
		#90 MHz:
		inputP.loadSinglePattern(rowCount, colCount, [nums[0], nums[1], nums[2], nums[3]], 10)
		#50 MHz:
		#inputP.loadSinglePattern(rowCount, colCount, [nums[0], nums[1], nums[2], nums[3]], 6)
		#77 MHz:
		#inputP.loadSinglePattern(rowCount, colCount, [nums[0], nums[1], nums[2], nums[3]], 8)
		print "Loaded " + str([nums[0], nums[1], nums[2], nums[3]]) + " in Row: " + str(rowCount) + ", Col: " + str(colCount)
		colCount += 1
		if (colCount == 32):
			colCount = 0
			rowCount += 1
	#inputsOut2.write("\n")
	#inputsOut1.close()
	#inputsOut2.close()
	#inputsOut3.close()
	inputP.close()
	return inputP

#Checking Patterns
def GenerateInputsRun(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	patternsFile = open(sys.argv[1], "r+")
	patterns = patternsFile.readlines()
	limit = 1024
	#exhausted = np.zeros(limit+1)
	outputFile = open("Expected CERN Outputs1.txt", "w+")
	nandFile = open(sys.argv[3], "r+")
	nandLines = nandFile.readlines()
	for layer in range(0, 4):
		nandNews[layer] = [int(nandLines[layer].split(" ")[0]), int(nandLines[layer].split(" ")[1]), int(nandLines[layer].split(" ")[2]), int(nandLines[layer].split(" ")[3])]
	#inputP.initializeRunPhase([1, 0, 0, 0])
	for index in range(int(sys.argv[2]), int(sys.argv[2])+limit):
		inputP.initializeRunPhase([1, 0, 0, 0])
		row = (index-1)/32
		print row
		col = (index-1) % 32
		strValues = patterns[index].split(" - ")
		values = [int(strValues[0]), int(strValues[1]), int(strValues[2]), int(strValues[3])]
		for ii in range(0, len(values)):
			#values[ii] = reshuffleBits(values[ii], nandNew, originalNand)
			values[ii] = reshuffleBits(values[ii], nandNews[ii], originalNand)
		inputP.checkPattern([32767, 32767, 32767, 32767], row)
		inputP.checkPattern(values, row)
		for j1 in range(0, 10):
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
		inputP.doRowChecker(row)
		for j2 in range(0, 10):
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
		outputFile.write(str(row) + " " + strValues[0] + " " + strValues[1] + " " + strValues[2] + " " + strValues[3] + "\n")
		#exhausted[index-int(sys.argv[2])] = 1

	inputP.close()
	return inputP
