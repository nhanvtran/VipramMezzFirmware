import os
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib.patches import *

def inspectMismatches(logfile):
    logFile = open(logfile, "r+")
    logLines = logFile.readlines()
    rowCounts = np.zeros(128)
    colCounts = np.zeros(32)
    for i in logLines:
        spacedElements = i.split(" ")
        rowNum = int(spacedElements[14])
        colNum = int(i.split("[")[1].split("]")[0])
        rowCounts[rowNum] += 1
	colCounts[colNum] += 1
    pyplot.subplot(211)
    pyplot.plot(range(0, 128), rowCounts, 'ro')
    pyplot.subplot(212)
    pyplot.plot(range(0, 32), colCounts, 'bo')
    pyplot.show()

def gridMismatches(logfile):
    logFile = open(logfile, "r+")
    lines = logFile.readlines()
    rowCoords = []
    colCoords = []
    for l in lines:
        rowCoords.append(int(l.split(" ")[14]))
	colCoords.append(int((l.split("[")[1]).split("]")[0]))
    pyplot.subplot(211)
    pyplot.xlabel("Row")
    pyplot.ylabel("Column")
    pyplot.title("Mismatches: Column vs. Row")
    pyplot.plot(rowCoords, colCoords, 'ro')
    
    pyplot.show()

def makeDataHistogram(log, logMismatches):
    logfile1 = open(log, "r+")
    logfile2 = open(logMismatches, "r+")
    logLines1 = logfile1.readlines()
    logLines2 = logfile2.readlines()
    data = []
    for l1 in logLines2:
	row = int(l1.split(" ")[14])
	for c in ((l1.split("[")[1]).split("]")[0]).split(", "):
	    col = int(c)
	    for l2 in logLines1:
	    #if ("Loaded Data" in l2) and (("Row: " + str(row)) in l2) and (("Col: " + str(col)) in l2):
	    #data.append(int(l2.split(" ")[2]))
	    #break
	        if ("Loaded" in l2) and (("Row: " + str(row)) in l2) and (("Col: " + str(col)) in l2):
		    for dataPiece in ((l2.split(" [")[1]).split("]")[0]).split(", "):
		    	data.append(int(dataPiece))
			break
    print len(data)
    figure = pyplot.figure()
    axes = figure.add_subplot(111)
    axes.set_xlabel("Data Value")
    axes.set_ylabel("Frequency")
    axes.set_title("Mismatches: Histogram of Data")
    axes.hist(data, 100, normed=1, facecolor = 'green', alpha = 0.75)
    pyplot.show()

def firstFourBitsTest(logfile, logfileRun, logfileRunMismatches):
    lf = open(logfile, "r+")
    #os.system("cat " + logfileRun + " | grep Loaded > New" + logfileRun)
    lfr = open(logfileRun, "r+")
    lfrm = open(logfileRunMismatches, "r+")
    lfLines = lf.readlines()
    lfrLines = lfr.readlines()
    lfrmLines = lfrm.readlines()
    counts = []
    for l in lfrmLines:
	row = int(l.split(" ")[14])
	col = int((l.split("[")[1]).split("]")[0])
	count = 0
	#print len(lfrLines)
	for l2 in range(0, len(lfrLines)):
	    print lfrLines[l2]
	    if ("Testing" in lfrLines[l2]) and (("Row:" + str(row)) in lfrLines[l2]) and (("Column: " + str(col)) in lfrLines[l2]):
		print "one"
		binStr = bin(int(lfrLines[l2+1].split(" ")[2]))[2:]
		fourBits = binStr[0:4]
		for l3 in range(0, l2):
		    if ("Later Loaded" in lfrLines[l3]):
			print "two"
		    	binComp = bin(int(lfrLines[l3].split(" ")[3]))[2:]
		    	if (fourBits == binComp[0:4]):
				count += 1
		flag = 0
	    	for l4 in range(0, len(lfLines)):
		    if ("Loaded Data" in lfLines[l4]) and (("Row: " + str(row)) in lfLines[l4]) and (("Col: " + str(col)) in lfLines[l4]):
			print "three"
			flag += 1
		    elif (flag == 4) and ("Loaded Data" in lfLines[l4]):
			print "4"
			binComp2 = bin(int(lfLines[l4].split(" ")[2]))[2:]
			if (fourBits == binComp2[0:4]):
			    count += 1
		break
	counts.append(count)
    print counts
    pyplot.bar(range(0, len(counts)), counts)
    pyplot.xlabel("Mismatches")
    pyplot.ylabel("Number of CAM cells with Same First 4 Bits At Time of Mismatch")
    pyplot.title("First Four Bits Test at 100 MHz")
    print len(counts)
    pyplot.show()

def mismatchesAcrossRows(logfileRun):
    lfr = open(logfileRun, "r+")
    lfrLines = lfr.readlines()
    counts = []
    for i in range(0, len(lfrLines)):
	if (("There are" in lfrLines[i]) and ("mismatches" in lfrLines[i])):
	    counts.append(int(lfrLines[i].split(" ")[2]))
    pyplot.bar(range(0, len(counts)), counts)
    pyplot.xlabel("Starting Row of Execution")
    pyplot.ylabel("Number of Mismatches")
    pyplot.title("Mismatches vs. Starting Row")
    pyplot.show()

