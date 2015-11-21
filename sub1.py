import numpy as np
def main():
	numM = raw_input("Number of workers having multiple skills: ")
	numS = raw_input("Number of workers having a single skill: ")
	timeI = raw_input("Number of time segments: ")
	classtype = raw_input("Number of classtype  input ")
	fakeData = subProb1Dat(int(numM), int(numS), int(timeI))
	newWRA = solver1(fakeData[0], fakeData[1], fakeData[2],fakeData[4])
	newWU  = solver2(fakeData[1], fakeData[3],fakeData[5])
	print 'updated WRA:'
	print newWRA
	print 'updated w/u:'
	print newWU0

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
	wu  = np.random.randint(20, size=numS*timeI).reshape(numS, timeI)
	wrb= wra+np.random.randint(20, size=numM*numS*timeI).reshape(numM, numS, timeI)
	wub = wu+np.random.randint(20, size=numS*timeI).reshape(numS, timeI)
	return [lagMul1, lagMul2, wra, wrb, wu ,wub]

def solver1(lagMul1, lagMul2, wra, wrb):
	dim1 = lagMul1.shape
	dim2 = lagMul2.shape
	for i in range(dim1[0]):
		for j in range(dim2[0]):
			for k in range(dim1[1]):
					if lagMul1[i,k] > lagMul2[j,k]:
						wra[i,j,k] = 0
					else:
						wra[i,j,k] = wrb[i,j] #some big value
	return wra
def solver2(lagMul2,wu,wub):
	dim2 = lagMul2.shape
	for i in range(dim2[0]):
		for j in range(dim2[1]):
			if lagMul2[i,j]<1:
				wu[i,j]=0
			else:
				wu[i,j]=wub[i,j]
	return wu
# def subgradientsolver(lagMul1,lagMul2,newwra,newwu,newwas,newwam,classinfom,demand,delta):
# 	dim1=lagMul1.shape
# 	dim2=lagMul2.shape
# 	dim3=classinfom.shape
# 	for i in range(dim1[0]):
# 		for j in range(dim1[1]):
# 			wrasum[i,j]=0
# 			for k in range(dim2[0]):
# 				wrasum[i,j]=newwra[i,k,j]
# 			for c in range(dim3[0]):
# 				wamc[i,j]=newwam[i,c]*classinfom[c,j]
# 			subgrad1[i,j]=wrasum[i,j]-wamc[i,j]
            if subgrad1[i,j]=
# 			newlagMul1[i,j]=lagMul1[i,j]+delta*subgrad1[i,j]
# 	for i in range(dim2[0]):
# 		for j in range(dim2[1]):
# 			wrasum[i,j]=0
# 			for k in range(dim1[0]):
# 				wrasum[i,j]=newwra[k,i,j]
# 			for c in range(dim3[0]):
# 				wasc[i,j]=newwas[i,c]*classinfom[c,j]
# 			subgrad2[i,j]=demand[i,j]-wrasum[i,j]-wasc[i,j]-newwu[i,j]
# 			newlagMul2[i,j]=lagMul2[i,j]+delta*subgrad2[i,j]

#     return [newlagMul1,newlagMul2]
if __name__ == "__main__":
    main()    
