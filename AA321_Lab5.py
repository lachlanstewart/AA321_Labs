import numpy as np
import pandas as pd
import tarfile as tf
from matplotlib import pyplot as plt

correctionMatrix = np.array([0.996207007, 0.015003149, 0.000118082,-0.001113054, 0.993660091, -2.06E-05, 0.069284612, -0.129778221, 0.994153092])
correctionMatrix = correctionMatrix.reshape(3,3)

# Data Correction
def main():
    # Open .tar files separately and use as look up files for tare data
    filePath = '.\..\Lab5_Data\Final_Data_Delivery\Raw Data\RUN_0001.eu'
    df = pd.read_fwf(filePath, skiprows=[0,1,2])
    print(df)



main()
