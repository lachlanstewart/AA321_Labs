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

# aluminum beam information
alumGageFactor = 2.105
alumYoungsMod = 68.9*(10**9)

alumBeamDensityGCM3 = 2.70
alumBeamDensityKgM3 = alumBeamDensityGCM3 * 1000

alumBeamLengthCM = 63.75
alumBeamLengthM = alumBeamLengthCM / 100

alumBeamWidthMM = 25.64 # Width not provided by Ben Fetter's group so assuming the same as steel beam
alumBeamWidthM = alumBeamWidthMM / 1000

alumBeamHeightMM = 12.78 # Height not provided by Ben Fetter's group so assuming the same as steel beam
alumBeamHeightM = alumBeamHeightMM / 1000

alumBeamAreaM2 = alumBeamWidthM * alumBeamHeightM
alumBeamAreaMomentM4 = (1/12) * alumBeamWidthM * (alumBeamHeightM**3)

# recorded lab data

def voltageToStress(Vout, Vin, GageFactor, YoungsMod, voltageOffset):
    
    
    strain = 0.25 * (4/GageFactor) * (abs(voltageOffset - Vout) / Vin)
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
    
    # Theoretical Frequencies 
    omega1 = (3.516/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )

    omega2 = (22.03/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )
    
    omega3 = (61.7/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )

    omega4 = (3.516/(alumBeamLengthM**2))*\
        np.sqrt( (alumYoungsMod*alumBeamAreaMomentM4) / (alumBeamDensityKgM3 * alumBeamAreaM2) )

    omega5 = (22.03/(alumBeamLengthM**2))*\
        np.sqrt( (alumYoungsMod*alumBeamAreaMomentM4) / (alumBeamDensityKgM3 * alumBeamAreaM2) )
    
    omega6 = (61.7/(ironBeamLengthM**2))*\
        np.sqrt( (alumYoungsMod*alumBeamAreaMomentM4) / (alumBeamDensityKgM3 * alumBeamAreaM2) )
    
    print('\n Theoretical Natural Frequencies for 4140 Steel Beam')
    print(omega1 / (2*np.pi), ' Hz')
    print(omega2 / (2*np.pi), ' Hz')
    print(omega3 / (2*np.pi), ' Hz')
    
    print('\n Theoretical Natural Frequencies for 6061-T6 Aluminum Beam')
    print(omega4 / (2*np.pi), ' Hz')
    print(omega5 / (2*np.pi), ' Hz')
    print(omega6 / (2*np.pi), ' Hz')

    # Stress and Strain in Beam, Theoretical vs. Measured
    ironBeamStressTheoryLoad10lb60cm = forceToStress(10, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad20lb60cm = forceToStress(20, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad30lb60cm = forceToStress(30, 0.6, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad10lb40cm = forceToStress(10, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad20lb40cm = forceToStress(20, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    ironBeamStressTheoryLoad30lb40cm = forceToStress(30, 0.4, ironBeamHeightM, ironBeamAreaMomentM4)
    
    alumBeamStressTheoryLoad10lb60cm = forceToStress(10.15, 59.4, alumBeamHeightM, alumBeamAreaMomentM4)
    alumBeamStressTheoryLoad20lb60cm = forceToStress(20.00, 59.4, alumBeamHeightM, alumBeamAreaMomentM4)
    alumBeamStressTheoryLoad30lb60cm = forceToStress(30.00, 59.4, alumBeamHeightM, alumBeamAreaMomentM4)
    alumBeamStressTheoryLoad10lb40cm = forceToStress(9.90, 59.4,  alumBeamHeightM, alumBeamAreaMomentM4)
    alumBeamStressTheoryLoad20lb40cm = forceToStress(20.11, 59.4, alumBeamHeightM, alumBeamAreaMomentM4)
    alumBeamStressTheoryLoad30lb40cm = forceToStress(29.90, 59.4, alumBeamHeightM, alumBeamAreaMomentM4)

    print('\n Theoretical Stress Measured for 4140 Steel Beam') # 4.448 N per Pound
    print(ironBeamStressTheoryLoad10lb60cm)
    print(ironBeamStressTheoryLoad20lb60cm)
    print(ironBeamStressTheoryLoad30lb60cm)
    print(ironBeamStressTheoryLoad10lb40cm)
    print(ironBeamStressTheoryLoad20lb40cm)
    print(ironBeamStressTheoryLoad30lb40cm)
    
    print('\n Theoretical Stress Measured for 6061-T6 Aluminum Beam') # 4.448 N per Pound
    print(alumBeamStressTheoryLoad10lb60cm)
    print(alumBeamStressTheoryLoad20lb60cm)
    print(alumBeamStressTheoryLoad30lb60cm)
    print(alumBeamStressTheoryLoad10lb40cm)
    print(alumBeamStressTheoryLoad20lb40cm)
    print(alumBeamStressTheoryLoad30lb40cm)

    ironBeamStressTrueLoad10lb60cm = voltageToStress(0.018, 4.981, 2.090, ironYoungsMod, 0.020)
    ironBeamStressTrueLoad20lb60cm = voltageToStress(0.01623, 4.981, 2.090, ironYoungsMod, 0.020)
    ironBeamStressTrueLoad30lb60cm = voltageToStress(0.01436, 4.981, 2.090, ironYoungsMod, 0.020)
    ironBeamStressTrueLoad10lb40cm = voltageToStress(0.01803, 4.981, 2.090, ironYoungsMod, 0.020)
    ironBeamStressTrueLoad20lb40cm = voltageToStress(0.01780, 4.981, 2.090, ironYoungsMod, 0.020)
    ironBeamStressTrueLoad30lb40cm = voltageToStress(0.01676, 4.981, 2.090, ironYoungsMod, 0.020)
  
    alumBeamStressTrueLoad10lb60cm = voltageToStress(-0.01018, -4.981, alumGageFactor, alumYoungsMod, -0.0414)
    alumBeamStressTrueLoad20lb60cm = voltageToStress(-0.01453, -4.981, alumGageFactor, alumYoungsMod, -0.0414)
    alumBeamStressTrueLoad30lb60cm = voltageToStress(-0.02052, -4.981, alumGageFactor, alumYoungsMod, -0.0414)
    alumBeamStressTrueLoad10lb40cm = voltageToStress(-0.00767, -4.981, alumGageFactor, alumYoungsMod, -0.0414)
    alumBeamStressTrueLoad20lb40cm = voltageToStress(-0.01194, -4.981, alumGageFactor, alumYoungsMod, -0.0414)
    alumBeamStressTrueLoad30lb40cm = voltageToStress(-0.01383, -4.981, alumGageFactor, alumYoungsMod, -0.0414)

    print('\n True Stress Measured for 4140 Steel Beam')
    print(ironBeamStressTrueLoad10lb60cm)
    print(ironBeamStressTrueLoad20lb60cm)
    print(ironBeamStressTrueLoad30lb60cm)
    print(ironBeamStressTrueLoad10lb40cm)
    print(ironBeamStressTrueLoad20lb40cm)
    print(ironBeamStressTrueLoad30lb40cm)
    
    print('\n True Stress Measured for 6061-T6 Aluminum Beam')
    print(alumBeamStressTrueLoad10lb60cm)
    print(alumBeamStressTrueLoad20lb60cm)
    print(alumBeamStressTrueLoad30lb60cm)
    print(alumBeamStressTrueLoad10lb40cm)
    print(alumBeamStressTrueLoad20lb40cm)
    print(alumBeamStressTrueLoad30lb40cm)

    # Damping Coefficient
    ironBeamDampingCoefficient = amplitudeToDampingCoefficient(43.2,-372,42.0,-288)
    ironBeamFundamentalFrequency = fundamentalFrequency(-372,-288, 2)

    alumBeamDampingCoefficient = amplitudeToDampingCoefficient(22,-308,20.8,-264)
    alumBeamFundamentalFrequency = fundamentalFrequency(-308,-264, 1)

    print('\n Damping Coefficient for 4140 Steel Beam')
    print(ironBeamDampingCoefficient)
    
    print('\n Fundamental Frequency of 4140 Steel Beam')
    print(ironBeamFundamentalFrequency)
    
    print('\n Damping Coefficient for 6061-T6 Aluminum Beam')
    print(alumBeamDampingCoefficient)
    
    print('\n Fundamental Frequency of 6061-T6 Aluminum Beam')
    print(alumBeamFundamentalFrequency)
    
main()