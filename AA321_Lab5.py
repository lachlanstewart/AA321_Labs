import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def weightBal(dataMatrix,balanceMatrix,tareMatrix):
    
    k = len(dataMatrix)
    
    LDP = np.zeros((k,4))
    LDP[:,0] = dataMatrix[:,2]
    
    tareCLW = tareMatrix[:,0]
    tareL = tareMatrix[:,1]
    tareD = tareMatrix[:,2]
    tarePM = tareMatrix[:,3]   
    
    for x in range(k):
        tempArray = np.zeros((3,1))
        CLW = dataMatrix[x,12] / (9.375 * dataMatrix[x,5])
        
        tempArray[0,0] = dataMatrix[x,12] #L_R
        tempArray[1,0] = dataMatrix[x,13] #D_R
        tempArray[2,0] = dataMatrix[x,14] #PM_R

        LDP[x, [1,2,3]] = np.transpose(np.matmul(balanceMatrix,tempArray))
        
        LDP[x,1] = LDP[x,1] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tareL)
        LDP[x,2] = LDP[x,2] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tareD)
        LDP[x,3] = LDP[x,3] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tarePM)
        
    return LDP
        
def process_data():
    # Retrieve Data
    Run35 = pd.read_csv(r'Raw Data\RUN_0035.csv', header=1)
    Run36 = pd.read_csv(r'Raw Data\RUN_0036.csv', header=1)
    Run37 = pd.read_csv(r'Raw Data\RUN_0037.csv')
    Run38 = pd.read_csv(r'Raw Data\RUN_0038.csv', header=1)
    Run39 = pd.read_csv(r'Raw Data\RUN_0039.csv', header=1)
    Run40 = pd.read_csv(r'Raw Data\RUN_0040.csv', header=1)
    
    tare10q = (pd.read_csv(r'Data Correction Resources\10Q_CLW.csv')).to_numpy()
    tare35q = (pd.read_csv(r'Data Correction Resources\35Q_CLW.csv')).to_numpy()
    
    preMatrix = pd.read_csv(r'Data Correction Resources\Balance Interaction Matrix.csv', skip_blank_lines=True, index_col=0, header=[1,2])
    balanceMatrix = preMatrix.to_numpy()
    
    
    run37M = Run37.to_numpy()
    run38M = Run38.to_numpy()
    run39M = Run39.to_numpy()
    run40M = Run40.to_numpy()
    
    LDP37 = weightBal(run37M,balanceMatrix,tare10q)
    LDP38 = weightBal(run38M,balanceMatrix,tare10q)
    LDP39 = weightBal(run39M,balanceMatrix,tare35q)
    LDP40 = weightBal(run40M,balanceMatrix,tare35q)
    print(LDP38) # for debugging

    
    # print('Balance Matrix: \n', balanceMatrix) # for debugging
    # print('\n Run 37: \n', run37M)             # for debugging
    
def main():
    # Read data
    process_data()
    print('Main Successfully Executed')
    
main()
