import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

### TO DO ###
# Stress for theoretical and true are orders of magnitude off. Not sure what's going on there.




# GLOBAL VARIABLES #

# iron beam information
ironYoungsMod = 200*(10**9)

ironBeamDensityGCM3 = 7.85
ironBeamDensityKgM3 = ironBeamDensityGCM3 * 1000

ironBeamLengthCM = 63.5
ironBeamLengthM = ironBeamLengthCM / 100

ironBeamWidthMM = 25.3
ironBeamWidthM = ironBeamWidthMM / 1000

ironBeamHeightMM = 12.69
ironBeamHeightM = ironBeamHeightMM / 1000

ironBeamAreaM2 = ironBeamWidthM * ironBeamHeightM
ironBeamAreaMomentM4 = (1/12) * ironBeamWidthM * (ironBeamHeightM**3)

# recorded lab data

def voltageToStress(Vout, Vin, GageFactor, YoungsMod):
    
    
    strain = 0.25 * (4/GageFactor) * (abs(0.020 - Vout) / Vin)
    stressMPa = (YoungsMod * strain) / 10**6 # outputs MPa
    
    #Outputs in MPa
    return stressMPa

def forceToStress(forceLB,distanceM,heightM,areaMomentofInertiaM4):
    
    forceN = forceLB * 4.448
    
    stressMPa = (forceN * distanceM) * (heightM / 2) / (areaMomentofInertiaM4 * 10**6) #10^6 for kPa conversion
    
    return stressMPa 

def amplitudeToDampingCoefficient(amplitude1V, time1ms, amplitude2V, time2ms):
    
    C = np.log( (amplitude1V/amplitude2V)/ (abs(time2ms-time1ms)/1000) )
    
    return(C)

def fundamentalFrequency(time1ms, time2ms, cycles):
    
    periodS = abs(time1ms - time2ms) / (1000 * cycles)
    
    freq = 1/periodS
    
    return(freq)

def main():
    print('Hi Ian')
    
    # Theoretical Frequencies (off by 1 order of magnitude?)
    omega1 = (3.516/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )

    omega2 = (22.03/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )
    
    omega3 = (61.7/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )
    
    print('\n Theoretical Natural Frequencies for 4140 Steel Beam')
    print(omega1 / (2*np.pi), ' Hz')
    print(omega2 / (2*np.pi), ' Hz')
    print(omega3 / (2*np.pi), ' Hz')
    
    # Stress and Strain in Beam, Theoretical vs. Measured
    ironBeamStressTheoryLoad10lb60cm = forceToStress(10, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad20lb60cm = forceToStress(20, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad30lb60cm = forceToStress(30, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad10lb40cm = forceToStress(10, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad20lb40cm = forceToStress(20, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad30lb40cm = forceToStress(30, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    
    print('\n Theoretical Stress Measured for 4140 Steel Beam') # 4.448 N per Pound
    print(ironBeamStressTheoryLoad10lb60cm)
    print(ironBeamStressTheoryLoad20lb60cm)
    print(ironBeamStressTheoryLoad30lb60cm)
    print(ironBeamStressTheoryLoad10lb40cm)
    print(ironBeamStressTheoryLoad20lb40cm)
    print(ironBeamStressTheoryLoad30lb40cm)
    
    ironBeamStressTrueLoad10lb60cm = voltageToStress(0.018, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad20lb60cm = voltageToStress(0.01623, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad30lb60cm = voltageToStress(0.01436, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad10lb40cm = voltageToStress(0.01803, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad20lb40cm = voltageToStress(0.01780, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad30lb40cm = voltageToStress(0.01676, 4.981, 2.090, ironYoungsMod)
    
    print('\n True Stress Measured for 4140 Steel Beam')
    print(ironBeamStressTrueLoad10lb60cm)
    print(ironBeamStressTrueLoad20lb60cm)
    print(ironBeamStressTrueLoad30lb60cm)
    print(ironBeamStressTrueLoad10lb40cm)
    print(ironBeamStressTrueLoad20lb40cm)
    print(ironBeamStressTrueLoad30lb40cm)
    
    # Damping Coefficient
    ironBeamDampingCoefficient = amplitudeToDampingCoefficient(43.2,-372,42.0,-288)
    ironBeamFundamentalFrequency = fundamentalFrequency(-372,-288, 2)
    
    print('\n Damping Coefficient for 4140 Steel Beam')
    print(ironBeamDampingCoefficient)
    
    print('\n Fundamental Frequency of 4140 Steel Beam')
    print(ironBeamFundamentalFrequency)

main()