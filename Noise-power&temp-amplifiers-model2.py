#!/usr/bin/env python
# coding: utf-8

# In[7]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.constants import *


# 
# """"The program provides the total noise temperature and total noise power of circuit and its components. This is obtained by providing the voltage-rms of resistor and each amplifier, gains from each amplifier and the frequency, bandwidth and resistance of the circuit. 
# 
# The difference between the model1 and this program is that, here we provide the voltage-rms instead of voltage fluctuation data points. 

# In[8]:


class Amplifier:
    
    def __init__(self, gain, vrms):
        self.gain = gain
        self.vrms = vrms


class Resistor:
    
    def __init__(self, vrms):
        self.vrms = vrms
        
class Circuit:
    def __init__(self, resistance, bandwidth, frequency):
        self.resistance = resistance
        self.bandwidth = bandwidth
        self.frequency = frequency
        
amplifiers = [
    Amplifier(5,1.1745930046241017e-05),
    Amplifier(10,1.017186676745961e-05),
    Amplifier(15,9.097630153982875e-06),
    Amplifier(20,8.304629751072748e-06)
]
        
resistor = [
    Resistor(2.3493270156603197e-05)
]    

circuit_inputs = [
    Circuit(50, 5e9, 1e9),
]


# In[13]:


#providing the inputs
def inputs():
    number_res = 1    #At the moment the model is designed for only 1 resistors, not for intermidate resistors
    number_amp = int(input("Enter the number of the amplifiers in the circuit: "))
    
    
    vrms_of_resistor = []
                              
    b = []                    #random variables only used for constructing the loop
    for i in range(number_res):  
        b.append(resistor[i].vrms)
        vrms_of_resistor.append(b)
        
        
        
    vrms_of_amplifiers = []
    gain_of_amplifiers = []
    
                
    b = []       #random variables only used for constructing the loop
    for i in range(number_amp):
        b.append(amplifiers[i].vrms)
        vrms_of_amplifiers.append(b)
        gain_of_amplifiers.append(amplifiers[i].gain)
    
    resistance = circuit_inputs[0].resistance
    bandwidth = circuit_inputs[0].bandwidth
    frequency = circuit_inputs[0].frequency
    
    return(vrms_of_resistor, vrms_of_amplifiers, gain_of_amplifiers, resistance, bandwidth, frequency)




vrms_of_resistor, vrms_of_amplifiers, gain_of_amplifiers, resistance, bandwidth, frequency = inputs()




#for calculating noiseopower of resistors
def noisepower_resistors(vrms_of_resistor, gain_of_amplifiers, resistance):   
    

    #calculating noiseopower of resistors without gain
    noisepower_resistors_nogain = []
    for i in range(len(vrms_of_resistor)):
        noisepower_resistors_nogain.append(((resistor[i].vrms)**2)/(4*resistance))


    #calculating noiseopower of resistors with gain
    ll = 1                                             #random variables only used for constructing the loop
    rr = 1
    oo = 1
    mm = 1
    noisepower_resistor_withgain = []
    for i in range(len(vrms_of_resistor)):
        oo = noisepower_resistors_nogain[i]
        for j in range(0,len(gain_of_amplifiers)):  #equation for n amplifers, e.g. n=4; total noise power contributing from the resistor =  g1*g2*g3*g4(Noisepower of resistor)
            mm = gain_of_amplifiers[j]*oo
            oo = mm
        noisepower_resistor_withgain.append(oo)
    
    print('---------------------------------------------------------------')
    print('Noise power of the resistors:', noisepower_resistor_withgain)
    print('---------------------------------------------------------------')
    
    totalnoisepower_from_resisitors = sum(noisepower_resistor_withgain)   #total noisepower from the resistors
    print('Total noise power of the resistors:', totalnoisepower_from_resisitors)
    print('---------------------------------------------------------------')
    
    return(noisepower_resistors_nogain, noisepower_resistor_withgain, totalnoisepower_from_resisitors)



noisepower_resistors_nogain, noisepower_resistor_withgain, totalnoisepower_from_resisitors = noisepower_resistors(vrms_of_resistor, gain_of_amplifiers, resistance)