def mismatchesHeatMap(logfiles):
    rowMax = 128
    colMax = 32
    rows = []
    for r in range(0, rowMax):
        rows.append(np.zeros(colMax))
    grid = np.array(rows)
    totalMismatches = 0
    for l in logfiles:
	lFile = open(l, "r+")
	lines = lFile.readlines()
	for line in lines:
	    if ("checkData" in line):
		row = int(line.split(" ")[14])
		col = int(line.split("[")[1].split("]")[0])
		grid[row][col] += 1
		totalMismatches += 1
    figure = pyplot.figure()
    axes = figure.add_subplot(111)
    #colors = ['green', 'turquoise', 'darkblue', 'darkviolet', 'crimson']
    colors = ['green', 'lightpink', 'deeppink', 'crimson', 'maroon']
    threshold = [10, 20, 30, 40]
    print totalMismatches
    for i in range(0, rowMax):
	for j in range(0, colMax):
	    if (grid[i][j] >= threshold[3]):
	        axes.fill_between(np.arange(i, i+1, 0.1), j, j+1, facecolor=colors[4])
	    elif (grid[i][j] >= threshold[2]):
		axes.fill_between(np.arange(i, i+1, 0.1), j, j+1, facecolor=colors[3])
	    elif (grid[i][j] >= threshold[1]):
		axes.fill_between(np.arange(i, i+1, 0.1), j, j+1, facecolor=colors[2])
	    elif (grid[i][j] >= threshold[0]):
		axes.fill_between(np.arange(i, i+1, 0.1), j, j+1, facecolor=colors[1])
	    else:
		axes.fill_between(np.arange(i, i+1, 0.1), j, j+1, facecolor=colors[0])
    pyplot.xticks(np.arange(0, 128, 1))
    pyplot.yticks(np.arange(0, 32, 1))
    pyplot.xlim(0, 128)
    pyplot.ylim(0, 32)
    axes.grid()
    pyplot.legend()
    labels = []
    labels.append("mismatches < " + str(threshold[0]))
    for t in range(1, len(threshold)):
	labels.append(str(threshold[t-1]) + " <= mismatches < " + str(threshold[t]))
    labels.append("mismatches > " + str(threshold[3]))
    patchesArr = []
    for p in range(0, 5):
	patchesArr.append(Patch(color=colors[p]))
    pyplot.legend(patchesArr, labels, loc='upper right')
    #pyplot.legend((colors[0] + ": mismatches < " + str(threshold[0]), colors[1] + ": " + str(threshold[0]) + " <= mismatches < " + str(threshold[1]), colors[2] + ": " + str(threshold[1]) + " <= mismatches < " + str(threshold[2]), colors[3] + ": " + str(threshold[2]) + " <= mismatches < " + str(threshold[3]), colors[4] + " mismatches > " + str(threshold[3])), loc='upper left')
    pyplot.show()

def barRealDataMismatches(logfiles1Unopt, logfiles1Opt, logfiles2Unopt, logfiles2Opt):
    logs1U = []
    logs1O = []
    logs2U = []
    logs2O = []
    for l1u in logfiles1Unopt:
	logs1U.append((open(l1u[:len(l1u)-4] + "Run.log", "r+")).readlines())
    for l1o in logfiles1Opt:
	logs1O.append((open(l1o[:len(l1o)-4] + "Run.log", "r+")).readlines())
    for l2u in logfiles2Unopt:
	logs2U.append((open(l2u[:len(l2u)-4] + "Run.log", "r+")).readlines())
    for l2o in logfiles2Opt:
	logs2O.append((open(l2o[:len(l2o)-4] + "Run.log", "r+")).readlines())
    mismatches1u = 0
    mismatches2u = 0
    mismatches1o = 0
    mismatches2o = 0
    for i1 in logs1U:
	for ii1 in i1:
	    if ("checkData" in ii1):
	        mismatches1u += 1
    for i2 in logs1O:
	for ii2 in i2:
	    if ("checkData" in ii2):
	        mismatches1o += 1
    for i3 in logs2U:
	for ii3 in i3:
	    if ("checkData" in ii3):
	        mismatches2u += 1
    for i4 in logs2O:
	for ii4 in i4:
	    if ("checkData" in ii4):
		mismatches2o += 1
    pyplot.bar(1, mismatches1u, color='maroon')
    pyplot.bar(2, mismatches1o, color='orange')
    pyplot.bar(3, mismatches2u, color='maroon')
    pyplot.bar(4, mismatches2o, color='orange')
    pyplot.xticks([0, 1, 2, 3, 4, 5], ['', '77', '77', '90', '90', ''])
    pyplot.legend([Patch(color='maroon'), Patch(color='orange')], ['Unoptimized', 'Optimized'], loc='upper right')
    pyplot.show()
