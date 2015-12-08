import numpy as np

def heuristic(Dsi, WAs, WAm, classMat, CAs, CAm): # matrix of dim(numS, numC), class available for each skill 
    numS = WAs.shape[0]
    numM = WAm.shape[0]
    numIntvl = WAs.shape[1]
    WIs = np.dot(WAs, classMat) # table(row of skill s, col of intvl i)
    Psi = Dsi - WIs
    for s in range(numS):
        for i in range(numIntvl):
            while Psi[s,i] < 0:
                hasMoved = False
                for co in range(numC):
                    if CAs[s,co] == 1 && classMat[co,i] == 1:
                        for ci in range(numC):
                            if CAs[s,ci] == 1 && classMat[ci,i] == 0:
                                WAs[s,co] -= 1
                                WAs[s,ci] += 1
                                hasMoved = True
                                for k in range(numIntvl):
                                    if classMat[co,k] == 1:
                                        Psi[s,k] += 1
                                    if classMat[ci,k] == 1:
                                        Psi[s,k] -= 1
                                for t in range(i):
                                    if Psi[s,t] < 0:
                                        for k in range(numIntvl):
                                            if classMat[co,k] == 1:
                                                Psi[s,k] -= 1
                                            if classMat[ci,k] == 1:
                                                Psi[s,k] += 1
                                        hasMoved = False
                            if hasMoved == True:           
                                break
                    if hasMoved == True:
                        break
                if hasMoved == False:
                    Psi[s,i] = 0
   
    # sumPsVec = [sum Psi[:, i] for i in Psi.shape[1]] # vector of length numIntvl, col sum of Psi
    # WIm = np.dot(WAm, classMat) # table(row of skill s', col of intvl i)
    # sumPsmVec = [sum WIm[:,i] for i in WIm.shape[1]] # vector of length numIntvl, col sum of WIm
    # WU = 0

    # for i in range(numIntvl):
        # if sumPsVec < sumPsmVec: # infeasible
            # break
        # else:
            # WU = sumPsVec - sumPsmVec

        






def main():
    pass

if __name__ = "__main__":
    main()
