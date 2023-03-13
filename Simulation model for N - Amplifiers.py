#!/usr/bin/env python
# coding: utf-8

# In[27]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.constants import *


# In[28]:


class Amplifier:
    def __init__(self, gain, vflucation_data_path):
        self.gain = gain
        self.vflucation_data_path = vflucation_data_path

class Resistor:
    def __init__(self, vflucation_data_path):
        self.vflucation_data_path = vflucation_data_path

class Otherinputs:
    def __init__(self, resistance, bandwidth, frequency):
        self.resistance = resistance
        self.bandwidth = bandwidth
        self.frequency = frequency


# In[29]:


amplifiers = [
    Amplifier(5,'Amplifier0_Voltageflucations.txt'),
    Amplifier(10,'Amplifier1_Voltageflucations.txt'),
    Amplifier(15,'Amplifier2_Voltageflucations.txt'),
    Amplifier(20,'Amplifier3_Voltageflucations.txt')
]


resistor = [
    Resistor('Resistor_Voltageflucations.txt')
]


otherinputs = [
    Otherinputs(50, 5e9, 1e9),
]


# In[30]:


#providing the inputs
def inputs():
    number_res = 1    #At the moment the model is designed for only 1 resistors, not for intermidate resistors
    number_amp = int(input("Enter the number of the amplifiers in the circuit: "))
    
    
    vrmsofresistor = []
    a = 1                             #random variables only used for constructing the loop
    b = []
    for i in range(number_res):  
        b.append(np.loadtxt(resistor[i].vflucation_data_path))
        a = np.std(b)
        vrmsofresistor.append(a)
        
        
        
    vrmsofamplifiers = []
    gainofamplifiers = []
    a = 1                             #random variables only used for constructing the loop
    b = []
    for i in range(number_amp):
        b.append(np.loadtxt(amplifiers[i].vflucation_data_path))
        a = np.std(b)
        vrmsofamplifiers.append(a)
        gainofamplifiers.append(amplifiers[i].gain)
    
    resistance = otherinputs[0].resistance
    bandwidth = otherinputs[0].bandwidth
    frequency = otherinputs[0].frequency
    
    return(vrmsofresistor, vrmsofamplifiers, gainofamplifiers, resistance, bandwidth, frequency)

vrmsofresistor, vrmsofamplifiers, gainofamplifiers, resistance, bandwidth, frequency = inputs()

print('---------------------------------------------------------------')

#for calculating noiseopower of resistors
def noisepower_resistors():   
    

    #calculating noiseopower of resistors without gain
    noisepower_resistors_nogain = []
    for i in range(len(vrmsofresistor)):
        noisepower_resistors_nogain.append(((vrmsofresistor[i])**2)/(4*resistance))


    #calculating noiseopower of resistors with gain
    ll = 1                                             #random variables only used for constructing the loop
    rr = 1
    oo = 1
    mm = 1
    noisepower_resistor_withgain = []
    for i in range(len(vrmsofresistor)):
        oo = noisepower_resistors_nogain[i]
        for j in range(0,len(gainofamplifiers)):  #equation for n amplifers, e.g. n=4; total noise power contributing from the resistor =  g1*g2*g3*g4(Noisepower of resistor)
            mm = gainofamplifiers[j]*oo
            oo = mm
        noisepower_resistor_withgain.append(oo)
    print('Noise power of the resistors:', noisepower_resistor_withgain)
    print('---------------------------------------------------------------')
    
    totalnoisepower_from_resisitors = sum(noisepower_resistor_withgain)   #total noisepower from the resistors
    print('Total noise power of the resistors:', totalnoisepower_from_resisitors)
    print('---------------------------------------------------------------')
    
    return(noisepower_resistors_nogain, noisepower_resistor_withgain, totalnoisepower_from_resisitors)
noisepower_resistors_nogain, noisepower_resistor_withgain, totalnoisepower_from_resisitors = noisepower_resistors()

