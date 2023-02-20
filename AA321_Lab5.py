import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

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

def main():
    # Read data
    print('Main Successfully Executed')
    
    
process_data()
main()
