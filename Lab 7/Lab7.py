import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def dataProcess(rawArray,diameterIn): #OUTPUT: thrust, torque, Ct, Cq, Cp, Prop Efficiency, Advance Ratio
    
    revFreq = rawArray[:,1] / (60)
    densityslugft3 = 0.002377
    densityslugin3 = densityslugft3 * (1/12)**3
    
    postProcessArray = np.zeros( (len(rawArray[:,0]), 7) )
    postProcessArray[:,0] = (rawArray[:,3] - (0.0147*rawArray[:,2] - 0.03 ))
    postProcessArray[:,1] = (rawArray[:,4] - (0.0024*rawArray[:,2] - 0.014))
    postProcessArray[:,2] = postProcessArray[:,0] / (densityslugin3 * revFreq[:]**2 * diameterIn**4)
    postProcessArray[:,3] = postProcessArray[:,1] / (densityslugin3 * revFreq[:]**2 * diameterIn**5)
    postProcessArray[:,4] = 2 * np.pi * postProcessArray[:,3]
    postProcessArray[:,6] = 12 * np.sqrt(2 * rawArray[:,2] / densityslugft3) / (revFreq[:] * diameterIn)
    #postProcessArray[:,6] = np.sqrt(rawArray[:,2]) / (revFreq[:] * diameterIn)
    postProcessArray[:,5] = (postProcessArray[:,2] / postProcessArray[:,3]) * (postProcessArray[:,6] / (2 * np.pi) )
    
    index = []
    for i in range(len(postProcessArray[:,0])):
        if postProcessArray[i,5] < 0:
            index.append(i)
        elif postProcessArray[i,5] > 1:
            index.append(i)
            
    postProcessArray = np.delete(postProcessArray, index, axis=0)
    postProcessArray = postProcessArray[~np.isnan(postProcessArray).any(axis=1)] #a[~np.isnan(a).any(axis=1)]
        
    return(postProcessArray)

def arrayCombineAndSort(Array1,Array2,Array3):
    
    combinedArray = np.concatenate( (Array1, Array2, Array3), axis=0)
    combinedArray = combinedArray[combinedArray[:,6].argsort()]
    
    
    
    return(combinedArray)

def arrayCombineAndSortAndFit(Array1,Array2,Array3): # Outputs polynomial fit of CT, CQ, CP, n versus J as [CT, CQ, CP, n, J]
        
    combinedArray = np.concatenate( (Array1, Array2, Array3), axis=0)
    combinedArray = combinedArray[combinedArray[:,6].argsort()]
    
    newArray = np.zeros( (len(combinedArray), 5) )
    newArray[:,0] = np.polyval(np.polyfit(combinedArray[:,6],combinedArray[:,2],2), combinedArray[:,6])
    newArray[:,1] = np.polyval(np.polyfit(combinedArray[:,6],combinedArray[:,3],2), combinedArray[:,6])
    newArray[:,2] = np.polyval(np.polyfit(combinedArray[:,6],combinedArray[:,4],2), combinedArray[:,6])
    newArray[:,3] = np.polyval(np.polyfit(combinedArray[:,6],combinedArray[:,5],2), combinedArray[:,6])
    newArray[:,4] = combinedArray[:,6]
    
    return(newArray)

