import numpy as np

def main():
	numM = raw_input("Number of workers having multiple skills: ")
	numS = raw_input("Number of workers having a single skill: ")
	timeI = raw_input("Number of time segments: ")
	fakeData = subProb1Dat(int(numM), int(numS), int(timeI))
	newWRA = solver1(fakeData[0], fakeData[1], fakeData[2])
	print 'updated WRA:'
	print newWRA

def subProb1Dat(numM,numS,timeI):
	### initialize lagrangian multipliers
	lagMul1 = np.random.randint(20, size=numM*timeI).reshape(numM, timeI)
	lagMul2 = np.random.randint(20, size=numS*timeI).reshape(numS, timeI)
	print 'lagMul1: '
	print lagMul1
	print 'lagMul2: '
	print lagMul2
	### random ndarray in the range of 20
	wra = np.random.randint(20, size=numM*numS*timeI).reshape(numM, numS, timeI)
	print 'wra: '
	print wra
	return [lagMul1, lagMul2, wra]

def solver1(lagMul1, lagMul2, wra):
	dim1 = lagMul1.shape
	dim2 = lagMul2.shape
	for i in range(dim1[0]):
		for j in range(dim2[0]):
			for k in range(dim1[1]):
					if lagMul1[i,k] > lagMul2[j,k]:
						wra[i,j,k] = 0
					else:
						wra[i,j,k] = 1000 #some big value
	return wra

if __name__ == "__main__":
    main()
