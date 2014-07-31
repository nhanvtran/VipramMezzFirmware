from pVIPRAM_inputBuilderClass import *
class RankedEntity:
	def __init__(self, ident, score):
		self.id = ident
		self.score = score
	def __lt__(self, other):
		return self.score < other.score

def convertStrToInt(str):
	binNum = ""
	for s in str.lower():
		if ((ord(s) < 97) or (ord(s) > 122)):
			continue
		else:
			binThis = bin(ord(s)-96)
			while (len(binThis) < 5):
				binThis = "0" + binThis
			binNum += binThis
	if (len(binNum) > 0):
		return int(binNum, 2)
	return 0

def kNN(trainingFile, testFile, k):
	tr = open(trainingFile, "r+")
	te = open(testFile, "r+")
	trLines = tr.readlines()
	rowCount = 0
	colCount = 0
	lineNum = 0
	suffixes = ["ation", "ing"]
	passWords = ["the", "as", "a", "an", "then", "for", "with", "in"]
	documents = []
	classes = []
	d = -1
	while (lineNum < len(trLines)):
		if ((trLines[lineNum] != "NEW DOCUMENT\n") and (rowCount < 128)):
			line = trLines[lineNum].split(" ")
			for word in line:
				if (word in passWords):
					continue
				for s in suffixes:
					if (word[len(word)-len(s):] == s):
						word = word[:len(word)-len(s)]
				flag = 0
				for i in range(0, 4):
					if (len(word) > 3*i):
						length = min(len(word)-(3*i), 3)
						inWord = word[3*i:(3*i)+length]
						value = convertStrToInt(word)
						if (value != 0):
							documents[d][rowCount][colCount][i] = value
							flag = 1
						else:
							documents[d][rowCount][colCount][i] = 0
					else:
						documents[d][rowCount][colCount][i] = 0
				if (flag == 1):
					colCount += 1
					if (colCount == 32):
						rowCount += 1
						colCount = 0
						if (rowCount == 128):
							break
		elif (trLines[lineNum] == "NEW DOCUMENT\n"):
			while (rowCount < 128):
				for i2 in range(0, 4):
					documents[d][rowCount][colCount][i2] = 0
				colCount += 1
				if (colCount == 32):
					rowCount += 1
					colCount = 0
			d += 1
			rowCount = 0
			colCount = 0
			lineNum += 1
			classes.append([])
			for top in trLines[lineNum]:
				classes[d].append(top)
		
		lineNum += 1
	teLines = te.readlines()
	t = -1
	lineNum = 0
	tClass = []
	dScores = []
	#inputP = inputBuilder("root/tmp1.root")
	#rowCount = 0
	#colCount = 0
	while (lineNum < len(teLines)):
		if (teLines[lineNum] == "NEW DOCUMENT\n"):
			t += 1
			dScores = []
			lineNum += 2
		#elif (rowCount < 128):
		else:
			originalLine = lineNum
			for d in range(0, len(documents)):
				for round in range(0, 32):
					inputP = inputBuilder("root/tmp1.root")
					inputP.initializeLoadPhase()
					for row in range(4*round, (4*round)+4):
						for col in range(0, 32):
							inputP.loadSinglePattern(row, col, documents[d][row][col], 2)
					inputP.close()
					sendToChip(inputP)
				lineNum = originalLine
				while ((lineNum < len(teLines)) and (teLines[lineNum] != "NEW DOCUMENT\n")):
					line = teLines[lineNum]
					count = 0
					inputP = inputBuilder("root/tmp1.root")
					inputP.initializeRunPhase([1, 1, 0, 0])
					for word in line:
						if word in passWords:
							continue
						for s in suffixes:
							if (word[len(word)-len(s):] == s):
								word = word[:len(word)-len(s)]
						flag = 0
						inputArr = []
						for i in range(0, 4):
							if (len(word) > 3*i):
								length = min(len(word)-(3*i), 3)
								inWord = word[3*i:(3*i)+length]
								value = convertStrToInt(inWord)
								if (value != 0):
									flag = 1
								inputArr.append(value)
							else:
								inputArr.append(0)
						if (flag == 1):
							inputP.checkPattern(inputArr)
							count += 1
							if (count == 256):
								inputP.close()
								sendToChip(inputP)
								inputP = inputBuilder("root/tmp1.root")
								inputP.initializeRunPhase([1, 1, 0, 0])
								count = 0
					lineNum += 1
				inputP = inputBuilder("root/tmp1.root")
				inputP.initializeRunPhase([1, 0, 0, 0])
				for row in range(0, 128):
					inputP.checkPattern([0, 0, 0, 0], row)
					inputP.checkPattern([0, 0, 0, 0], row)
					inputP.doRowChecker(row)
					inputP.checkPattern([0, 0, 0, 0], row)
				inputP.close()
				sendToChip(inputP)
				getFromChip(inputP)
				iLineNum = 0
				iLines = (open("tmp1_i.txt", "r+")).readlines()
				fLines = (open("tmp1_f.txt", "r+")).readlines()
				score = 0
				while (iLineNum < len(iLines)):
					if (iLines[iLineNum][0] == "1"):
						val = ""
						for j in range(0, 32):
							if (fLines[iLineNum][j] == "1"):
								val += fLines[iLineNum][j]
							elif (len(val) > 0):
								score += int(val)
								val = ""
					iLineNum += 1
				heapq.heappush(dScores, RankedEntity(d, score))
			poss = []
			poss2 = []
			for ds in range(0, k):
				docObj = heapq.heappop(dScores)
				for p in range(0, len(classes[docObj.id])):
					if classes[docObj.id][p] not in poss2:
						poss.append(RankedEntity(classes[docObj.id][p], 1))
						poss2.append(classes[docObj.id][p])
					else:
						poss[poss2.index(classes[docObj.id][p])].score += 1
			heapq.heapify(poss)
			#flag = 0
			classif = []
			re = heapq.heappop(poss)
			while (re.score > 1):
				#flag = 1
				classif.append(re.id)
				re = heapq.heappop(poss)
			tClass.append(classif)
	for t in tClass:
		print str(tClass.index(t)) + " " + str(t)


