import numpy as np

with open('inputForLag.txt', 'r') as f:
    lines = f.readlines()

for i in range(len(lines)):
    lines[i] = lines[i][:-1]

numIntvl = int(lines[0])
numS = int(lines[2])
numM = int(lines[4])
numC = int(lines[6])

demand = np.zeros([numS, numIntvl])
for i in range(numS):
    line = lines[8+i]
    line = map(int, line.split(' '))
    demand[i] = line

classMat = np.zeros([numC, numIntvl])
for i in range(numC):
    line = lines[9+numS+i]
    line = map(int, line.split(' '))
    classMat[i] = line

Mss = np.zeros([numM, numS])
for i in range(numM):
    line = lines[10+numS+numC+i]
    line = map(int, line.split(' '))
    Mss[i] = line

WSs = map(int, lines[11+numS+numC+numM].split(' '))

WSm = map(int, lines[13+numS+numC+numM].split(' '))


