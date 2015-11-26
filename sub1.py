import numpy as np
import sub3 as s3
import math

def main():
    numM = int(raw_input("Number of multiple skills: "))
    numS = int(raw_input("Number of single skills: "))
    timeI = int(raw_input("Number of time intervals: "))
    numC = int(raw_input("Number of class types: "))

    # initialize lagrangian multipliers
    lagMul1 = np.zeros((numM, timeI))
    lagMul2 = np.zeros((numS, timeI))
    params = paramsGen(numM, numS, numC, timeI)
    delta = 1
    for i in range(1,10000):
        delta = delta / math.sqrt(i)
        #solver1, 2
        newWRA = solver1(lagMul1, lagMul2, params[0], params[1])
        newWU = solver2(lagMul2, params[2], params[3])
        print 'updated WRA:'
        print newWRA
        print 'updated w/u:'
        print newWU

        #solver3, 4
        newWAs = s3.solver3(numS, numC, lagMul2, params[6], params[4])
        newWAm = s3.solver3(numM, numC, lagMul1, params[6], params[5])
        print 'updated WAs:'
        print newWAs
        print 'updated WAm:'
        print newWAm

        newLMs = subgradientsolver(lagMul1, lagMul2, newWRA, newWU, newWAs, newWAm,
                                params[6], params[7], delta)

def paramsGen(numM, numS, numC, timeI):
    # random ndarray in the range of 20
    wra = np.zeros((numM, numS, timeI))
    # wrb is the upper bound for wra
    wrb = np.random.randint(20, size=numM*numS).reshape(numM, numS)
    wu = np.zeros((numS, timeI))
    # wu is the upper bound for wu
    wub = np.random.randint(20, size=numS*timeI).reshape(numS, timeI)
    # for sub3 and sub4
    numSUBs = np.random.randint(20, size=numS)
    numMUBs = np.random.randint(20, size=numM)
    # class Matrix
    classMat = np.random.randint(2, size=numC*timeI).reshape(numC,timeI)
    # demand Matrix
    demand = np.random.randint(5, size=numS*timeI).reshape(numS, timeI)

    return [wra, wrb, wu, wub, numSUBs, numMUBs, classMat, demand]


def solver1(lagMul1, lagMul2, wra, wrb):
    dim1 = lagMul1.shape
    dim2 = lagMul2.shape
    for i in range(dim1[0]):
        for j in range(dim2[0]):
            for k in range(dim1[1]):
                if lagMul1[i, k] > lagMul2[j, k]:
                    wra[i, j, k] = 0
                else:
                    wra[i, j, k] = wrb[i, j]
    return wra


def solver2(lagMul2, wu, wub):
    dim2 = lagMul2.shape
    for i in range(dim2[0]):
        for j in range(dim2[1]):
            if lagMul2[i, j] < 1:
                wu[i, j] = 0
            else:
                wu[i, j] = wub[i, j]
    return wu


def subgradientsolver(lagmul1, lagmul2, newwra, newwu, newwas, newwam,
                      classinfom, demand, delta):
    dim1 = lagmul1.shape
    dim2 = lagmul2.shape
    dim3 = classinfom.shape
    subgrad1 = np.zeros((dim1[0], dim1[1]))
    wrasum = np.zeros((dim1[0], dim1[1]))
    wamc = np.zeros((dim1[0], dim1[1]))
    newlagmul1 = np.zeros((dim1[0], dim1[1]))

    for i in range(dim1[0]):
        for j in range(dim1[1]):
            for k in range(dim2[0]):
                wrasum[i, j] += newwra[i, k, j]
            for c in range(dim3[0]):
                wamc[i, j] = newwam[i, c]*classinfom[c, j]
            subgrad1[i, j] = wrasum[i, j]-wamc[i, j]
            newlagmul1[i, j] = lagmul1[i, j]+delta*subgrad1[i, j]
            if newlagmul1[i, j] < 0:
                newlagmul1[i, j] = 0
    print subgrad1

    subgrad2 = np.zeros((dim2[0], dim2[1]))
    wrasum = np.zeros((dim2[0], dim2[1]))
    wasc = np.zeros((dim2[0], dim2[1]))
    newlagmul2 = np.zeros((dim2[0], dim2[1]))

    for i in range(dim2[0]):
        for j in range(dim2[1]):
            for k in range(dim1[0]):
                wrasum[i, j] = newwra[k, i, j]
            for c in range(dim3[0]):
                wasc[i, j] = newwas[i, c]*classinfom[c, j]
            subgrad2[i, j] = demand[i, j]-wrasum[i, j]-wasc[i, j]-newwu[i, j]
            newlagmul2[i, j] = lagmul2[i, j]+delta*subgrad2[i, j]
            if newlagmul2[i, j] < 0:
                newlagmul2[i, j] = 0
    print subgrad2

    return [newlagmul1, newlagmul2]

if __name__ == "__main__":
    main()
