import matplotlib.pyplot as pyplot
from matplotlib.patches import *
import numpy as np
from math import *

def logisticFunction(f, N):
	#a1 = 23.9958
	#a2 = -0.189942
	#a3 = -0.13193
	#a1 = 24.5235
	#a2 = -0.193081
	#a3 = -0.13514
	#a1 = 24.39
	#a2 = -0.192351
	#a3 = -0.134203
	#WITHOUT 100 MHz DATA
	#a1 = 26.1727
	#a2 = -0.19861
	#a3 = -0.147887
	a1 = 35.4468
	a2 = -0.267674
	a3 = -0.201668
	#a1 = 29.4257
	#a2 = -0.222864
	#a3 = -0.166692
	return np.exp(a1+(a2*f)+(a3*N))/(1.0+np.exp(a1+(a2*f)+(a3*N)))

def logisticFunctionBetter(f, N):
	#a1 = 37.4722
	#a2 = -0.274156
	#a3 = -60.5223
	#Error ^ 0.00575921 <-- WRONG!!
	a1 = 35.7412
	a2 = -0.261266
	a3 = -18.0922
	#Error ^ 0.006
	print sqrt(N/100.0)
	return np.exp(a1+(a2*f)+(a3*sqrt(N/100.0)))/(1.0+np.exp(a1+(a2*f)+(a3*sqrt(N/100.0))))

def logisticFunctionF(f, coeff0, coeff1):
	return np.exp(coeff0+(coeff1*f))/(1.0+np.exp(coeff0+(coeff1*f)))

#def plotEffFrequency(logfileNames, freqList):
def plotEffFrequency(summaryfile, freqList, NList):
	#logfiles = []
	#for ln in logfileNames:
		#logfiles.append(open(ln, "r+"))
	#logLines = []
	#for l in logfiles:
		#logLines.append(l.readlines())
	#totalMatches = np.zeros(len(logLines))
	#for ll in range(0, len(logLines)):
		#for i in range(0, len(logLines[ll])):
			#if ("matches!" in logLines[ll][i]):
				#totalMatches[ll] += int(logLines[ll][i].split(" ")[2])
	colorList1 = ["ro", "bo", "go", "yo", "ko", "mo"]
	colorList2 = ['r', 'b', 'g', 'y', 'k', 'm']
	colorDesc = ["red", "blue", "green", "yellow", "black", "magenta"]
	summaryFile = open(summaryfile, "r+")
	summary = summaryFile.readlines()
	totalCompares = 1024.0
	for n in range(0, 6):
		efficiency = []
		for f in freqList:
			for s in summary:
				if ((int(s.split(" ")[1]) == f) and (int(s.split(" ")[2]) == NList[n])):
					efficiency.append(float(int(s.split(" ")[0]))/totalCompares)
					break
		pyplot.plot(freqList, efficiency, colorList1[n])
		#pyplot.plot(freqList, efficiency, colorList2[n])
		print "N = " + str(NList[n]) + " -> " + colorDesc[n]
	
	#pyplot.plot(freqList, totalMatches)
		freq = np.arange(0, 200, 1)
		result = logisticFunctionBetter(freq, float(NList[n]))
		pyplot.plot(freq, result, color=colorDesc[n])
	#pyplot.plot(freq, logisticFunctionF(freq, 41.6086, -0.301068), colorDesc[0])
	#pyplot.plot(freq, logisticFunctionF(freq, 24.7862, -0.224745), colorDesc[1])
	#pyplot.plot(freq, logisticFunctionF(freq, 45.0752, -0.490972), colorDesc[2])
	#pyplot.plot(freq, logisticFunctionF(freq, 33.4962, -0.39820), colorDesc[3])
	#pyplot.plot(freq, logisticFunctionF(freq, 19.9067, -0.270282), colorDesc[4])
	#pyplot.plot(freq, logisticFunctionF(freq, 17.2841, -0.267544), colorDesc[5])
	pyplot.xlabel("Frequency (Hz)")
	pyplot.ylabel("Efficiency (Number of Matches)")
	pyplot.xlim(0, 200)
	pyplot.ylim(0, 1.1)
	pyplot.title("Efficiency vs. Frequency")
	patchList = []
	labels = []
	for nval in range(0, 6):
		patchList.append(Patch(color=colorDesc[nval]))
		labels.append("N = " + str(nval*20))
	pyplot.legend(patchList, labels, loc='upper right')
	pyplot.show()

