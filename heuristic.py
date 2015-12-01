import numpy as np

def heuristic(Dsi, WAs, WAm, classMat):
    numIntvl = classMat.shape[1]
    WIs = np.dot(WAs, classMat) # table(row of skill s, col of intvl i)
    Psi = Dsi - WIs
    sumPsVec = [sum Psi[:, i] for i in Psi.shape[1]] # vector of length numIntvl, col sum of Psi
    WIm = np.dot(WAm, classMat) # table(row of skill s', col of intvl i)
    sumPsmVec = [sum WIm[:,i] for i in WIm.shape[1]] # vector of length numIntvl, col sum of WIm
    WU = 0

    for i in range(numIntvl):
        if sumPsVec < sumPsmVec: # infeasible
            break
        else:
            WU = sumPsVec - sumPsmVec

        






def main():
    pass

if __name__ = "__main__":
    main()