#for calculating noiseopower of amplifiers
def noisepower_amplifiers(vrms_of_amplifiers, gain_of_amplifiers, resistance):
    
    #calculating noiseopower of amplifiers without gain
    noisepower_amplifiers_nogain = []        
    for i in range(len(vrms_of_amplifiers)):
        noisepower_amplifiers_nogain.append(((amplifiers[i].vrms)**2)/(4*resistance))

    
    #calculating noiseopower of amplifiers with gain
    noisepower_amplifiers_withgains = []
    o = 1                                               #random variables only used for constructing the loop
    m = 1
    for i in range(len(vrms_of_amplifiers)):
        o = (((amplifiers[i].vrms)**2)/(4*resistance))
        for j in range(i+1,len(gain_of_amplifiers)):         #equation for n amplifers, e.g. n=4; total noise power contributing from the amplifer1 =  g2*g3*g4(Noisepower Amp1), total noise power contributing from the amplifer2 =  g3*g4(Noisepower Amp2), so on ....
            m = gain_of_amplifiers[j]*o
            o = m
        noisepower_amplifiers_withgains.append(o)
        
    print('Noise power of the amplifiers:', noisepower_amplifiers_withgains)
    print('---------------------------------------------------------------')
    
    totalnoisepower_from_amplifiers = sum(noisepower_amplifiers_withgains)   #total noisepower from the amplifiers
    print('Total noise power of the amplifiers:', totalnoisepower_from_amplifiers)
    print('---------------------------------------------------------------')
    
    return(noisepower_amplifiers_nogain,noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers)



noisepower_amplifiers_nogain, noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers = noisepower_amplifiers(vrms_of_amplifiers, gain_of_amplifiers, resistance)



#for calculating noisetemperatures of amplifiers
def noisetemperature_amplifiers(noisepower_amplifiers_nogain, noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers, frequency, bandwidth, resistance, vrms_of_amplifiers):
    
    #temperature_amplifiers: are the actual temperatures(i.e by which we deduce the Vrms of each amplifer). This is just required for verifying the model. 
    t1 = 1
    temperature_amplifiers=[]
    for i in range(len(vrms_of_amplifiers)):
        t1 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifiers_nogain[i])+1))    #Formula for finding the temperature with given noisepower
        temperature_amplifiers.append(t1)
    
    #for calculating the noise temperature of the amplifiers
    t2 = 1
    noisetemperature_amplifiers=[]
    for i in range(len(vrms_of_amplifiers)):
        t2 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifiers_withgains[i])+1))
        noisetemperature_amplifiers.append(t2)
        
    print('Noisetemperature of the amplifiers:', noisetemperature_amplifiers)
    print('---------------------------------------------------------------')

    
    totalnoisetemperature_from_amplifiers = sum(noisetemperature_amplifiers)
    print('Total Noisetemperature from the amplifiers:', totalnoisetemperature_from_amplifiers)
    print('---------------------------------------------------------------')
    
    return(temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers)



temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers = noisetemperature_amplifiers(noisepower_amplifiers_nogain, noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers, frequency, bandwidth, resistance, vrms_of_amplifiers)



#for calculating the noise temperature of the amplifiers

def noisetemperature_resistors(frequency, bandwidth, noisepower_resistor_withgain,vrms_of_resistor):
    
    t3 = 1
    noisetemperature_resistors=[]
    for i in range(len(vrms_of_resistor)):
        t3 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_resistor_withgain[i])+1))
        noisetemperature_resistors.append(t3)
    print('Total Noisetemperature from the resistors:', noisetemperature_resistors)
    print('---------------------------------------------------------------')
    
    totalnoisetemperature_from_resisitors = sum(noisetemperature_resistors)
    print('Total Noisetemperature from the resistors:', totalnoisetemperature_from_resisitors)
    print('---------------------------------------------------------------')
    return(noisetemperature_resistors, totalnoisetemperature_from_resisitors)
noisetemperature_resistors, totalnoisetemperature_from_resisitors = noisetemperature_resistors(frequency, bandwidth, noisepower_resistor_withgain, vrms_of_resistor)



total_noisepower = totalnoisepower_from_resisitors  + totalnoisepower_from_amplifiers 
print('Total Noisepower of circuit:', total_noisepower)

total_noisetemperature = totalnoisetemperature_from_resisitors + totalnoisetemperature_from_amplifiers
print('Total Noisetemperature of circuit:', total_noisetemperature)


# In[ ]:




