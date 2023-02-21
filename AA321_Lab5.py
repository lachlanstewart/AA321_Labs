import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

<<<<<<< Updated upstream
def process_data():
    # Retrieve Data
    Run35 = pd.read_csv('Raw Data\RUN_0035.csv')
    Run36 = pd.read_csv('Raw Data\RUN_0036.csv')
    Run37 = pd.read_csv('Raw Data\RUN_0037.csv')
    Run38 = pd.read_csv('Raw Data\RUN_0038.csv')
    Run39 = pd.read_csv('Raw Data\RUN_0039.csv')
    Run40 = pd.read_csv('Raw Data\RUN_0040.csv')
    
    preMatrix = pd.read_csv('Data Correction Resources\Balance Interaction Matrix.csv', skip_blank_lines=True, index_col=0, header=[1,2])
    balanceMatrix = preMatrix.to_numpy()
    
    print(balanceMatrix)

=======
<<<<<<< Updated upstream
=======
def weightBal(input1,input2): # Inputs (1) array from RUN and (2) Balance Array and alters (1).
    
    
    k = len(input1)
    
    
    for x in range(k):
        tempArray = np.zeros((3,1))
        LDP = np.zeros((3,1))
        tempArray[0,0] = input1[x,12] #L_R
        tempArray[1,0] = input1[x,13] #D_R
        tempArray[2,0] = input1[x,14] #PM_R

        LDP = np.matmul(input2,tempArray)
        
        input1[x,12] = LDP[0,0]
        input1[x,13] = LDP[1,0]
        input1[x,14] = LDP[2,0]
        
def process_data():
    # Retrieve Data
    Run35 = pd.read_csv(r'Raw Data\RUN_0035.csv', header=1)
    Run36 = pd.read_csv(r'Raw Data\RUN_0036.csv', header=1)
    Run37 = pd.read_csv(r'Raw Data\RUN_0037.csv')
    Run38 = pd.read_csv(r'Raw Data\RUN_0038.csv', header=1)
    Run39 = pd.read_csv(r'Raw Data\RUN_0039.csv', header=1)
    Run40 = pd.read_csv(r'Raw Data\RUN_0040.csv', header=1)
    
    tare10q = pd.read_csv(r'Data Correction Resources\10Q_CLW.csv')
    tare35q = pd.read_csv(r'Data Correction Resources\35Q_CLW.csv')
    
    preMatrix = pd.read_csv(r'Data Correction Resources\Balance Interaction Matrix.csv', skip_blank_lines=True, index_col=0, header=[1,2])
    balanceMatrix = preMatrix.to_numpy()
    
    
    run37M = Run37.to_numpy()
    run38M = Run38.to_numpy()
    run39M = Run39.to_numpy()
    run40M = Run40.to_numpy()
    
    #print('Pre Matrix: \n',run37M) # For Debugging, before changes
    weightBal(run37M,balanceMatrix)
    #print('Post Matrix: \n',run37M) # For Debugging, after changes
    weightBal(run38M,balanceMatrix)
    weightBal(run39M,balanceMatrix)
    weightBal(run40M,balanceMatrix)

    
    # print('Balance Matrix: \n', balanceMatrix) # for debugging
    # print('\n Run 37: \n', run37M)             # for debugging

>>>>>>> Stashed changes
>>>>>>> Stashed changes
def main():
    # Read data
    print('Main Successfully Executed')
    
    
process_data()
main()
