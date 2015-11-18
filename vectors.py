import numpy as np

def main():
	pass

def getClassTypes():
    classType = []
    for i in range(10):
        classType.append(np.random.randint(2, size=1000))
    return classType

def getObjVec():
	return np.random.randint(20, size=1000)



if __name__ == "__main__":
	main()
