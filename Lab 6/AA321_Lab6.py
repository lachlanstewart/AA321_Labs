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
    stress = (YoungsMod * strain) / 10**3
    
    #Outputs in kPa
    return stress
    

def main():
    print('Hi Ian')
    
    # Theoretical Frequencies (off by 1 order of magnitude?)
    omega1 = (3.516/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )

    omega2 = (22.03/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )
    
    omega3 = (61.7/(ironBeamLengthM**2))*\
        np.sqrt( (ironYoungsMod*ironBeamAreaMomentM4) / (ironBeamDensityKgM3 * ironBeamAreaM2) )
    
    print('Theoretical Natural Frequencies for 4140 Steel Beam')
    print(omega1 / (2*np.pi), ' Hz')
    print(omega2 / (2*np.pi), ' Hz')
    print(omega3 / (2*np.pi), ' Hz')
    
    # Stress and Strain in Beam, Theoretical vs. Measured
    ironBeamStressTheoryLoad10 = (10 * 4.448) / (ironBeamAreaM2 * 10**3) #Outputs kPa
    ironBeamStressTheoryLoad20 = (20 * 4.448) / (ironBeamAreaM2 * 10**3)
    ironBeamStressTheoryLoad30 = (30 * 4.448) / (ironBeamAreaM2 * 10**3)
    print('Theoretical Stress Measured for 4140 Steel Beam') # 4.448 N per Pound
    print(ironBeamStressTheoryLoad10)
    print(ironBeamStressTheoryLoad20)
    print(ironBeamStressTheoryLoad30)
    
    ironBeamStressTrueLoad10 = voltageToStress(0.018, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad20 = voltageToStress(0.01623, 4.981, 2.090, ironYoungsMod)
    ironBeamStressTrueLoad30 = voltageToStress(0.01436, 4.981, 2.090, ironYoungsMod)
    
    print('True Stress Measured for 4140 Steel Beam')
    print(ironBeamStressTrueLoad10)
    print(ironBeamStressTrueLoad20)
    print(ironBeamStressTrueLoad30)
    
    
main()