import os
import sys
import time
import random
from pVIPRAM_inputBuilderClass import *

def noneWrong(correctArr, iP, row):
	iP.checkPattern(correctArr, row)

def oneWrong(correctArr, iP, row):
	for i in range(0, len(correctArr)):
		newArr = [correctArr1[0], correctArr1[1], correctArr[2], correctArr[3]]
		#newArr[i] = 1-newArr[i]
		newArr[i] = 1+newArr[i]
		inputP.checkPattern(newArr, row)

def twoWrong(correctArr, iP, row):
	for i in range(1, len(correctArr)):
		for j in range(0, i):	
			newArr = [correctArr1[0], correctArr1[1], correctArr[2], correctArr[3]]
			#newArr[i] = 1 - newArr[i]
			#newArr[j] = 1 - newArr[j]
			newArr[i] = 1 + newArr[i]
			newArr[j] = 1 + newArr[j]
			inputP.checkPattern(newArr, row)

def threeWrong(correctArr, iP, row):
	for i in range(0, len(correctArr)):
		newArr = [correctArr1[0], correctArr[1], correctArr[2], correctArr[3]]
		for j in range(0, len(correctArr)):
			if j != i:
				#newArr[j] = 1-newArr[j]
				newArr[j] = 1+newArr[j]
		inputP.checkPattern(newArr, row)

def allWrong(correctArr, iP, row):
	wrongArr = []
	for i in range(0, len(correctArr)):
		#wrongArr.append(1-correctArr[i])
		wrongArr.append(1+correctArr[i])
	inputP.checkPattern(wrongArr, row)

def GenerateInputs(filename):
	inputP = inputBuilder("root/" + filename + ".root")
	inputP.initializeLoadPhase()
	#Test Miss0
	#Row = 0
	for c0 in range(0, 10):
		inputP.loadSinglePattern(0, c0, [0, 0, 0, 0], 10)
	#Miss1
	for c1 in range(10, 20):
		inputP.loadSinglePattern(1, c1, [0, 0, 0, 1], 10)
	#Miss2
	for c2 in range(20, 30):
		inputP.loadSinglePattern(2, c2, [0, 0, 1, 1], 10)
	#RequireLayerA only
	for cA in range(0, 10):
		inputP.loadSinglePattern(3, cA, [1, 0, 0, 0], 10)
	
	#Miss0 and Miss1
	for c01 in range(10, 20):
		inputP.loadSinglePattern(4, c01, [0, 0, 0, 0], 10)

	#Miss0 and Miss2
	for c02 in range(20, 30):
		inputP.loadSinglePattern(5, c02, [0, 0, 0, 0], 10)

	#Miss1 and Miss2
	for c12 in range(0, 10):
		inputP.loadSinglePattern(6, c12, [1, 1, 1, 1], 10)

	#Miss0 and Miss1 and Miss2
	for c012 in range(10, 20):
		inputP.loadSinglePattern(7, c012, [0, 0, 0, 0], 10)

	#Miss0 and RequireLayerA
	for c0A in range(20, 30):
		inputP.loadSinglePattern(8, c0A, [0, 0, 0, 0], 10)

	#Only Miss0
	inputP.initializeRunPhase([1, 0, 0, 0])
	correctArr0 = [0, 0, 0, 0]
	#Match:
	noneWrong(correctArr0, inputP, 0)
	#All mismatches:
	oneWrong(correctArr0, inputP, 0)
	twoWrong(correctArr0, inputP, 0)
	threeWrong(correctArr0, inputP, 0)
	allWrong(correctArr0, inputP, 0)
	
	#Only Miss1
	inputP.changeLogic([0, 1, 0, 0])
	correctArr1 = [0, 0, 0, 1]
	#All Matches:
	oneWrong(correctArr1, inputP, 1)
	#All mismatches:
	noneWrong(correctArr1, inputP, 1)
	twoWrong(correctArr1, inputP, 1)
	threeWrong(correctArr1, inputP, 1)
	allWrong(correctArr1, inputP, 1)

	#Only Miss2
	inputP.changeLogic([0, 0, 1, 0])
	correctArr2 = [0, 0, 1, 1]
	#All Matches:
	twoWrong(correctArr2, inputP, 2)
	#All Mismatches:
	noneWrong(correctArr2, inputP, 2)
	oneWrong(correctArr2, inputP, 2)
	threeWrong(correctArr2, inputP, 2)
	allWrong(correctArr2, inputP, 2)
	
	#Only RequireLayerA
	inputP.changeLogic([0, 0, 0, 1])
	correctArrA = [1, 0, 0, 0]
	#All Matches:
	for i in range(0, 2):
		for j in range(0, 2):
			for k in range(0, 2):
				inputP.checkPattern([correctArrA[0], i, j, k], 3)
	#All Mismatches:
	for i in range(0, 2):
		for j in range(0, 2):
			for k in range(0, 2):
				inputP.checkPattern([1-correctArrA[0], i, j, k], 3)
	
	#Miss0 and Miss1
	inputP.changeLogic([1, 1, 0, 0])
	correctArr01 = [0, 0, 0, 0]
	#All Matches:
	noneWrong(correctArr01, inputP, 4)
	oneWrong(correctArr01, inputP, 4)
	#All Mismatches:
	twoWrong(correctArr01, inputP, 4)
	threeWrong(correctArr01, inputP, 4)
	allWrong(correctArr01, inputP, 4)

	#Miss0 and Miss2
	inputP.changeLogic([1, 0, 1, 0])
	correctArr02 = [0, 0, 0, 0]
	#All Matches:
	noneWrong(correctArr02, inputP, 5)
	twoWrong(correctArr02, inputP, 5)
	#All Mismatches:
	oneWrong(correctArr02, inputP, 5)
	threeWrong(correctArr02, inputP, 5)
	allWrong(correctArr02, inputP, 5)

	#Miss1 and Miss2
	inputP.changeLogic([0, 1, 1, 0])
	correctArr12 = [1, 1, 1, 1]
	#All Matches:
	oneWrong(correctArr12, inputP, 6)
	twoWrong(correctArr12, inputP, 6)
	#All Mismatches:
	noneWrong(correctArr12, inputP, 6)
	threeWrong(correctArr12, inputP, 6)
	allWrong(correctArr12, inputP, 6)

	#Miss0 and Miss1 and Miss2
	inputP.changeLogic([1, 1, 1, 0])
	correctArr012 = [0, 0, 0, 0]
	#All Matches:
	noneWrong(correctArr012, inputP, 7)
	oneWrong(correctArr012, inputP, 7)
	twoWrong(correctArr012, inputP, 7)
	#All Mismatches:
	threeWrong(correctArr012, inputP, 7)
	allWrong(correctArr012, inputP, 7)
	
	#Miss0 and RequireLayerA
	inputP.changeLogic([1, 0, 0, 1])
	correctArr0A = [0, 0, 0, 0]
	#All Matches:
	noneWrong(correctArr0A, inputP, 8)
	#All Mismatches:
	for i in range(0, 2):
		for j in range(0, 2):
			for k in range(0, 2):
				for m in range(0, 2):
					if (i == correctArr0A[0] and j == correctArr0A[1] and k == correctArr0A[2] and m == correctArr0A[3]):
						continue
					else:
						checkPattern([i, j, k, m], 8)

	#Miss1 and RequireLayerA
	inputP.changeLogic([0, 1, 0, 1])
	correctArr1A = [1, 0, 0, 0]
	#All Matches:
	
