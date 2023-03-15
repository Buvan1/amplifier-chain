#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from scipy.constants import *


# """"In this program I have generated a normal distribution of voltage fluctuation values, and this voltage has mean zero  but a non zero root mean square value. In this simulation we can observe that the temperature of components in circuit can be achieved by providing back the generated voltage-rms. Through this process we also validate that the formulas can also be adapted in cascade system(for more than one amplifier) to obtain noise temperature and noise-power of the components. 

# In[5]:


resistance = 50
actual_temperature_resistor = 200
actual_temperature_amplifier1 = 100
actual_temperature_amplifier2 = 75
actual_temperature_amplifier3 = 50
actual_temperature_amplifier4 = 25

bandwidth = 1e9
frequency = 5e9

gain_amplifier1 = 5
gain_amplifier2 = 10
gain_amplifier3 = 15
gain_amplifier4 = 20


# In[8]:


vrms_resistor = np.sqrt((4*h*frequency*bandwidth*resistance)/(np.exp((h*frequency)/(k*actual_temperature_resistor))-1))                 #Vrms of resisitor
noise_power_resistor = (vrms_resistor*vrms_resistor)/(4*resistance)                                                                     #Noise power of resisitor

vrms_amplifier1 = np.sqrt((4*h*frequency*bandwidth*resistance)/(np.exp((h*frequency)/(k*actual_temperature_amplifier1))-1))             #Vrms of amplifier 1
noise_power_amplifier1 = (vrms_amplifier1*vrms_amplifier1)/(4*resistance)                                                               #Noise power of amplifier 1

vrms_amplifier2 = np.sqrt((4*h*frequency*bandwidth*resistance)/(np.exp((h*frequency)/(k*actual_temperature_amplifier2))-1))             #Vrms of amplifier 2
noise_power_amplifier2 = (vrms_amplifier2*vrms_amplifier2)/(4*resistance)                                                               #Noise power of amplifier 2

vrms_amplifier3 = np.sqrt((4*h*frequency*bandwidth*resistance)/(np.exp((h*frequency)/(k*actual_temperature_amplifier3))-1))             #Vrms of amplifier 3
noise_power_amplifier3 = (vrms_amplifier3*vrms_amplifier3)/(4*resistance)                                                               #Noise power of amplifier 3

vrms_amplifier4 = np.sqrt((4*h*frequency*bandwidth*resistance)/(np.exp((h*frequency)/(k*actual_temperature_amplifier4))-1))             #Vrms of amplifier 4
noise_power_amplifier4 = (vrms_amplifier4*vrms_amplifier4)/(4*resistance)                                                               #Noise power of amplifier 4


# "" From the above Vrms of each component we generate random voltage flucations values, which are noise from the components. 

# In[37]:


x_resistor = np.random.normal(loc=0, scale = vrms_resistor, size=100000)          #Voltage flucation values from resisitor
x_amplifier_1 = np.random.normal(loc=0, scale = vrms_amplifier1, size=100000)     #Voltage flucation values from amplifier1
x_amplifier_2 = np.random.normal(loc=0, scale = vrms_amplifier2, size=100000)     #Voltage flucation values from amplifier2
x_amplifier_3 = np.random.normal(loc=0, scale = vrms_amplifier3, size=100000)     #Voltage flucation values from amplifier3
x_amplifier_4 = np.random.normal(loc=0, scale = vrms_amplifier4, size=100000)     #Voltage flucation values from amplifier4


# In[38]:


x_gain_resistor = np.sqrt(gain_amplifier1)*np.sqrt(gain_amplifier2)*np.sqrt(gain_amplifier3)*np.sqrt(gain_amplifier4)*(x_resistor)       #Multiplying gains from each amplifier on voltage flucations from resisitor
x_gain_amplifier_1 = np.sqrt(gain_amplifier2)*np.sqrt(gain_amplifier3)*np.sqrt(gain_amplifier4)*(x_amplifier_1)                          #Multiplying gains from next preceding amplifiers in the amplifier chain, on voltage flucations from amplifier1
x_gain_amplifier_2 = np.sqrt(gain_amplifier3)*np.sqrt(gain_amplifier4)*(x_amplifier_2)                                                   #Multiplying gains from next preceding amplifiers in the amplifier chain, on voltage flucations from amplifier2
x_gain_amplifier_3 = np.sqrt(gain_amplifier4)*(x_amplifier_3)                                                                            #Multiplying gains from next preceding amplifiers in the amplifier chain, on voltage flucations from amplifier3
#Voltage flucations from the amplifier4 is not multiplied by any gain, because it is the last amplifier in the amplifier chain


# In[39]:


gain_vrms_resistor = np.std(x_gain_resistor)                #vrms of gained voltage flucations from resistor
gain_vrms_amplifier1 = np.std(x_gain_amplifier_1)           #vrms of gained voltage flucations from amplifier1
gain_vrms_amplifier2 = np.std(x_gain_amplifier_2)           #vrms of gained voltage flucations from amplifier2
gain_vrms_amplifier3 = np.std(x_gain_amplifier_3)           #vrms of gained voltage flucations from amplifier3
vrms_amplifier_4 = np.std(x_amplifier_4)                    #vrms of voltage flucations from amplifier4. Note-It has no gain.


# In[40]:


noisepower_resistor = (gain_vrms_resistor*gain_vrms_resistor)/(4*resistance)             #
noisepower_amplifier_1 = (gain_vrms_amplifier1*gain_vrms_amplifier1)/(4*resistance)
noisepower_amplifier_2 = (gain_vrms_amplifier2*gain_vrms_amplifier2)/(4*resistance)
noisepower_amplifier_3 = (gain_vrms_amplifier3*gain_vrms_amplifier3)/(4*resistance)
noisepower_amplifier_4 = (vrms_amplifier_4*vrms_amplifier_4)/(4*resistance)
Total_noisepower = noisepower_resistor + noisepower_amplifier_1 + noisepower_amplifier_2  + noisepower_amplifier_3 + noisepower_amplifier_4 


# In[41]:


Total_noise_temperature = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/Total_noisepower)+1))
print("the total noise power:", Total_noisepower)
print("the total temperature:", Total_noise_temperature)


# In[43]:


noise_temperature_resistor = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_resistor)+1))
noise_temperature_amplifier_1 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifier_1)+1))
noise_temperature_amplifier_2 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifier_2)+1))
noise_temperature_amplifier_3 = (h*frequency)/(k*np.log(((h*frequency*bandwidth)/noisepower_amplifier_3)+1))
temperature_amplifier_4 = Total_noise_temperature - noise_temperature_resistor - noise_temperature_amplifier_1 - noise_temperature_amplifier_2 - noise_temperature_amplifier_3                #note: I have not multiplied g(gain) with tr1 and ta11 because its already taken into account while calculating for vr and va1.
print("The temperature of the amplifier is:", temperature_amplifier_4)
print("The actual temperature of the amplifier is:", actual_temperature_amplifier4)


# In[ ]:





# In[ ]:




