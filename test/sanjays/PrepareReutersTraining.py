trainingFile = open("ReutersTraining.txt", "w+")

for num in range(0, 21):
	strNum = str(num)
	while (len(strNum) < 3):
		strNum = "0" + strNum
	inputFile = open("reut2-" + strNum + ".sgm", "r+")
	inputLines = inputFile.readlines()
	il = 0
	flag = 2
	while (il < len(inputLines)):
		if (flag == 2):
			if (("<TOPICS>" in inputLines[il]) and (("\"TRAIN\"" in inputLines[il-3]) or ("\"TRAIN\"" in inputLines[il-2]))):
				print inputLines[il]
				trainingFile.write("NEW DOCUMENT\n")
				flag2 = 0
				for j in range(0, 6):
					items = inputLines[il+j].split("<D>")
					if (len(items) > 1):
						flag2 = 1
						for it in range(1, len(items)):
							trainingFile.write(items[it].split("</D>")[0] + " ")
				if (flag2 == 1):
					trainingFile.write("\n")
				flag = 0
				il += 6
			else:
				il += 1
		elif flag == 0:
			if ("<TITLE>" in inputLines[il]):
				trainingFile.write(inputLines[il].split("<TITLE>")[1].split("</TITLE>")[0] + "\n")
				print inputLines[il]
				if ("</TITLE>" in inputLines[il]):
					trainingFile.write(inputLines[il].split("</TITLE>")[1] + "\n")
				flag = 1
			il += 1
		else:
			trainingFile.write(inputLines[il])
			if ("</TEXT>" in inputLines[il]):
				flag = 2
			il += 1
	inputFile.close()
trainingFile.close()