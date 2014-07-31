from pVIPRAM_inputBuilderClass import *
import sys
import random

def invertFirstFour(num):
	if (num >= 2**14):
		num -= 2**14
	else:
		num += 2**14
	if (num >= 2**13):
		num -= 2**13
	else:
		num += 2**13
	if (num >= 2**12):
		num -= 2**12
	else:
		num += 2**12
	if (num >= 2**11):
		num -= 2**11
	else:
		num += 2**11
	return num

def GenerateInputs(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	for row in range(int(sys.argv[1]), int(sys.argv[1])+4):
		for iter in range(0, 6):
			standardData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, (5*iter), standardData, 12)
			print "-Loaded Data: " + str(standardData[0]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerA"
			print "-Loaded Data: " + str(standardData[1]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerB"
			print "-Loaded Data: " + str(standardData[2]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerC"
			print "-Loaded Data: " + str(standardData[3]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerD"
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.checkPattern(standardData, row)
			for i1 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.doRowChecker(row)
			for i2 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			newData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			print "-Later Loaded Data: " + str(newData[0]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerA"
			print "-Later Loaded Data: " + str(newData[1]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerB"
			print "-Later Loaded Data: " + str(newData[2]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerC"
			print "-Later Loaded Data: " + str(newData[3]) + " in Row: " + str(row) + " and Col: " + str(5*iter) + " in LayerD"

			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, (5*iter)+1, [invertFirstFour(standardData[0]), standardData[1], standardData[2], standardData[3]], 12)
			print "-Loaded Data: " + str(invertFirstFour(standardData[0])) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerA"
			print "-Loaded Data: " + str(standardData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerB"
			print "-Loaded Data: " + str(standardData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerC"
			print "-Loaded Data: " + str(standardData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerD"
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.checkPattern([invertFirstFour(standardData[0]), standardData[1], standardData[2], standardData[3]], row)
			for i1 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.doRowChecker(row)
			for i2 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			newData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			print "-Later Loaded Data: " + str(newData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerA"
			print "-Later Loaded Data: " + str(newData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerB"
			print "-Later Loaded Data: " + str(newData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerC"
			print "-Later Loaded Data: " + str(newData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+1) + " in LayerD"

			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, (5*iter)+2, [standardData[0], invertFirstFour(standardData[1]), standardData[2], standardData[3]], 12)
			print "-Loaded Data: " + str(standardData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerA"
			print "-Loaded Data: " + str(invertFirstFour(standardData[1])) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerB"
			print "-Loaded Data: " + str(standardData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerC"
			print "-Loaded Data: " + str(standardData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerD"
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.checkPattern([standardData[0], invertFirstFour(standardData[1]), standardData[2], standardData[3]], row)
			for i1 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.doRowChecker(row)
			for i2 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			newData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			print "-Later Loaded Data: " + str(newData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerA"
			print "-Later Loaded Data: " + str(newData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerB"
			print "-Later Loaded Data: " + str(newData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerC"
			print "-Later Loaded Data: " + str(newData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+2) + " in LayerD"

			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, (5*iter)+3, [standardData[0], standardData[1], invertFirstFour(standardData[2]), standardData[3]], 12)
			print "-Loaded Data: " + str(standardData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerA"
			print "-Loaded Data: " + str(standardData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerB"
			print "-Loaded Data: " + str(invertFirstFour(standardData[2])) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerC"
			print "-Loaded Data: " + str(standardData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerD"
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.checkPattern([standardData[0], standardData[1], invertFirstFour(standardData[2]), standardData[3]], row)
			for i1 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.doRowChecker(row)
			for i2 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			newData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			print "-Later Loaded Data: " + str(newData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerA"
			print "-Later Loaded Data: " + str(newData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerB"
			print "-Later Loaded Data: " + str(newData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerC"
			print "-Later Loaded Data: " + str(newData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+3) + " in LayerD"

			inputP.initializeLoadPhase()
			inputP.loadSinglePattern(row, (5*iter)+4, [standardData[0], standardData[1], standardData[2], invertFirstFour(standardData[3])], 12)
			print "-Loaded Data: " + str(standardData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerA"
			print "-Loaded Data: " + str(standardData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerB"
			print "-Loaded Data: " + str(standardData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerC"
			print "-Loaded Data: " + str(invertFirstFour(standardData[3])) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerD"
			inputP.initializeRunPhase([1, 0, 0, 0])
			inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.checkPattern([standardData[0], standardData[1], standardData[2], invertFirstFour(standardData[3])], row)
			for i1 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			inputP.doRowChecker(row)
			for i2 in range(0, 10):
				inputP.checkPattern([32767, 32767, 32767, 32767], row)
			newData = [random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766), random.randint(0, 32766)]
			print "-Later Loaded Data: " + str(newData[0]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerA"
			print "-Later Loaded Data: " + str(newData[1]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerB"
			print "-Later Loaded Data: " + str(newData[2]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerC"
			print "-Later Loaded Data: " + str(newData[3]) + " in Row: " + str(row) + " and Col: " + str((5*iter)+4) + " in LayerD"

	inputP.close()
	return inputP

