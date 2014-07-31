import random
import numpy as np
import sys

if __name__ == "__main__":
	lineNums = np.zeros(10000)
	dataFile = open(sys.argv[1], "r+")
	rearrangedFile = open("Rearranged" + sys.argv[1], "w+")
	dataLines = dataFile.readlines()
	rearrangedFile.write("Filler Line...\n")
	for count in range(0, 4096):
		chosen = random.randint(1, 9999)
		while (lineNums[chosen] == 1):
			chosen = random.randint(1, 9999)
		lineNums[chosen] = 1
		rearrangedFile.write(dataLines[chosen])
	rearrangedFile.close()