#for calculating noiseopower of amplifiers
def noisepower_amplifiers():
    
    #calculating noiseopower of amplifiers without gain
    noisepower_amplifiers_nogain = []        
    for i in range(len(vrmsofamplifiers)):
        noisepower_amplifiers_nogain.append(((vrmsofamplifiers[i])**2)/(4*resistance))

    
    #calculating noiseopower of amplifiers with gain
    noisepower_amplifiers_withgains = []
    o = 1                                               #random variables only used for constructing the loop
    m = 1
    for i in range(len(vrmsofamplifiers)):
        o = (((vrmsofamplifiers[i])**2)/(4*resistance))
        for j in range(i+1,len(gainofamplifiers)):         #equation for n amplifers, e.g. n=4; total noise power contributing from the amplifer1 =  g2*g3*g4(Noisepower Amp1), total noise power contributing from the amplifer2 =  g3*g4(Noisepower Amp2), so on ....
            m = gainofamplifiers[j]*o
            o = m
        noisepower_amplifiers_withgains.append(o)
    print('Noise power of the amplifiers:', noisepower_amplifiers_withgains)
    print('---------------------------------------------------------------')
    
    totalnoisepower_from_amplifiers = sum(noisepower_amplifiers_withgains)   #total noisepower from the amplifiers
    print('Total noise power of the amplifiers:', totalnoisepower_from_amplifiers)
    print('---------------------------------------------------------------')
    
    return(noisepower_amplifiers_nogain,noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers)

noisepower_amplifiers_nogain, noisepower_amplifiers_withgains, totalnoisepower_from_amplifiers = noisepower_amplifiers()



#for calculating noisetemperatures of amplifiers
def noisetemperature_amplifiers():
    
    #temperature_amplifiers: are the actual temperatures(i.e by which we deduce the Vrms of each amplifer). This is just required for verifying the model. 
    t1 = 1
    temperature_amplifiers=[]
    for i in range(len(vrmsofamplifiers)):
        t1 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifiers_nogain[i])+1))    #Formula for finding the temperature with given noisepower
        temperature_amplifiers.append(t1)
    
    #for calculating the noise temperature of the amplifiers
    t2 = 1
    noisetemperature_amplifiers=[]
    for i in range(len(vrmsofamplifiers)):
        t2 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifiers_withgains[i])+1))
        noisetemperature_amplifiers.append(t2)
        
    print('Noisetemperature of the amplifiers:', noisetemperature_amplifiers)
    print('---------------------------------------------------------------')
    
    totalnoisetemperature_from_amplifiers = sum(noisetemperature_amplifiers)
    print('Total Noisetemperature from the amplifiers:', totalnoisetemperature_from_amplifiers)
    print('---------------------------------------------------------------')
    
    return(temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers)
temperature_amplifiers, noisetemperature_amplifiers, totalnoisetemperature_from_amplifiers = noisetemperature_amplifiers()


#for calculating the noise temperature of the amplifiers
def noisetemperature_resistors():
    

    t3 = 1
    noisetemperature_resistors=[]
    for i in range(len(noisepower_resistor_withgain)):
        t3 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_resistor_withgain[i])+1))
        noisetemperature_resistors.append(t3)
    print('Total Noisetemperature from the resistors:', noisetemperature_resistors)
    print('---------------------------------------------------------------')
    
    totalnoisetemperature_from_resisitors = sum(noisetemperature_resistors)
    print('Total Noisetemperature from the resistors:', totalnoisetemperature_from_resisitors)
    print('---------------------------------------------------------------')
    return(noisetemperature_resistors, totalnoisetemperature_from_resisitors)
noisetemperature_resistors, totalnoisetemperature_from_resisitors = noisetemperature_resistors()



total_noisepower = totalnoisepower_from_resisitors  + totalnoisepower_from_amplifiers 
print('Total Noisepower of circuit:', total_noisepower)

total_noisetemperature = totalnoisetemperature_from_resisitors + totalnoisetemperature_from_amplifiers
print('Total Noisetemperature of circuit:', total_noisetemperature)