def main():
    print('Hello Lachlan')
    
    # READ CSV
    #propArray12x14at0 = pd.read_csv(r'Lab 7\Data\12x14_0psf.csv').to_numpy()
    propArray12x14at4 = pd.read_csv(r'Lab 7\Data\12x14_4psf_blownfuse.csv').to_numpy()
    propArray12x14at8 = pd.read_csv(r'Lab 7\Data\12x14_8psf.csv').to_numpy()
    propArray12x14at12 = pd.read_csv(r'Lab 7\Data\12x14_12psf.csv').to_numpy()
    
    #propArray12x10at0 = pd.read_csv(r'Lab 7\Data\12x10_0psf.csv').to_numpy()
    propArray12x10at4 = pd.read_csv(r'Lab 7\Data\12x10_4psf.csv').to_numpy()
    propArray12x10at9 = pd.read_csv(r'Lab 7\Data\12x10_9psf.csv').to_numpy()
    propArray12x10at12 = pd.read_csv(r'Lab 7\Data\12x10_12psf.csv').to_numpy()
    
    #propArray5x8at0_3 = pd.read_csv(r'Lab 7\Data\10_5x8_3blade_0psf.csv').to_numpy()
    propArray5x8at4_3 = pd.read_csv(r'Lab 7\Data\10_5x8_3blade_4psf.csv').to_numpy()
    propArray5x8at8_3 = pd.read_csv(r'Lab 7\Data\10_5x8_3blade_8psf.csv').to_numpy()
    propArray5x8at12_3 = pd.read_csv(r'Lab 7\Data\10_5x8_3blade_12psf.csv').to_numpy()
    
    #propArray5x8at0_4 = pd.read_csv(r'Lab 7\Data\10_5x8_4blade_0psf.csv').to_numpy()
    propArray5x8at4_4 = pd.read_csv(r'Lab 7\Data\10_5x8_4blade_4psf.csv').to_numpy()
    propArray5x8at8_4 = pd.read_csv(r'Lab 7\Data\10_5x8_4blade_8psf.csv').to_numpy()
    propArray5x8at12_4 = pd.read_csv(r'Lab 7\Data\10_5x8_4blade_12psf.csv').to_numpy()
    
    # PROCESS ARRAYS
    #propArrayProcessed12x14at0 = dataProcess(propArray12x14at0,12)
    propArrayProcessed12x14at4 = dataProcess(propArray12x14at4,12)
    propArrayProcessed12x14at8 = dataProcess(propArray12x14at8,12)
    propArrayProcessed12x14at12 = dataProcess(propArray12x14at12,12)
    
    #propArrayProcessed12x10at0 = dataProcess(propArray12x10at0,12)
    propArrayProcessed12x10at4 = dataProcess(propArray12x10at4,12)
    propArrayProcessed12x10at9 = dataProcess(propArray12x10at9,12)
    propArrayProcessed12x10at12 = dataProcess(propArray12x10at12,12)
    
    #propArrayProcessed5x8at0_3 = dataProcess(propArray5x8at0_3,5)
    propArrayProcessed5x8at4_3 = dataProcess(propArray5x8at4_3,5)
    propArrayProcessed5x8at8_3 = dataProcess(propArray5x8at8_3,5)
    propArrayProcessed5x8at12_3 = dataProcess(propArray5x8at12_3,5)
    
    #propArrayProcessed5x8at0_4 = dataProcess(propArray5x8at0_4,5)
    propArrayProcessed5x8at4_4 = dataProcess(propArray5x8at4_4,5)
    propArrayProcessed5x8at8_4 = dataProcess(propArray5x8at8_4,5)
    propArrayProcessed5x8at12_4 = dataProcess(propArray5x8at12_4,5)
    
    prop12x14 = arrayCombineAndSort(propArrayProcessed12x14at4, propArrayProcessed12x14at8, propArrayProcessed12x14at12)
    np.savetxt('test1.csv', prop12x14, delimiter=',')
    
    prop12x10raw = arrayCombineAndSort(propArrayProcessed12x10at4,propArrayProcessed12x10at9,propArrayProcessed12x10at12)
    prop12x14raw = arrayCombineAndSort(propArrayProcessed12x14at4,propArrayProcessed12x14at8,propArrayProcessed12x14at12)
    prop12x10 = arrayCombineAndSortAndFit(propArrayProcessed12x10at4,propArrayProcessed12x10at9,propArrayProcessed12x10at12)
    prop12x14 = arrayCombineAndSortAndFit(propArrayProcessed12x14at4, propArrayProcessed12x14at8, propArrayProcessed12x14at12)
    prop5x8_3 = arrayCombineAndSortAndFit(propArrayProcessed5x8at4_3, propArrayProcessed5x8at8_3, propArrayProcessed5x8at12_3)
    prop5x8_4 = arrayCombineAndSortAndFit(propArrayProcessed5x8at4_4, propArrayProcessed5x8at8_4, propArrayProcessed5x8at12_4)
    
    np.savetxt('test1.csv', prop12x14, delimiter=',')
    np.savetxt('test2.csv', propArrayProcessed12x14at8, delimiter=',')
    
    plt.style.use('seaborn-v0_8-deep')
    
    P = 1
    L = 2
    
    plt.figure(P)
    plt.title("CT versus J")
    plt.plot(propArrayProcessed12x14at8[:,6],propArrayProcessed12x14at8[:,2], linewidth=L, label="12x14")
    plt.plot(propArrayProcessed12x10at9[:,6],propArrayProcessed12x10at9[:,2], linewidth=L, label="12x10")
    plt.plot(propArrayProcessed5x8at8_3[:,6],propArrayProcessed5x8at8_3[:,2], linewidth=L, label="5x8, 3 Blade")
    plt.plot(propArrayProcessed5x8at8_4[:,6],propArrayProcessed5x8at8_4[:,2], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("CQ versus J")
    plt.plot(propArrayProcessed12x14at8[:,6],propArrayProcessed12x14at8[:,3], linewidth=L, label="12x14")
    plt.plot(propArrayProcessed12x10at9[:,6],propArrayProcessed12x10at9[:,3], linewidth=L, label="12x10")
    plt.plot(propArrayProcessed5x8at8_3[:,6],propArrayProcessed5x8at8_3[:,3], linewidth=L, label="5x8, 3 Blade")
    plt.plot(propArrayProcessed5x8at8_4[:,6],propArrayProcessed5x8at8_4[:,3], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("CP versus J")
    plt.plot(propArrayProcessed12x14at8[:,6],propArrayProcessed12x14at8[:,4], linewidth=L, label="12x14")
    plt.plot(propArrayProcessed12x10at9[:,6],propArrayProcessed12x10at9[:,4], linewidth=L, label="12x10")
    plt.plot(propArrayProcessed5x8at8_3[:,6],propArrayProcessed5x8at8_3[:,4], linewidth=L, label="5x8, 3 Blade")
    plt.plot(propArrayProcessed5x8at8_4[:,6],propArrayProcessed5x8at8_4[:,4], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("n versus J")
    #plt.plot(propArrayProcessed12x14at8[:,6],propArrayProcessed12x14at8[:,5], label="12x14")
    plt.plot(propArrayProcessed12x14at8[:,6],propArrayProcessed12x14at8[:,5], linewidth=L, label="12x14")
    plt.plot(propArrayProcessed12x10at9[:,6],propArrayProcessed12x10at9[:,5], linewidth=L, label="12x10")
    plt.plot(propArrayProcessed5x8at8_3[:,6],propArrayProcessed5x8at8_3[:,5], linewidth=L, label="5x8, 3 Blade")
    plt.plot(propArrayProcessed5x8at8_4[:,6],propArrayProcessed5x8at8_4[:,5], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.ylim(0,1)
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("Thrust Coefficient versus Advance Ratio")
    plt.ylabel("CT")
    plt.xlabel("J")
    plt.plot(prop12x14[:,4],prop12x14[:,0], linewidth=L, label="12x14")
    plt.plot(prop12x10[:,4],prop12x10[:,0], linewidth=L, label="12x10")
    plt.plot(prop5x8_3[:,4],prop5x8_3[:,0], linewidth=L, label="5x8, 3 Blade")
    plt.plot(prop5x8_4[:,4],prop5x8_4[:,0], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("Torque Coefficient versus Advance Ratio")
    plt.ylabel("CQ")
    plt.xlabel("J")
    plt.plot(prop12x14[:,4],prop12x14[:,1], linewidth=L, label="12x14")
    plt.plot(prop12x10[:,4],prop12x10[:,1], linewidth=L, label="12x10")
    plt.plot(prop5x8_3[:,4],prop5x8_3[:,1], linewidth=L, label="5x8, 3 Blade")
    plt.plot(prop5x8_4[:,4],prop5x8_4[:,1], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("Power Coefficient versus Advance Ratio")
    plt.ylabel("CP")
    plt.xlabel("J")
    plt.plot(prop12x14[:,4],prop12x14[:,2], linewidth=L, label="12x14")
    plt.plot(prop12x10[:,4],prop12x10[:,2], linewidth=L, label="12x10")
    plt.plot(prop5x8_3[:,4],prop5x8_3[:,2], linewidth=L, label="5x8, 3 Blade")
    plt.plot(prop5x8_4[:,4],prop5x8_4[:,2], linewidth=L, label="5x8, 4 Blade")
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("Propeller Efficiency versus Advance Ratio")
    plt.ylabel("n")
    plt.xlabel("J")
    plt.plot(prop12x14[:,4],prop12x14[:,3], linewidth=L, label="12x14")
    plt.plot(prop12x10[:,4],prop12x10[:,3], linewidth=L, label="12x10")
    #plt.plot(prop12x10[:,6],prop12x10[:,5], label="12x10")
    plt.plot(prop5x8_3[:,4],prop5x8_3[:,3], linewidth=L, label="5x8, 3 Blade")
    plt.plot(prop5x8_4[:,4],prop5x8_4[:,3], linewidth=L, label="5x8, 4 Blade")
    plt.ylim(0,1)
    plt.grid()
    plt.legend()
    P = P+1
    
    plt.figure(P)
    plt.title("Raw Data Versus Curve Fit for 12x10 Propeller")
    plt.plot(prop12x10raw[:,6],prop12x10raw[:,5], linestyle="", marker="o", label="12x10 Raw")
    plt.plot(prop12x10[:,4],prop12x10[:,3], linewidth=(L*2), label="12x10 Curve")
    plt.ylim(0,1)
    plt.grid()
    plt.legend()
    P = P+1
    
    
    plt.show()
    
main()