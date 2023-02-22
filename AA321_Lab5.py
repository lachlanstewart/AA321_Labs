import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

# Global Vars
SREF = 9.375    # Area of test article in ft^2 
BREF = 90       # Wingspan in inches
MAC = 15        # Mean Aero Chord in inches
AR = (BREF**2)/(SREF*144)
titleF = 18         # Title Font Size
axisF = 16          # Label Font Size
legendF = 16        # legend Font Size

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

# Takes a matrix of coefficients (CLDP) and prints the values at alpha
def printAlpha(CLDP, alpha):
    arg = np.argmin(abs(CLDP[:,0] - alpha))
    print('Coefficients at alpha =', alpha, 'deg: [CL CD CM]')
    print(CLDP[arg, [1, 2, 3]])
    print('Max alpha before stall:', CLDP[np.argmax(abs(CLDP[:, 1])),0])

def getPlots(CLDP, LDP, kwt, Q, title):
    a = min(len(kwt[:,8]),len(CLDP[:,1]))
    alphas = kwt[:a,8]

    # Plot CL, CD, CM together
    plt.plot(alphas, CLDP[:a,1], '-k', label='C_L', linewidth='3')
    plt.plot(alphas, CLDP[:a,2], '-g', label='C_D', linewidth='3')
    plt.plot(alphas, CLDP[:a,3], '-b', label='C_M', linewidth='3')
    plt.title(title + ' Q = ' + str(Q) + 'psf (CL, CD, CM vs Alpha)', fontname="Times New Roman", size=titleF,fontweight="bold")
    plt.xlabel('Alpha (deg)', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.ylabel('Dimensionless Coefficient', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.legend(fontsize="16")
    plt.ylim([-0.5, 1.5])
    plt.xlim([-4.1, 20.5])
    plt.grid('on')
    plt.show()

    # Plot L/D vs alphas 
    liftVsDrag = np.divide(LDP[:,1], LDP[:,2])
    plt.plot(alphas, liftVsDrag[:a], '-k', label='L/D', linewidth='4')
    plt.title(title + ' Q = ' + str(Q) + ' (L/D vs Alpha)', fontname="Times New Roman", size=titleF,fontweight="bold")
    plt.xlabel('Alpha (deg)', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.ylabel('L/D', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.legend(fontsize="16")
    plt.grid('on')
    plt.show()

    # Plot CL vs CD 
    plt.plot(CLDP[:a,2], CLDP[:a,1], '-k', label='CL', linewidth='4')
    plt.title(title + ' Q = ' + str(Q) + ' (CL vs CD)', fontname="Times New Roman", size=titleF,fontweight="bold")
    plt.xlabel('CD', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.ylabel('CL', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.legend(fontsize="16")
    plt.grid('on')
    plt.show() 

def getComp(kwt, CLDP, alpha, endcaps):
    k = min(len(kwt), len(CLDP))
    plt.plot(kwt[:k,8], CLDP[:k,1], '-k', label='C_L', linewidth='4')
    plt.plot(kwt[:k,8], CLDP[:k,2], '-r', label='C_D', linewidth='4')
    plt.plot(kwt[:k,8], CLDP[:k,3], '-c', label='C_M', linewidth='4')
    plt.plot(kwt[:k,8], kwt[:k,21], '--b', label='C_L_KWT', linewidth='3')
    plt.plot(kwt[:k,8], kwt[:k,22], '--g', label='C_D_KWT', linewidth='3')
    plt.plot(kwt[:k,8], kwt[:k,23], '--m', label='C_D_KWT', linewidth='3')
    plt.title(endcaps + ' Run Q = ' + alpha + ' psf', fontname="Times New Roman", size=titleF,fontweight="bold")
    plt.xlabel('Alpha (deg)', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.ylabel('Dimensionless Coefficient', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.xlim([-4, 20.5])
    plt.legend(fontsize="16")
    plt.grid('on')
    plt.show()

def getFiniteComp(kwt,CLDP, alpha, endcaps):
    
    k = min(len(kwt), len(CLDP))
    
    twoDslope = 0.075 # 1/deg
    twoDintercept = 0.1 # idek unit, you tell me man
    
    twoDlift = twoDslope*kwt[:k,8]+twoDintercept
    
    plt.plot(kwt[:k,8], CLDP[:k,1], '-k', label='3D C_L', linewidth='4')
    plt.plot(kwt[:k,8], twoDlift, '--b', label='2D C_L', linewidth='4')
    plt.title('3D vs 2D Airfoil: ' + endcaps + ' Run Q = ' + alpha + ' psf', fontname="Times New Roman", size=titleF,fontweight="bold")
    plt.xlabel('Alpha (deg)', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.ylabel('CL', fontname="Times New Roman", size=axisF,fontweight="bold")
    plt.xlim([-4, 15])
    plt.legend(fontsize="16")
    plt.grid('on')
    plt.show()
    
# Return Parasitic Drag and Span Efficiency Factor
def analyzeDrag(CLDP):

    # Calculate span efficiency factor 
    CL2 = np.power(CLDP[:,1],2) # Square of lift coefficients
    CD = CLDP[:,2] # Drag coefficients
    CL = CLDP[:,1] # Lift coefficients
    
    n= np.argmin(abs(CD-0.050)) # Linear region for all plots is centered around CD = 0.050
    m = np.gradient(CL2, CD)[n]
    e = m/(np.pi*AR)
    # plt.plot(CD, CL2)     # For checking the quality of slope approximation
    # plt.plot(CD, CD * m)
    # plt.show()

    result = []
    k = np.argmin(abs(CL2[:]))
    # Find index where lift coefficient = 0, then retrieve parasitic drag
    CDpara = CD[k]
    result.append(CDpara)
    result.append(e)
    return result

def main():
    # Retrieve Data
    run34M = pd.read_csv(r'Raw Data\RUN_0034.csv').to_numpy() # Runs without endcaps
    run35M = pd.read_csv(r'Raw Data\RUN_0035.csv').to_numpy()
    run38M = pd.read_csv(r'Raw Data\RUN_0038.csv').to_numpy()[1:] # Runs with endcaps   
    run39M = pd.read_csv(r'Raw Data\RUN_0039.csv').to_numpy()     # Note : Run 38 has an abnormal first data point so it is omitted
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
    LDP38 = tareData(run38M,balanceMatrix,tare35q)[1:]
    LDP39 = tareData(run39M,balanceMatrix,tare35q)

    # Get matrices of coefficients at alpha (LDP matrix, Raw data file)
    CLDP34 = getCoefficients(LDP34, run34M)
    CLDP35 = getCoefficients(LDP35, run35M)
    CLDP38 = getCoefficients(LDP38, run38M)
    CLDP39 = getCoefficients(LDP39, run39M)
    
    # Print out the coefficients at the alpha value closest to 10deg as well as the max alpha value
    printAlpha(CLDP34, 10)

    # Create plots for each dataset
    getPlots(CLDP34, LDP34, kwt34M, 10, 'Baseline Run')
    getPlots(CLDP35, LDP35, kwt35M, 35, 'Baseline Run')
    getPlots(CLDP38, LDP38, kwt38M, 10, 'Endcaps Run')
    getPlots(CLDP39, LDP39, kwt39M, 35, 'Endcaps Run')

    # Calculate Parasitic Drag and Oswald Efficiency Factor
    [CDp34, o34] = analyzeDrag(CLDP34)
    [CDp34k, o34k] = analyzeDrag(kwt34M[:,20:24])
    print('Run 34 (our data): CDp = ', CDp34, ' e = ', o34)
    print('Run 34 (KWT data): CDp = ', CDp34k, ' e = ', o34k)
    [CDp35, o35] = analyzeDrag(CLDP35)
    [CDp35k, o35k] = analyzeDrag(kwt35M[:,20:24])
    print('Run 35 (our data): CDp = ', CDp35, ' e = ', o35)
    print('Run 35 (KWT data): CDp = ', CDp35k, ' e = ', o35k)
    [CDp38, o38] = analyzeDrag(CLDP38)
    [CDp38k, o38k] = analyzeDrag(kwt38M[:,20:24])
    print('Run 38 (our data): CDp = ', CDp38, ' e = ', o38)
    print('Run 38 (KWT data): CDp = ', CDp38k, ' e = ', o38k)
    [CDp39, o39] = analyzeDrag(CLDP39)
    [CDp39k, o39k] = analyzeDrag(kwt39M[:,20:24])
    print('Run 39 (our data): CDp = ', CDp39, ' e = ', o39)
    print('Run 39 (KWT data): CDp = ', CDp39k, ' e = ', o39k)

    # Comparison of KWT vs corrected
    getComp(kwt34M, CLDP34, '10', 'Baseline')
    getComp(kwt35M, CLDP35, '35', 'Baseline')
    getComp(kwt38M, CLDP38, '10', 'Endcaps')
    getComp(kwt39M, CLDP39, '35', 'Endcaps')
    
    getFiniteComp(kwt35M, CLDP35, '35', 'Baseline')
    getFiniteComp(kwt39M, CLDP39, '35', 'Endcaps')
main()
