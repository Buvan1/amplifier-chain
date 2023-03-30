#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import matplotlib.pyplot as plt
import random 
from scipy.constants import *
from scipy.stats import norm
from scipy.special import softmax


# In[3]:


def iterations_required(iterations, std, signal1mean, signal2mean):
    
    measurments_probability1_signal_1 = {}
    num_of_iterations_for_prob1_signal1 =[]
    measurments_probability2_signal_2 = {}
    num_of_iterations_for_prob2_signal2 =[]
    for j in range(len(std)):
        for i in range(len(iterations)):
            s1, s2, p1, p2 = 0, 0, 0, 0
            probability1_measurment_signal_1 = [] 
            signal1 = np.random.normal(loc=signal1mean, scale= std[j], size=iterations[i])
            signal2 = np.random.normal(loc=signal2mean, scale = std[j], size=iterations[i])
    

            # log(p(v=signal1|Si))
            for k in range(len(signal1)):
                s1 += -((signal1[k]- signal1mean)**2)/(2*(std[j]**2))
            
    
        
            # log(p(v=signal2|Si))
            for l in range(len(signal1)):
                s2 += -((signal1[l] - signal2mean)**2)/(2*(std[j]**2))

            p1, p2 = softmax([s1, s2])
        
            probability1_measurment_signal_1.append(p1)
            f = 'prob1_meas_sig_1_std_'+str(std[j])+'_itert_'+str(iterations[i])
            measurments_probability1_signal_1[f] = probability1_measurment_signal_1
        
        
            if p1 == 1:
                num_of_iterations_for_prob1_signal1.append(iterations[i])
                break
                
                
    for j in range(len(std)):         
        for i in range(len(iterations)):
            signal1 = np.random.normal(loc=signal1mean, scale= std[j], size=iterations[i])
            signal2 = np.random.normal(loc=signal2mean, scale = std[j], size=iterations[i])
            s1, s2, p1, p2 = 0, 0, 0, 0
            probability2_measurment_signal_2 = [] 
            
            
            # log(p(v=signal1|Si))
            for k in range(len(signal1)):
                s1 += -((signal2[k]- signal1mean)**2)/(2*(std[j]**2))
            
    
        
            # log(p(v=signal2|Si))
            for l in range(len(signal1)):
                s2 += -((signal2[l] - signal2mean)**2)/(2*(std[j]**2))


            p1, p2 = softmax([s1, s2])
            probability2_measurment_signal_2.append(p2)
            f = 'prob2_meas_sig_2_std_'+str(std[j])+'_itert_'+str(iterations[i])
            measurments_probability2_signal_2[f] = probability2_measurment_signal_2
        
    
        
            if p2 == 1:
                num_of_iterations_for_prob2_signal2.append(iterations[i])
                break
    return(num_of_iterations_for_prob1_signal1, num_of_iterations_for_prob2_signal2, 
           measurments_probability1_signal_1, measurments_probability2_signal_2)
    


# In[4]:


def plotting_iterations_results(std, num_of_iterations_for_prob1_signal1, num_of_iterations_for_prob2_signal2):
    fig, axes = plt.subplots(ncols=2, figsize=(12,4))
    
    #plotting number of iterations required to achieve probability of signal-1 = 1, for respective standard devations
    ax = axes[0]
    ax.plot(std, num_of_iterations_for_prob1_signal1, 'o', label='probability of measuring signal1 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal1) = 1', 
           xlabel='Standard devation', ylabel='Iterations')
    ax.legend()
    
    
    
    #plotting number of iterations required to achieve probability of signal-2 = 1, for respective standard devations
    ax = axes[1]
    ax.plot(std, num_of_iterations_for_prob2_signal2, 'o', label='probability of measuring signal2 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal2) = 1', 
           xlabel='Standard devation', ylabel='Iterations')
    ax.legend()    

