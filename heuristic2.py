import numpy as np

def heuristic(WAs, WAm, classMat, Dsi, Mss):
    numS = WAs.shape[0]
    numM = WAm.shape[0]
    numIntvl = classMat.shape[1]
    WIs = np.dot(WAs, classMat) # table(row of skill s, col of intvl i)
    Psi = Dsi - WIs
    sumPsVec = [sum(Psi[:,i]) for i in range(Psi.shape[1])] # vector of length numIntvl, col sum of Psi
    WIm = np.dot(WAm, classMat) # table(row of skill s', col of intvl i)
    sumPsmVec = [sum(WIm[:,i]) for i in range(WIm.shape[1])] # vector of length numIntvl, col sum of WIm
    
    Psi = [ map(lambda x: 0 if x<0 else x, xs) for xs in Psi ]
    Psi = np.array(Psi).reshape(numS, numIntvl)
    for i in range(numIntvl):
        for s in range(numS):
            for m in range(numM):
                if Psi[s,i]>0:
                    if Mss[m,s]==1:
                        Psi[s,i]-= WIm[m,s]
                        WIm[m,s]=0
                        if Psi[s,i]< 0:
                            WIm[m,s]=-Psi[s,i]
                            Psi[s,i]=0
                        else:
                            break
    result = 0
    for i in range(numIntvl):
        for s in range(numS):
            result += Psi[s,i]
    return result


def main():
    WAs = np.random.randint(10, size=10*1000).reshape(10,1000)
    WAm = np.random.randint(10, size=50*1000).reshape(50,1000)
    classMat = np.random.randint(2, size=1000*672).reshape(1000,672)
    Dsi = np.random.randint(20000, size=10*672).reshape(10, 672)
    Mss = np.random.randint(2, size=50*10).reshape(50,10)

    heuristic(WAs, WAm, classMat, Dsi, Mss)
    


if __name__ == "__main__":
    main()
