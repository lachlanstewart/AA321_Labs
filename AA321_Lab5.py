import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def tareData(dataMatrix,balanceMatrix,tareMatrix):
    
    k = len(dataMatrix)
    
    # LDP is matrix with Columns of: AlphaENC, Lift, Drag, PitchMoment
    LDP = np.zeros((k,4))
    LDP[:,0] = dataMatrix[:,2] #AlphaENC Column filled
    
    # Columns from tare reference table to be used by np.interp()
    tareCLW = tareMatrix[:,0]
    tareL = tareMatrix[:,1]
    tareD = tareMatrix[:,2]
    tarePM = tareMatrix[:,3]   
    
    # For every row of data, adjust L,D,PM for weight and fill to LDP, then subtract strut interference
    # Note that Strut Interference is semi-normalized, dataMatrix[x,5] is Q_Actual
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

    
def main():
    # Retrieve Data
    Run35 = pd.read_csv(r'Raw Data\RUN_0035.csv')
    Run36 = pd.read_csv(r'Raw Data\RUN_0036.csv')
    Run37 = pd.read_csv(r'Raw Data\RUN_0037.csv')
    Run38 = pd.read_csv(r'Raw Data\RUN_0038.csv')
    Run39 = pd.read_csv(r'Raw Data\RUN_0039.csv')
    Run40 = pd.read_csv(r'Raw Data\RUN_0040.csv')
    
    tare10q = (pd.read_csv(r'Data Correction Resources\10Q_CLW.csv')).to_numpy() # I figured out I can to_numpy in same line. Too lazy to retroactively fix others
    tare35q = (pd.read_csv(r'Data Correction Resources\35Q_CLW.csv')).to_numpy()
    
    preBalanceMatrix = pd.read_csv(r'Data Correction Resources\Balance Interaction Matrix.csv', skip_blank_lines=True, index_col=0, header=[1,2])
    
    balanceMatrix = preBalanceMatrix.to_numpy()
    run37M = Run37.to_numpy()
    run38M = Run38.to_numpy()
    run39M = Run39.to_numpy()
    run40M = Run40.to_numpy()
    
    # Execute tare function
    # LDP's are arrays organized by columns, where column 0 is AlphaENC, 1 Lift, 2 Drag, 3 PitchMoment
    LDP37 = tareData(run37M,balanceMatrix,tare10q)
    LDP38 = tareData(run38M,balanceMatrix,tare10q)
    LDP39 = tareData(run39M,balanceMatrix,tare35q)
    LDP40 = tareData(run40M,balanceMatrix,tare35q)
    
    #print(LDP38) # For Debugging, good luck m8
    
    print('Main Successfully Executed')
    
main()
