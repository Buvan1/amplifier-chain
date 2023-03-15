#!/usr/bin/env python
# coding: utf-8

# In[63]:


import numpy as np
import matplotlib.pyplot as plt
import random 
from scipy.constants import *
from scipy.stats import norm
import seaborn as sns
from scipy.special import softmax


# "" Probability of signals: 
# 
# 
# "" Section 1:  P(signal) as a function of standard deviation. 
# 
#  
# """ The number of iterations are kept constant, we are only changing the standard devation. 
# 

# """" Example inputs:
# """" Mean of signal 1: 2.296270691410484e-09 V  ;        (For E= (h/2π) * 1e9, the voltage is  2.296270691410484e-09 V)
# """" Mean of signal 1: 2.296270691410484e-09 V  ;       (For E= (h/2π) * 2e9, the voltage is  3.247417154672551e-09 V)
# 
# """" Standard devations = [ 1.2e-09, 1.6e-09, 2e-09, 2.4e-09, 2.8e-09, 3.2e-09, 3.6e-09, 4e-09, 4.4e-09]

# In[64]:


signal1mean = 2.296270691410484e-09
signal2mean = 3.247417154672551e-09
std = []
for i in range(9):
    std.append(1.2e-09 + i*0.4e-09)


# In[65]:


def measurements_of_signal(signal1mean, signal2mean, std):    #std: standard devation
    probability1_measurment_signal_1 = []
    probability1_measurment_signal_2 = []
    probability2_measurment_signal_1 = []
    probability2_measurment_signal_2 = []
    
    for i in range(len(std)):
        s1, s2, p1, p2 = 0, 0, 0, 0
        signal1 = np.random.normal(loc=signal1mean, scale= std[i], size=20)
        signal2 = np.random.normal(loc=signal2mean, scale = std[i], size=20)
    

        # log(p(v=signal1|Si))
        for k in range(len(signal1)):
            s1 += -((signal1[k]- signal1mean)**2)/(2*(std[i]**2))
            
    
        
        # log(p(v=signal2|Si))
        for l in range(len(signal1)):
            s2 += -((signal1[l] - signal2mean)**2)/(2*(std[i]**2))
            

        p1, p2 = softmax([s1, s2])                              #softmax is used to normalize the results.
        probability1_measurment_signal_1.append(p1)
        probability2_measurment_signal_1.append(p2)
        
    
        
        s1, s2, p1, p2 = 0, 0, 0, 0
        # log(p(v=signal1|Si))
        for k in range(len(signal2)):
            s1 += -((signal2[k]- signal1mean)**2)/(2*(std[i]**2))
            
    
        
        # log(p(v=signal2|Si))
        for l in range(len(signal2)):
            s2 += -((signal2[l] - signal2mean)**2)/(2*(std[i]**2))
        

        p1, p2 = softmax([s1, s2])
        probability1_measurment_signal_2.append(p1)
        probability2_measurment_signal_2.append(p2)
        
    return(probability1_measurment_signal_1, probability1_measurment_signal_2, probability2_measurment_signal_1, probability2_measurment_signal_2)


    


# In[67]:


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


# In[68]:


plotting_results(std, probability1_measurment_signal_1, probability1_measurment_signal_2, probability2_measurment_signal_1, probability2_measurment_signal_2)


# " Section 2:  Here we find the number of iterations required achieve P(signal) = 1, for each respective standard deviation. 

# "" Example inputs: the example inputs are same as the previous sections. 
# 

# In[52]:


iterations = np.arange(300, 6000, 300)


# In[69]:


def iterations_required(iterations, std, signal1mean, signal2mean):
    
    measurments_probability1_signal_1 = {}
    num_of_iterations_with_prob1_signal1 =[]
    measurments_probability2_signal_2 = {}
    num_of_iterations_with_prob2_signal2 =[]
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
                num_of_iterations_with_prob1_signal1.append(iterations[i])
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
                num_of_iterations_with_prob2_signal2.append(iterations[i])
                break
    return(num_of_iterations_with_prob1_signal1, num_of_iterations_with_prob2_signal2, 
           measurments_probability1_signal_1, measurments_probability2_signal_2)


# In[77]:


def plotting_iterations_results(std, num_of_iterations_with_prob1_signal1, num_of_iterations_with_prob2_signal2):
    fig, axes = plt.subplots(ncols=2, figsize=(12,4))
    
    #plotting number of iterations required to achieve probability of signal-1 = 1, for respective standard devations
    ax = axes[0]
    ax.plot(std, num_of_iterations_with_prob1_signal1, 'o', label='probability of signal1 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal1) = 1', 
           xlabel='Standard devation', ylabel='Iterations')
    ax.legend()
    
    
    
    #plotting number of iterations required to achieve probability of signal-2 = 1, for respective standard devations
    ax = axes[1]
    ax.plot(std, num_of_iterations_with_prob2_signal2, 'o', label='probability of signal2 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal2) = 1', 
           xlabel='Standard devation', ylabel='Iterations')
    ax.legend()       


# In[ ]:




