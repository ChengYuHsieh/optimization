import numpy as np

def subProb3Dat(numSkill, numClass, numIntvl):
    LMMat = np.zeros((numSkill, numIntvl))
    numSkillUBs = np.random.randint(20, size=numSkill)
    classMat = np.random.randint(2, size=numClass*numIntvl).reshape(numClass,numIntvl)
    return LMMat, numSkillUBs, classMat

def solver3(numSkill, numClass, LMMat, classMat, numSkillUBs): ### all inputs shall be type Int

    ### multiply each col of classMat by corresponding LMVec
    def LMClassMat(classMat, LMVec):
        mat = np.copy(classMat)
        numIntvl = mat.shape[1]
        for i in range(numIntvl):
            mat[:,i] = mat[:,i] * LMVec[i]
        return mat

    ### start solving
    assignmentMat = np.zeros((numSkill, numClass))
    for i in range(numSkill):
        mat = LMClassMat(classMat, LMMat[i,:])
        matRowSum = [sum(mat[k,:]) for k in range(mat.shape[0])]
        maxIndxs = [n for n,m in enumerate(matRowSum) if m==max(matRowSum)]
        divisible = True if (numSkillUBs[i] % len(maxIndxs))==0 else False
        for j in maxIndxs:
            assignmentMat[i,j] = numSkillUBs[i] / len(maxIndxs)
            if divisible == False:
                assignmentMat[i,maxIndxs[0]] += numSkillUBs[i] - sum(assignmentMat[i,:])
    return assignmentMat

def main():
    numS = int(raw_input("Number of skills: "))
    numC = int(raw_input("Number of class types: "))
    numI = int(raw_input("Number of time intervals: "))

    params = subProb3Dat(numS, numC, numI)
    LMMat = params[0]
    numSkillUBs = params[1]
    classMat = params[2]

    assignmentMat = solver3(numS, numC, LMMat, classMat, numSkillUBs)
    print assignmentMat

if __name__ == "__main__":
    main()
