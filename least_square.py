import numpy as np
from vectors import getClassTypes, getObjVec

## get all the class vectors
classTypes = getClassTypes()
numclassType = len(classTypes)
objVec = getObjVec()

## concatenate vectors into matrix
dim = (1000, numclassType)
classMatrix = np.zeros(dim)
for i in range(numclassType):
	classMatrix[:,i] = classTypes[i]
classMatrixTrans = np.transpose(classMatrix)

## least square optimization, using analytic solution
decisionVar = np.linalg.inv(classMatrixTrans.dot(classMatrix)).dot(classMatrixTrans).dot(objVec)
print decisionVar




