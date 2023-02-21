import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Global Vars
SREF = 9.375    # Area of test article in ft^2 
BREF = 90       # Wingspan in inches
MAC = 15        # Mean Aero Chord in inches

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
        CLW = dataMatrix[x,12] / (SREF * dataMatrix[x,5])
        
        tempArray[0,0] = dataMatrix[x,12] #L_R
        tempArray[1,0] = dataMatrix[x,13] #D_R
        tempArray[2,0] = dataMatrix[x,14] #PM_R

        LDP[x, [1,2,3]] = np.transpose(np.matmul(balanceMatrix,tempArray))
        
        LDP[x,1] = LDP[x,1] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tareL)
        LDP[x,2] = LDP[x,2] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tareD)
        LDP[x,3] = LDP[x,3] - dataMatrix[x,5]*np.interp(CLW,tareCLW,tarePM)
        
    return LDP

# Takes matrix of alphas, lift, drag and pitching moment (LDP) & data Matrix (with raw vals of Q)
# Returns a list of column vectors with cofficients: [alpha, CL, CD, CM]
def getCoefficients(LDP, dataMatrix):
    coeffMatrix = np.zeros((len(LDP), 4))
    coeffMatrix[:,0] = LDP[:, 0]
    Q = dataMatrix[:, 5]     # Column vector of dynamic pressures (Q)
    for i in range(len(LDP)):
        coeffMatrix[i,1] = LDP[i,1] / (Q[i] * SREF)   # CL
        coeffMatrix[i,2] = LDP[i,2] / (Q[i] * SREF)   # CD
        coeffMatrix[i,3] = LDP[i,3] / (Q[i] * SREF * MAC)   # CM
    
    return coeffMatrix

def main():
    # Retrieve Data
    run34M = pd.read_csv(r'Raw Data\RUN_0034.csv').to_numpy() # Runs without endcaps
    run35M = pd.read_csv(r'Raw Data\RUN_0035.csv').to_numpy()
    run38M = pd.read_csv(r'Raw Data\RUN_0038.csv').to_numpy() # Runs with endcaps
    run39M = pd.read_csv(r'Raw Data\RUN_0039.csv').to_numpy()
    # Retrieve KWT-corrected Data
    kwt34M = pd.read_csv(r'KWT-Corrected Data\run_0034.csv').to_numpy() # Runs without endcaps
    kwt35M = pd.read_csv(r'KWT-Corrected Data\run_0035.csv').to_numpy()
    kwt38M = pd.read_csv(r'KWT-Corrected Data\run_0038.csv').to_numpy() # Runs with endcaps
    kwt39M = pd.read_csv(r'KWT-Corrected Data\run_0039.csv').to_numpy()

    tare10q = (pd.read_csv(r'Data Correction Resources\10Q_CLW.csv')).to_numpy() 
    tare35q = (pd.read_csv(r'Data Correction Resources\35Q_CLW.csv')).to_numpy()
    
    preBalanceMatrix = pd.read_csv(r'Data Correction Resources\Balance Interaction Matrix.csv', skip_blank_lines=True, index_col=0, header=[1,2])
    
    balanceMatrix = preBalanceMatrix.to_numpy()
    
    # Execute tare function
    # LDP's are arrays organized by columns, where column 0 is AlphaENC, 1 Lift, 2 Drag, 3 PitchMoment

    LDP34 = tareData(run34M,balanceMatrix,tare10q)
    LDP35 = tareData(run35M,balanceMatrix,tare10q)
    LDP38 = tareData(run38M,balanceMatrix,tare35q)
    LDP39 = tareData(run39M,balanceMatrix,tare35q)
    
    # print(LDP38) # For Debugging, good luck m8 -- Thanks brother xD

    # Get matrices of coefficients at alpha (LDP matrix, Raw data file)
    CLDP34 = getCoefficients(LDP34, run34M)
    CLDP35 = getCoefficients(LDP35, run35M)
    CLDP38 = getCoefficients(LDP38, run38M)
    CLDP39 = getCoefficients(LDP39, run39M)
    
    # Print out the coefficients at the alpha value closest to 10deg as well as the max alpha value

    # Plotting


    plt.plot(kwt34M[:,8], CLDP34[:,1], '-k', label='C_L', linewidth='4')
    plt.plot(kwt34M[:,8], CLDP34[:,2], '-g', label='C_D', linewidth='4')
    plt.plot(kwt34M[:,8], CLDP34[:,3], '-m', label='C_M', linewidth='4')
    plt.plot(kwt34M[:,8], kwt34M[:,21], '-r', label='C_L_KWT', linewidth='4')
    plt.plot(kwt34M[:,8], kwt34M[:,22], '-b', label='C_D_KWT', linewidth='4')
    plt.plot(kwt34M[:,8], kwt34M[:,23], '-y', label='C_D_KWT', linewidth='4')
    plt.legend()
    plt.show()
main()
