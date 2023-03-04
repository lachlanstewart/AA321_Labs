import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dataProcess(rawArray,diameterIn): #OUTPUT: thrust, torque, Ct, Cq, Power, Advance Ratio
    
    revFreq = rawArray[:,1] / 60
    densitylbin3 = 1.3756*(10**(-6))
    densityslugft3 = 0.002377
    
    postProcessArray = np.zeros( (len(rawArray[:,0]), 6) )
    postProcessArray[:,0] = -(rawArray[:,3] - (0.0147*rawArray[:,2] - 0.03 ))
    postProcessArray[:,1] = -(rawArray[:,4] - (0.0024*rawArray[:,2] - 0.014))
    postProcessArray[:,2] = np.divide(postProcessArray[:,0], (densitylbin3 * revFreq[:]**2 * diameterIn**4) )
    postProcessArray[:,3] = np.divide(postProcessArray[:,1], (densitylbin3 * revFreq[:]**2 * diameterIn**5) )
    postProcessArray[:,4] = 2 * np.pi * postProcessArray[:,3]
    postProcessArray[:,5] = 12 * np.sqrt(2 * rawArray[:,2] / densityslugft3) / (revFreq[:] * diameterIn)
    
    return(postProcessArray)

def main():
    print('Hello Lachlan')
    
    #propArray12x14at0 = pd.read_csv(r'Lab 7\Data\12x14_0psf.csv').to_numpy()
    propArray12x14at8 = pd.read_csv(r'Lab 7\Data\12x14_8psf.csv').to_numpy()
    propArray12x14at12 = pd.read_csv(r'Lab 7\Data\12x14_12psf.csv').to_numpy()
    
    #propArray12x10at0 = pd.read_csv(r'Lab 7\Data\12x10_0psf.csv').to_numpy()
    propArray12x10at9 = pd.read_csv(r'Lab 7\Data\12x10_9psf.csv').to_numpy()
    propArray12x10at12 = pd.read_csv(r'Lab 7\Data\12x10_12psf.csv').to_numpy()
    
    #propArrayProcessed12x14at0 = dataProcess(propArray12x14at0,12)
    propArrayProcessed12x14at8 = dataProcess(propArray12x14at8,12)
    propArrayProcessed12x14at12 = dataProcess(propArray12x14at12,12)
    
    #propArrayProcessed12x10at0 = dataProcess(propArray12x10at0,12)
    propArrayProcessed12x10at9 = dataProcess(propArray12x10at9,12)
    propArrayProcessed12x10at12 = dataProcess(propArray12x10at12,12)
    
    print(propArrayProcessed12x10at9)
    
    plt.figure(1)
    plt.plot(propArrayProcessed12x14at8[:,5],propArrayProcessed12x14at8[:,3])
    plt.show()
    
main()