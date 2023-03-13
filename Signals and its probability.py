#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import random 
from scipy.constants import *
from scipy.stats import norm
import seaborn as sns
from scipy.special import softmax


# ## Probability of signals: 
# 
# 
# ## Section 1:  P(signal) as a function of standard deviation. 
# 
#  
# ### The number of iterations are kept constant, we are only changing the standard devation. 
# 

# #### Example inputs:
# #### Mean of signal 1: 2.296270691410484e-09 V  ;        (For E= (h/2π) * 1e9, the voltage is  2.296270691410484e-09 V)
# #### Mean of signal 1: 2.296270691410484e-09 V  ;       (For E= (h/2π) * 2e9, the voltage is  3.247417154672551e-09 V)
# 
# #### Standard devations = [ 1.2e-09, 1.6e-09, 2e-09, 2.4e-09, 2.8e-09, 3.2e-09, 3.6e-09, 4e-09, 4.4e-09]

# In[2]:


signal1mean = 2.296270691410484e-09
signal2mean = 3.247417154672551e-09
std = []
for i in range(9):
    std.append(1.2e-09 + i*0.4e-09)


# In[3]:


def measurment_signal1():
    probability1_measurment_signal_1 = []
    probability2_measurment_signal_1 = []
    for i in range(len(std)):
        s1 = 0
        s2 = 0
        p1 = 0
        p2 = 0
        signal1 = np.random.normal(loc=signal1mean, scale= std[i], size=20)
        signal2 = np.random.normal(loc=signal2mean, scale = std[i], size=20)
    

        # log(p(v=0|Si))
        for k in range(len(signal1)):
            a = -((signal1[k]- signal1mean)**2)/(2*(std[i]**2))
            s1 = s1+a
    
        
        # log(p(v=1|Si))
        for l in range(len(signal1)):
            b = -((signal1[l] - signal2mean)**2)/(2*(std[i]**2))
            s2 = s2 + b

        p1, p2 = softmax([s1, s2])
        probability1_measurment_signal_1.append(p1)
        probability2_measurment_signal_1.append(p2)
        
    plt.plot(std,probability1_measurment_signal_1,  'o', color = 'b', label='probability of signal1')
    plt.plot(std,probability2_measurment_signal_1, 'o', color = 'k', label='probability of signal2')
    plt.title('Measurment of probability of signal 1')
    plt.ylabel("probability")
    plt.xlabel("Standard devation")
    plt.legend()


def measurment_signal2():
    probability1_measurment_signal_2 = []
    probability2_measurment_signal_2 = []
    for i in range(len(std)):
        s1 = 0
        s2 = 0
        p1 = 0
        p2 = 0
        signal1 = np.random.normal(loc=signal1mean, scale= std[i], size=20)
        signal2 = np.random.normal(loc=signal2mean, scale = std[i], size=20)
    

        # log(p(v=0|Si))
        for k in range(len(signal2)):
            a = -((signal2[k]- signal1mean)**2)/(2*(std[i]**2))
            s1 = s1+a
    
        
        # log(p(v=1|Si))
        for l in range(len(signal2)):
            b = -((signal2[l] - signal2mean)**2)/(2*(std[i]**2))
            s2 = s2 + b

        p1, p2 = softmax([s1, s2])
        probability1_measurment_signal_2.append(p1)
        probability2_measurment_signal_2.append(p2)
        
    plt.plot(std,probability1_measurment_signal_2,  'o', color = 'b', label='probability of signal1')
    plt.plot(std,probability2_measurment_signal_2, 'o', color = 'k', label='probability of signal2')
    plt.title('Measurment of probability of signal 2')
    plt.ylabel("Probability")
    plt.xlabel("Standard devation")
    plt.legend()
    


# In[6]:


measurment_signal1()


# In[8]:


measurment_signal2()


# ## Section 2:  Here we find the number of iterations required achieve P(signal) = 1, for each respective standard deviation. 

# #### Example inputs: the example inputs are same as the previous sections. 
# 

# In[9]:


iterations = np.arange(300, 6000, 300)


# In[10]:


def iterations_probability_of_signal1():
    
    measurments_probability1_signal_1 = {}
    num_of_iterations_with_prob1_signal1 =[]
    probability_of_signal_1_is1_iteration = []
    for j in range(len(std)):
        for i in range(len(iterations)):
            s1 = 0
            s2 = 0
            p1 = 0
            p2 = 0
            probability1_measurment_signal_1 = [] 
            signal1 = np.random.normal(loc=signal1mean, scale= std[j], size=iterations[i])
            signal2 = np.random.normal(loc=signal2mean, scale = std[j], size=iterations[i])
    

            # log(p(v=0|Si))
            for k in range(len(signal1)):
                a = -((signal1[k]- signal1mean)**2)/(2*(std[j]**2))
                s1 = s1+a
    
        
            # log(p(v=1|Si))
            for l in range(len(signal1)):
                b = -((signal1[l] - signal2mean)**2)/(2*(std[j]**2))
                s2 = s2 + b

            p1, p2 = softmax([s1, s2])
        
            probability1_measurment_signal_1.append(p1)
            f = 'prob1_meas_sig_1_std_'+str(std[j])+'_itert_'+str(iterations[i])
            measurments_probability1_signal_1[f] = probability1_measurment_signal_1
        
        
            if p1 == 1:
                num_of_iterations_with_prob1_signal1.append(iterations[i])
                break
                
    plt.plot(std, num_of_iterations_with_prob1_signal1, 'o', label='probability of signal1 = 1')
    plt.xlabel("Standard devation")
    plt.ylabel("Iterations")
    plt.title("No. of iterations required to achieve P(Signal1) = 1, for respective standard devations")
    plt.legend()

def iterations_probability_of_signal2():
    y_axis_probability2_measurment_signal_2 = []
    measurments_probability2_signal_2 = {}
    num_of_iterations_with_prob2_signal2 =[]
    probability_of_signal_2_is1_iteration = []
    for j in range(len(std)):
        for i in range(len(iterations)):
            s1 = 0
            s2 = 0
            p1 = 0
            p2 = 0
            probability2_measurment_signal_2 = [] 
            signal1 = np.random.normal(loc=signal1mean, scale= std[j], size=iterations[i])
            signal2 = np.random.normal(loc=signal2mean, scale = std[j], size=iterations[i])
    

            # log(p(v=0|Si))
            for k in range(len(signal1)):
                a = -((signal2[k]- signal1mean)**2)/(2*(std[j]**2))
                s1 = s1+a
    
        
            # log(p(v=1|Si))
            for l in range(len(signal1)):
                b = -((signal2[l] - signal2mean)**2)/(2*(std[j]**2))
                s2 = s2 + b

            p1, p2 = softmax([s1, s2])
        
            probability2_measurment_signal_2.append(p2)
            f = 'prob2_meas_sig_2_std_'+str(std[j])+'_itert_'+str(iterations[i])
            measurments_probability2_signal_2[f] = probability2_measurment_signal_2
        
    
        
            if p2 == 1:
                num_of_iterations_with_prob2_signal2.append(iterations[i])
                break
                
    plt.plot(std, num_of_iterations_with_prob2_signal2, 'o', label='probability of signal2 = 1')
    plt.xlabel("Standard devation")
    plt.ylabel("Iterations")
    plt.title("No. of iterations required to achieve P(Signal2) = 1, for respective standard devations")
    plt.legend()


# In[11]:


iterations_probability_of_signal1()


# In[12]:


iterations_probability_of_signal2()

