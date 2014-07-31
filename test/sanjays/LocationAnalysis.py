import numpy as np
import matplotlib.pyplot as pyplot
import math

rowRef = 0
colRef = 0

class Unit:
	def __init__(self, row, col):
		self.r = row
		self.c = col
	def __lt__(self, otherUnit):
		return math.sqrt(((float(self.r)-float(rowRef))**2)+((float(self.c)-float(colRef))**2)) < math.sqrt(((float(otherUnit.r)-float(rowRef))**2)+((float(otherUnit.c)-float(colRef))**2))

def locationAnalysis(logfilesN):
	logs = []
	for l in range(0, len(logfilesN)):
		logs.append((open(logfilesN[l], "r+")).readlines())
	rows = np.zeros(128)
	cols = np.zeros(32)
	for l2 in range(0, len(logs)):
		for l3 in range(0, len(logs[l2])):
			if ("no match" in logs[l2][l3]):
				rows[int(logs[l2][l3].split(" ")[14])] += 1
				cols[int(logs[l2][l3].split("[")[1].split("]")[0])] += 1
	pyplot.subplot(211)
	pyplot.title("Number of mismatches vs. Row number/Column Number")
	pyplot.bar(range(0, 128), rows )#, 'ro')
	pyplot.xlabel("Row number")
	pyplot.ylabel("Number of mismatches")
	pyplot.subplot(212)
	pyplot.xlabel("Column number")
	pyplot.ylabel("Number of mismatches")
	pyplot.bar(range(0, 32), cols)#, 'bo')
	pyplot.show()

def distanceMatch(dataFile, logfile):
	nandSameList = []
	data = (open(dataFile, "r+")).readlines()
	for line in data:
		for col in line.split(" "):
			if (col == "1-N"):
				nandSameList.append(Unit(data.index(line), line.split(" ").index(col)))
	logLines = (open(logfile, "r+")).readlines()
	dist = []
	count = 0
	grid = []
	for i in range(0, 128):
		grid.append(np.zeros(32))
	for l in logLines:
		if ("checkData" in l):
			rowRef = int(l.split(" ")[14])
			colRef = int(l.split("[")[1].split("]")[0])
			grid[rowRef][colRef] += 1
			#nandSameList = sorted(nandSameList)
			#dist.append(math.sqrt(((float(nandSameList[0].r)-float(rowRef))**2)+((float(nandSameList[0].c)-float(colRef))**2)))
			count += 1
			if (count % 1000 == 0):
				print count
	count = 0
	for row in range(0, 128):
		for column in range(0, 32):
			if (grid[row][column] < 50):
				rowRef = row
				colRef = column
				nandSameList = sorted(nandSameList)
				while (grid[row][column] < 50):
					dist.append(math.sqrt(((float(nandSameList[0].r)-float(rowRef))**2)+((float(nandSameList[0].c)-float(colRef))**2)))
					count += 1
					grid[row][column] += 1
			if (count % 1000 == 0):
				print str(count) + " B"
	#print dist
	pyplot.hist(dist, bins=10)
	pyplot.xlabel("Euclidean Distance (cell units)")
	pyplot.ylabel("Frequency")
	pyplot.title("Histogram of Distance from Mismatch Location to Nearest NAND Match Location")
	pyplot.show()
