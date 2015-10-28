from vectors import getClassTypes, getObjVec
from scipy.optimize import nnls
import numpy as np

## get all the class vectors
classTypes = getClassTypes()
numclassType = len(classTypes)
objVec = getObjVec()

## concatenate vectors into matrix
dim = (100, numclassType)
classMatrix = np.zeros(dim)
for i in range(numclassType):
	classMatrix[:,i] = classTypes[i]
classMatrixTrans = np.transpose(classMatrix)

decisionVar = nnls(classMatrix, objVec)
print decisionVar

