from pVIPRAM_inputBuilderClass import *
import random
import sys

def GenerateInputsLoad(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	prob = int(sys.argv[2])
	mult = (int(sys.argv[3])/10)+1
	infoFile = open("NewStressInfoFile.txt", "a")
	for row in range(int(sys.argv[1]), int(sys.argv[1])+4):
		for col in range(0, 32):
			if (random.randint(1, 100) > prob):
				inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
				print "Loaded [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
				infoFile.write(str("N "))
			else:
				inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
				print "Loaded [32767, 32767, 32767, 32767] in Row: " + str(row) + ", Col: " + str(col)
				infoFile.write(str("1-N "))
		infoFile.write("\n")
	inputP.close()
	return inputP

def GenerateInputsRun(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	prob = int(sys.argv[2])
	mult = (int(sys.argv[3])/10)+1
	infoFile = open("NewStressInfoFile.txt", "r+")
	infoLines = infoFile.readlines()
	for row in range(int(sys.argv[1]), int(sys.argv[1])+16):
		for col in range(0, 32, 4):
			if (infoLines[row].split(" ")[col] == "N"):
				inputP.initializeLoadPhase()
				inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
				print "Loading and Checking [32766, 32766, 32766, 32766] at Row: " + str(row) + ", Col: " + str(col)
				for iteration in range(0, 1):
					inputP.initializeRunPhase([1, 0, 0, 0])
					inputP.checkPattern([21845, 21845, 21845, 21845], row)
					inputP.checkPattern([32766, 32766, 32766, 32766], row)
					for i in range(0, 10):
						inputP.checkPattern([21845, 21845, 21845, 21845], row)
					inputP.doRowChecker(row)
					for i in range(0, 10):
						inputP.checkPattern([21845, 21845, 21845, 21845], row)
				inputP.initializeLoadPhase()
				print "After Loading [0, 0, 0, 0] in Row: " + str(row) + ", Col: " + str(col)
				inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
			else:
				inputP.initializeLoadPhase()
				inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
				inputP.initializeRunPhase([1, 0, 0, 0])
				print "Loading and Checking [32766, 32766, 32766, 0] at Row: " + str(row) + ", Col: " + str(col)
				for iteration in range(0, 1):
					inputP.checkPattern([21845, 21845, 21845, 21845], row)
					inputP.checkPattern([32766, 32766, 32766, 32766], row)
					for j in range(0, 10):
						inputP.checkPattern([21845, 21845, 21845, 21845], row)
					inputP.doRowChecker(row)
					for i in range(0, 10):
						inputP.checkPattern([21845, 21845, 21845, 21845], row)
				inputP.initializeLoadPhase()
				print "After Loading [32767, 32767, 32767, 32767] in Row: " + str(row) + ", Col: " + str(col)
				inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)

	inputP.close()
	return inputP

def GenerateInputsOneLocRun(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	mult = int(sys.argv[3])/10
	row = 48
	col = 30
	inputP.loadSinglePattern(row, col, [32766, 32766, 32766, 32766], mult)
	for iteration in range(0, 1):
		inputP.initializeRunPhase([1, 0, 0, 0])
		inputP.checkPattern([21845, 21845, 21845, 21845], row)
		inputP.checkPattern([32766, 32766, 32766, 32766], row)
		for i in range(0, 10):
			inputP.checkPattern([21845, 21845, 21845, 21845], row)
		inputP.doRowChecker(row)
		for j in range(0, 10):
			inputP.checkPattern([21845, 21845, 21845, 21845], row)
	info = (open("NewStressInfoFile.txt", "r+").readlines())
	if (info[row].split(" ")[col] == "N"):
		inputP.loadSinglePattern(row, col, [0, 0, 0, 0], mult)
	else:
		inputP.loadSinglePattern(row, col, [32767, 32767, 32767, 32767], mult)
	inputP.close()
	return inputP
