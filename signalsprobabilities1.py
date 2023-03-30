#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import random 
from scipy.constants import *
from scipy.stats import norm
from scipy.special import softmax


# In[2]:


def measurements_of_signal(signal1, signal2, signal1mean, signal2mean, std, size):    #std: standard devation
    probability1_measurment_signal_1 = []
    probability1_measurment_signal_2 = []
    probability2_measurment_signal_1 = []
    probability2_measurment_signal_2 = []
    
    s1, s2, p1, p2 = 0, 0, 0, 0
    

    # log(p(v=signal1|Si))
    for k in range(len(signal1)):
        s1 += -((signal1[k]- signal1mean)**2)/(2*(std**2))
            
    
        
    # log(p(v=signal2|Si))
    for l in range(len(signal1)):
        s2 += -((signal1[l] - signal2mean)**2)/(2*(std**2))
            

    p1, p2 = softmax([s1, s2])                              #softmax is used to normalize the results.
    probability1_measurment_signal_1.append(p1)
    probability2_measurment_signal_1.append(p2)
        
    
        
    s1, s2, p1, p2 = 0, 0, 0, 0
    # log(p(v=signal1|Si))
    for k in range(len(signal2)):
        s1 += -((signal2[k]- signal1mean)**2)/(2*(std**2))
            
    
        
    # log(p(v=signal2|Si))
    for l in range(len(signal2)):
        s2 += -((signal2[l] - signal2mean)**2)/(2*(std**2))
        

    p1, p2 = softmax([s1, s2])
    probability1_measurment_signal_2.append(p1)
    probability2_measurment_signal_2.append(p2)
        
    return(probability1_measurment_signal_1, probability1_measurment_signal_2, probability2_measurment_signal_1, 
           probability2_measurment_signal_2)


# In[3]:


def plotting_results(std, probability1_measurment_signal_1, probability1_measurment_signal_2, probability2_measurment_signal_1, probability2_measurment_signal_2):
    fig, axes = plt.subplots(ncols=2, figsize=(12,4))
    
    #plotting probability of signal 1 while measuring signal 1
    ax = axes[0]
    ax.plot(std,probability1_measurment_signal_1,  'o', color = 'b', label='probability of signal1')
    ax.plot(std,probability2_measurment_signal_1, 'o', color = 'k', label='probability of signal2')
    ax.set(title='Measurment of probability of signal 1', xlabel='Standard devation', ylabel='probability')
    ax.legend()
    
    
    #plotting probability of signal 2 while measuring signal 2
    ax = axes[1]
    ax.plot(std,probability1_measurment_signal_2,  'o', color = 'b', label='probability of signal1')
    ax.plot(std,probability2_measurment_signal_2, 'o', color = 'k', label='probability of signal2')
    ax.set(title='Measurment of probability of signal 2', xlabel='Standard devation', ylabel='probability')
    ax.legend()