def nFunc(N):
	#return sqrt(N/100.0)
	return int(N)
#def prepareDataFiles(logfileNames):
def prepareDataFiles(fList, NList):
	logfileNames = []
	for fL in fList:
		for nL in NList:
			logfileNames.append("logfile"+str(fL)+"MHzNewStressBN"+str(nL)+".log")
	#for olf in otherLogFiles:
		#logfileNames.append(olf)
	#Format of logfile names in logfileNames: "logfile{freq}MHzNewStressBN{N_val}.log"
	detailedFile = open("NPercentTestColumnData.txt", "w+")
	summaryFile = open("NPercentTestSummary.txt", "w+")
	N_Max = 4096.0
	#detailedFile format: M 1/f N/N_Max R C
	#summaryFile format: Num_matches f N (all integers)
	totalChecks = int(N_Max/4)
	row_max = 128
	col_max = 32
	for logName in logfileNames:
		print logName
		logfile = open(logName, "r+")
		logLines = logfile.readlines()
		freq = float(logName.split("file")[1].split("MHz")[0])
		N = float(logName.split("BN")[1].split(".log")[0])
		#N=20
		rowCount = 0
		colCount = 0
		mismatchCount = 0
		for l in logLines:
			if ("checkData" in l):
				mismatchCount += 1
				rowEnd = int(l.split(" ")[14])
				colEnd = int(l.split("[")[1].split("]")[0])
				while ((rowCount < rowEnd) or (colCount < colEnd)):
					detailedFile.write("1 " + str(freq) + " " + str(N) + " " + str(float(colCount)) + "\n") #+ str(float(rowCount)/row_max) + " "
					colCount += 4
					#print colCount
					if (colCount == col_max):
						rowCount += 1
						colCount = 0
				detailedFile.write("0 " + str(freq) + " " + str(N) + " " + str(float(colEnd)) + "\n") #+ str(float(rowEnd)/row_max) + " "
				colCount += 4
				if (colCount == col_max):
					rowCount += 1
					colCount = 0
		summaryFile.write(str(int(totalChecks-mismatchCount)) + " " + str(int(freq)) + " " + str(nFunc(float(N))) + "\n")
		while ((rowCount < row_max) or (colCount < col_max)):
			if (colCount == 32):
				colCount = 0
			detailedFile.write("1 " + str(freq) + " " + str(N) + " " + str(float(colCount)) + "\n") #+ str(float(rowCount)/row_max) + " "
			colCount += 4
			if (colCount == col_max):
				rowCount += 1
	detailedFile.close()
	summaryFile.close()

def compileColumnData(logfiles):
	#colFil = open(colFile, "r+")
	#cols = np.zeros(32)
	#totMismatches = 0
	#for cf in colFil:
		#if (int(cf.split(" ")[0]) == 0):
			#cols[int(float(cf.split(" ")[len(cf.split(" "))-1].split("\n")[0]))] += 1
			#totMismatches += 1
	#colFil.close()
	colFilWrite = open("NormalDistrInput.txt", "w+")
	#for c in range(0, len(cols)):
		#colFilWrite.write(str(float(cols[c])/float(totMismatches)) + " 100.0 20.0 " + str(c) + "\n")
	#colFilWrite.close()
	cols = np.zeros(32)
	totMismatches = 0
	for l in logfiles:
		log = open(l, "r+")
		loglines = log.readlines()
		for ll in loglines:
			if ("checkData" in ll):
				column = int(ll.split("[")[1].split("]")[0])
				cols[column] += 1
				totMismatches += 1
	for c in range(0, 32):
		colFilWrite.write(str(c) + " " + str(float(cols[c])/float(totMismatches)) + "\n")

def measureEfficiency(logfiles, totalChecks):
#def measureEfficiency(f, N, totalChecks):
	#logfiles = []
	#for B in range(2, 6):
		#logfiles.append("logfile" + str(f) + "MHzNewStressB" + str(B) + "N" + str(N) + ".log")
	mismatches = 0
	for l in logfiles:
		lines = (open(l, "r+").readlines())
		for line in lines:
			if ("checkData" in line):
				mismatches += 1
	print mismatches
	return 1.0-(float(mismatches)/float(totalChecks))
