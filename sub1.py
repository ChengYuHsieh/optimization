import numpy as np
import sub3 as s3
import heuristic2
import io
import math

def solve(fileName):
    # parse input file
    params = io.inputParser(fileName)
    timeI = params[0]
    numS = params[1]
    numM = params[2]
    numC = params[3]
    demand = params[4]
    classMat = params[5]
    Mss = params[6]
    WSs = params[7]
    WSm = params[8]
    stop = 100;
    # initialize lagrangian multipliers
    lagMul1 = np.zeros((numM, timeI))
    lagMul2 = np.zeros((numS, timeI))
    # params = paramsGen(numM, numS, numC, timeI)
    delta = 100
    wra = np.zeros((numM, numS, timeI))
    wrb = np.zeros((numM, numS))
    wu = np.zeros((numS, timeI))
    wub = demand
    prelag = 2
    lag = 1
    smallflag = 0
    contiflag = 0
    for i in range(numM):
        for j in range(numS):
            wrb[i,j] = WSm[i]
    for i in range(1,50):
        print "Round"
        print i
        delta = delta / math.sqrt(100-i)
        if abs(lag-prelag)/(abs(prelag)+0.001)< 0.005:
            smallflag += 1
        else:
            smallflag = 0 
        if smallflag == 3:
            contiflag += 1
            delta = delta + i    
            smallflag = 0
        prelag = lag
        #solver1, 2
        newWRA = solver1(lagMul1, lagMul2, wra, wrb)
        newWU = solver2(lagMul2, wu, wub)
        #solver3, 4
        (newWAs, CAs) = s3.solver3(numS, numC, lagMul2, classMat, WSs)
        (newWAm, CAm) = s3.solver3(numM, numC, lagMul1, classMat, WSm)

        (lagMul1, lagMul2, stop , lag) = subgradientsolver(lagMul1, lagMul2, newWRA, newWU, newWAs, newWAm,
                                classMat, demand, delta)
 	if stop == 0 or contiflag > 2:
 	    break 
    
    print "--------------------"
    print "FINAL RESULT: WAs, WAm, WU"
    print newWAs, newWAm, newWU
    
    WU = 0
    for i in range(wu.shape[0]):
        for j in range(wu.shape[1]):
            WU += wu[i,j]  
    print "sum WU"
    print WU
    
    print "------------------"
    print "starting heuristic"

    FWU = heuristic2.heuristic(newWAs, newWAm, classMat, demand , Mss)

    print "heuristic WU:"
    print FWU
    return FWU


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
    stop = 0
    for i in range(dim1[0]):
        for j in range(dim1[1]):
            for k in range(dim2[0]):
                wrasum[i, j] += newwra[i, k, j]
            for c in range(dim3[0]):
                wamc[i, j] = newwam[i, c]*classinfom[c, j]
            subgrad1[i, j] = wrasum[i, j]-wamc[i, j]
            if subgrad1[i,j]>=0:
                stop += subgrad1[i, j]
            else:
                stop -= subgrad1[i ,j]
            newlagmul1[i, j] = lagmul1[i, j]+delta*subgrad1[i, j]
            if newlagmul1[i, j] < 0:
                newlagmul1[i, j] = 0
    #print "subgrad1:"
    #print subgrad1

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
            if subgrad2[i,j]>=0:
                stop += subgrad2[i, j]
            else:
                stop -= subgrad2[i ,j]
            newlagmul2[i, j] = lagmul2[i, j]+delta*subgrad2[i, j]
            if newlagmul2[i, j] < 0:
                newlagmul2[i, j] = 0
    #print "subgrad2:"
    #print subgrad2

    oneMat = np.ones((dim2[0], dim2[1]))
    oneMinusPi = oneMat - lagmul2
    elem1 = np.sum(oneMinusPi * newwu)


    sumSmWRA = np.sum(newwra, axis=1)
    elem2 = np.sum(lagmul1 * sumSmWRA)

    sumSsWRA = np.sum(newwra, axis=0)
    elem3 = np.sum(lagmul2 * sumSsWRA)

    elem4 = np.sum(lagmul2 * np.dot(newwas, classinfom))

    elem5 = np.sum(lagmul1 * np.dot(newwam, classinfom))

    objVal= elem1 + elem2 - elem3 - elem4 - elem5
    
    print "lag obj:"
    print objVal
    
    print "stop:"
    print stop

    return [newlagmul1, newlagmul2, stop, objVal]

def main():
    solve("inputForLag.txt")

if __name__ == "__main__":
    main()
