#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.constants import *


# In[ ]:


#providing the inputs
def inputs():
    #At the moment the model is designed for only 1 resistors, not for intermidate resistors
    
    
    
    vrms_of_resistor = []
                              
    b = []                    #random variables only used for constructing the loop
    for i in range(len(resistor)):  
        b.append(resistor[i].vrms)
        vrms_of_resistor.append(b)
        
        
        
    vrms_of_amplifiers = []
    gain_of_amplifiers = []
    
                
    b = []       #random variables only used for constructing the loop
    for i in range(len(amplifiers)):
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
    noisepower_resistor = []
    for i in range(len(vrms_of_resistor)):
        oo = noisepower_resistors_nogain[i]
        for j in range(0,len(gain_of_amplifiers)):  #equation for n amplifers, e.g. n=4; total noise power contributing from the resistor =  g1*g2*g3*g4(Noisepower of resistor)
            mm = gain_of_amplifiers[j]*oo
            oo = mm
        noisepower_resistor.append(oo)
    

    
    totalnoisepower_from_resisitors = sum(noisepower_resistor)   #total noisepower from the resistors

    
    return(noisepower_resistors_nogain, noisepower_resistor, totalnoisepower_from_resisitors)



noisepower_resistors_nogain, noisepower_resistor, totalnoisepower_from_resisitors = noisepower_resistors(vrms_of_resistor, gain_of_amplifiers, resistance)





#for calculating noiseopower of amplifiers
def noisepower_amplifiers(vrms_of_amplifiers, gain_of_amplifiers, resistance):
    
    #calculating noiseopower of amplifiers without gain
    noisepower_amplifiers_nogain = []        
    for i in range(len(vrms_of_amplifiers)):
        noisepower_amplifiers_nogain.append(((amplifiers[i].vrms)**2)/(4*resistance))

    
    #calculating noiseopower of amplifiers with gain
    noisepower_amplifiers = []
    o = 1                                               #random variables only used for constructing the loop
    m = 1
    for i in range(len(vrms_of_amplifiers)):
        o = (((amplifiers[i].vrms)**2)/(4*resistance))
        for j in range(i+1,len(gain_of_amplifiers)):         #equation for n amplifers, e.g. n=4; total noise power contributing from the amplifer1 =  g2*g3*g4(Noisepower Amp1), total noise power contributing from the amplifer2 =  g3*g4(Noisepower Amp2), so on ....
            m = gain_of_amplifiers[j]*o
            o = m
        noisepower_amplifiers.append(o)
        

    
    totalnoisepower_from_amplifiers = sum(noisepower_amplifiers)   #total noisepower from the amplifiers

    
    return(noisepower_amplifiers_nogain,noisepower_amplifiers, totalnoisepower_from_amplifiers)



noisepower_amplifiers_nogain, noisepower_amplifiers, totalnoisepower_from_amplifiers = noisepower_amplifiers(vrms_of_amplifiers, gain_of_amplifiers, resistance)



#for calculating noisetemperatures of amplifiers
def noisetemperature_amplifiers(noisepower_amplifiers_nogain, noisepower_amplifiers, totalnoisepower_from_amplifiers, frequency, bandwidth, resistance, vrms_of_amplifiers):
    
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
        t2 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifiers[i])+1))
        noisetemperature_amplifiers.append(t2)
        
    
    
    totalnoisetemperature_from_amplifiers = sum(noisetemperature_amplifiers)

    
    return(temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers)



temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers = noisetemperature_amplifiers(noisepower_amplifiers_nogain, noisepower_amplifiers, totalnoisepower_from_amplifiers, frequency, bandwidth, resistance, vrms_of_amplifiers)



#for calculating the noise temperature of the amplifiers

def noisetemperature_resistors(frequency, bandwidth, noisepower_resistor,vrms_of_resistor):
    
    t3 = 1
    noisetemperature_resistors=[]
    for i in range(len(vrms_of_resistor)):
        t3 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_resistor[i])+1))
        noisetemperature_resistors.append(t3)

    
    totalnoisetemperature_from_resisitors = sum(noisetemperature_resistors)
 
    return(noisetemperature_resistors, totalnoisetemperature_from_resisitors)

noisetemperature_resistors, totalnoisetemperature_from_resisitors = noisetemperature_resistors(frequency, bandwidth, noisepower_resistor, vrms_of_resistor)


def total_noise_temp_power(totalnoisepower_from_resisitors, totalnoisepower_from_amplifiers, totalnoisetemperature_from_resisitors, totalnoisetemperature_from_amplifiers):
    
    total_noisepower = totalnoisepower_from_resisitors  + totalnoisepower_from_amplifiers 


    total_noisetemperature = totalnoisetemperature_from_resisitors + totalnoisetemperature_from_amplifiers
    
    return(total_noisepower, total_noisetemperature)

total_noisepower, total_noisetemperature = total_noise_temp_power(totalnoisepower_from_resisitors, totalnoisepower_from_amplifiers, totalnoisetemperature_from_resisitors, totalnoisetemperature_from_amplifiers)

