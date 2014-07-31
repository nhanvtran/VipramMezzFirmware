import numpy as np
import matplotlib.pyplot as pyplot
#import matplotlib.pylab as pylab
class Bin:
	def __init__(self, num):
		self.value = num
		self.count = 1
	def __lt__(self, bin2):
		return self.count < bin2.count

def sortBins(filename):
	file = open(filename, "r+")
	allBins = []
	content = file.readlines()
	for c in range(1, len(content)):
		for c2 in range(0, len(content[c].split(" - "))-1):
			#print content[c].split(" - ")
			flag = -1
			for a in range(0, len(allBins)):
				if (allBins[a].value == int(content[c].split(" - ")[c2])):
					flag = a
					break
			if (-1 < flag):
				allBins[flag].count += 1
			else:
				allBins.append(Bin(int(content[c].split(" - ")[c2])))
	allBins.sort()
	fileOut = open("sortBinsOut.txt", "w+")
	for element in allBins:
		fileOut.write(str(element.value) + " " + str(element.count) + "\n")
	fileOut.close()

def histBins(filename, elementNum):
	fil = open(filename, "r+")
	filLines = fil.readlines()
	bins = []
	for i in range(1, len(filLines)):
		elements = filLines[i].split(" - ")
		if (i == 1):
			print elements
		if elementNum == -1:
			for j in range(0, len(elements)-1):
				bins.append(int(elements[j]))
		else:
			bins.append(int(elements[elementNum]))
	figure = pyplot.figure()
	axes = figure.add_subplot(111)
	axes.set_xlabel("Bin Number")
	axes.set_ylabel("Frequency")
	axes.set_title("Histogram of CERN Data for Tracking Trigger")
	axes.hist(bins, 100, normed=1, facecolor = 'green', alpha = 0.75)
	pyplot.show()

def separateByBit(filename, elementNum):
	dataFile = open(filename, "r+")
	dataLines = dataFile.readlines()
	counts = []
	numBits = 15
	for c in range(0, numBits):
		counts.append(0)
	for dl in range(1, len(dataLines)):
		value = int(dataLines[dl].split(" - ")[elementNum])
		binValue = bin(value)[2:]
		while (len(binValue) < numBits):
			binValue = "0" + binValue
		if (dl < 5):
			print binValue + " " + str(value)
		for bv in range(0, len(binValue)):
			counts[bv] += int(binValue[bv])
	for c2 in range(0, len(counts)):
		print str(c2) + " " + str(counts[c2])
	pyplot.bar(range(0, numBits), counts)
	pyplot.xlabel("Bit Number")
	pyplot.ylabel("Frequency that Bit Is Set to 1")
	pyplot.title("Bit Frequency Analysis for Layer " + str(elementNum))
	pyplot.show()

def combo4Bits(filename, nandBits, elementNum):
	dataFile = open(filename, "r+")
	counts = []
	for i1 in range(0, 2):
		counts.append([])
		for i2 in range(0, 2):
			counts[i1].append([])
			for i3 in range(0, 2):
				counts[i1][i2].append([])
				for i4 in range(0, 2):
					counts[i1][i2][i3].append(0)
	data = dataFile.readlines()
	for line in data:
		if (data.index(line) == 0):
			continue
		l = line.split(" - ")
		values = []
		for v in range(0, len(l)-1):
			values.append(int(l[v]))
		binVal = bin(values[elementNum])[2:]
		while (len(binVal) < 15):
			binVal = "0" + binVal
		counts[int(binVal[nandBits[0]])][int(binVal[nandBits[1]])][int(binVal[nandBits[2]])][int(binVal[nandBits[3]])] += 1
	outputX = []
	outputY = []
	for j1 in range(0, 2):
		for j2 in range(0, 2):
			for j3 in range(0, 2):
				for j4 in range(0, 2):
					outputX.append(str(str(j1)+str(j2)+str(j3)+str(j4)))
					outputY.append(counts[j1][j2][j3][j4])
	pyplot.bar(range(0, 16), outputY)
	pyplot.xticks(range(0, 16), outputX)
	pyplot.xlim(0, 17)
	pyplot.ylim(0, 10000)
	pyplot.xlabel("NAND Bit Configuration")
	pyplot.ylabel("Number of Values in this Configuration")
	pyplot.title("Number of Values in each NAND Bit Configuration")
	pyplot.show()
	return counts

def probNandMatching(filename, nandBits, patternNum, elementNum, stats):
	dataFile = open(filename, "r+")
	data = dataFile.readlines()
	binPattern = bin(int(data[patternNum].split(" - ")[elementNum]))[2:]
	bankSize = 10000
	while (len(binPattern) < 15):
		binPattern = "0" + binPattern
	counts = []
	for c in range(0, 5):
		counts.append(0)
	#for line in data:
		#if ((data.index(line) == 0) or (data.index(line) == patternNum)):
			#continue
		#thisVal = bin(int(line.split(" - ")[elementNum]))[2:]
		#while (len(thisVal) < 15):
			#thisVal = "0" + thisVal
		#compareValue = 4
		#for n in range(0, 4):
			#if (thisVal[nandBits[n]] != binPattern[nandBits[n]]):
				#compareValue -= 1
		#counts[compareValue] += 1

	#stats = combo4Bits(filename, nandBits, elementNum)
	for n1 in range(0, 2):
		for n2 in range(0, 2):
			for n3 in range(0, 2):
				for n4 in range(0, 2):
					compareValue = 4
					if (binPattern[nandBits[0]] != str(n1)):	compareValue -= 1
					if (binPattern[nandBits[1]] != str(n2)):	compareValue -= 1
					if (binPattern[nandBits[2]] != str(n3)):	compareValue -= 1
					if (binPattern[nandBits[3]] != str(n4)):	compareValue -= 1
					counts[compareValue] += stats[n1][n2][n3][n4]
	for c2 in range(0, 5):
		print str(c2) + " Matching: " + str(float(counts[c2])/bankSize)
	return [float(counts[0])/bankSize, float(counts[1])/bankSize, float(counts[2])/bankSize, float(counts[3])/bankSize, float(counts[4])/bankSize]

def probNandPlot(filename, nandBits, elementNum):
	hist1 = []
	hist2 = []
	hist3 = []
	hist4 = []
	dataFile = open(filename, "r+")
	data = dataFile.readlines()
	fileStats = combo4Bits(filename, nandBits, elementNum)
	for l in range(1, len(data)):
		info = probNandMatching(filename, nandBits, l, elementNum, fileStats)
		hist1.append(info[1])
		hist2.append(info[2])
		hist3.append(info[3])
		hist4.append(info[4])
	#pylab.hist([np.array(hist1), np.array(hist2), np.array(hist3), np.array(hist4)], 100, normed=1, histtype='bar', color='magenta', label=['1 Match', '2 Matches', '3 Matches', '4 Matches'], fill=False)
	#pylab.legend()
	#print len(hist1)
	#print len(hist2)
	#print len(hist3)
	#print len(hist4)
	#print hist1
	#pylab.hist(hist1, 500, normed=1, histtype='step', color='magenta', label='1 Match', fill=False)
	#pylab.hist(hist2, 100, normed=1, histtype='bar', color='blueviolet', label='2 Matches', fill=False)
	#pylab.hist(hist3, 50, normed=1, histtype='step', color='darkorange', label='3 Matches', fill=False)
	#pylab.hist(hist4, 50, normed=1, histtype='step', color='darkolivegreen', label='4 Matches', fill=False)
	#pylab.legend()
	#pylab.xlim(0, 1)
	#pylab.ylim(0, 600)
	#pylab.show()
	#pylab.hist(hist2, 100, normed=1, histtype='bar'
	#figure = pyplot.figure()
	#axes = figure.add_subplot(111)
	n = [[], [], [], []]
	b = []
	for i in range(0, 50):
		b.append(0.02*i)
	n[0], b = np.histogram(hist1, bins=b)
	print n[0]
	print b
	n[1], b = np.histogram(hist2, bins=b)
	n[2], b = np.histogram(hist3, bins=b)
	n[3], b = np.histogram(hist4, bins=b)
	#pyplot.cla()
	colors = ['green', 'blue', 'red', 'orange']
	x = []
	for bI in range(0, len(b)-1):
		x.append((b[bI]+b[bI+1])/2.0)
	#pyplot.figure()
	bot = []
	for botI in range(0, len(n[0])):
		bot.append(0)
	for j in range(0, 4):
		pyplot.figure()
		pyplot.bar(b[0:len(b)-1], n[j], facecolor=colors[j], width=0.02)
		bot += n[j]
	#pyplot.hist(hist1, bins=100)
		pyplot.xlim(0, 1)
		pyplot.ylim(0, 10000)
		pyplot.xlabel("Probability")
		pyplot.ylabel("Frequency")
		pyplot.title("Histogram of Probability - " + str(j) + " NAND Bits Matching")
	#axes.set_xlim(0, 1000)
	#axes.set_ylim(0, 5000)
	pyplot.show()
