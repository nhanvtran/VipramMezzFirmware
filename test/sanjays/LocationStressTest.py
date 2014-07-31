from pVIPRAM_inputBuilderClass import *
import sys
import random

def GenerateInputsLoad(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	N = int(sys.argv[2])
	mult = (int(sys.argv[3])/10)+1
	#offset = 0
	nInfoFile = open("LocationStressInfoFile.txt", "a")
	#if N != 0:
		#offset = int(round(100.0/float(N), 0))
	for row in range(int(sys.argv[1]), int(sys.argv[1])+4):
		for col in range(0, 32):
			if (random.randint(1, 100) <= N):
				inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
				print "Loaded [32767, 32767, 32767, 32767] in Row: "  + str(row) + ", Col: " + str(col)
				nInfoFile.write("1-N ")
			else:
				inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
				print "Loaded [0, 0, 0, 0] in Row: "  + str(row) + ", Col: " + str(col)
				nInfoFile.write("N ")
		nInfoFile.write("\n")
	nInfoFile.close()
	inputP.close()
	return inputP

def GenerateInputsRun(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	N = int(sys.argv[2])
	mult = (int(sys.argv[3])/10)+1
	#offset = 0
	#if N != 0:
		#offset = int(round(100.0/float(N), 0))
	row = int(sys.argv[1])
	nInfoFile = open("LocationStressInfoFile.txt", "r+")
	nInfoLines = nInfoFile.readlines()
	for col in range(int(sys.argv[4]), int(sys.argv[4])+16):
		inputP.initializeLoadPhase()
		inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
		for iteration in range(0, 50):
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([21845, 21845, 21845, 21845], row)
			inputP.checkPattern([32766, 32766, 32766, 32766], row)
			for i in range(0, 10):
				inputP.checkPattern([21845, 21845, 21845, 21845], row)
			inputP.doRowChecker(row)
			for j in range(0, 10):
				inputP.checkPattern([21845, 21845, 21845, 21845], row)
		inputP.initializeLoadPhase()
		if (nInfoLines[row].split(" ")[col] == "1-N"):
			inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
		else:
			inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
	inputP.close()
	return inputP
