#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
from scipy.constants import *
from scipy.special import softmax
from dataclasses import dataclass
@dataclass
class Amplifier:
    gain: float
    noisetemperature: float


# In[2]:


def gain_iteration(signal1mean,signal2mean, std_signal, iterations, amplifiers, frequency,bandwidth, impedance, iteration_range, h, k):

    signal1 = np.random.normal(loc=signal1mean, scale= std_signal, size=iterations)
    signal2 = np.random.normal(loc=signal2mean, scale = std_signal, size=iterations)

    #extracting gain and noisetemperature for amplifier class
    amplifiers_gain = []
    noise_temperature_amplifiers = []
    for i in range(len(amplifiers)):
        amplifiers_gain.append(amplifiers[i].gain)
        noise_temperature_amplifiers.append(amplifiers[i].noisetemperature + 300)



    #noise_temp -> std_noise
    std_noise = []
    for i in range(len(noise_temperature_amplifiers)):
        a = np.sqrt((4*h*frequency*bandwidth*impedance)/np.exp(((h*frequency)/(k*noise_temperature_amplifiers[i]))-1))
        std_noise.append(a)

    #generating noise
    generating_noise = []
    for j in range(len(noise_temperature_amplifiers)):
        b = np.random.normal(loc=0, scale = std_noise[j], size=iterations)
        generating_noise.append(b)

    #signals after gain at each stage
    total_gain_each_stage = []
    c = 0
    for i in range(len(amplifiers_gain)):
        c = c+amplifiers_gain[i]
        total_gain_each_stage.append(c)

    signal1_after_gain = []
    signal2_after_gain = []
    for i in range(len(amplifiers_gain)):
        d_1 = (10**(total_gain_each_stage[i]/10))*signal1 + generating_noise[i]
        d_2 = (10**(total_gain_each_stage[i]/10))*signal2 + generating_noise[i]

        signal1_after_gain.append(d_1)
        signal2_after_gain.append(d_2)



    std_signal1_at_each_stage = []
    std_signal2_at_each_stage = []
    mean_signal1_amplifier_each_stage = []
    mean_signal2_amplifier_each_stage = []
    #fig = plt.figure(figsize=(12,12))
    #fig.subplots_adjust(hspace=0.3, wspace=0.3)
    for i in range(1,len(total_gain_each_stage)+1):


        y,x = np.histogram(signal1_after_gain[i-1], bins=int((iterations/4)))
        y1,x1 = np.histogram(signal2_after_gain[i-1], bins=int((iterations/4)))
        #ax = fig.add_subplot(2, 2, i)
        #y,x,h = ax.hist(signal1_after_gain[i-1], bins=int((iterations/4)), label='signal1')
        #y1,x1,h1 = ax.hist(signal2_after_gain[i-1], bins=int((iterations/4)), label='signal2')
        #ax.legend()

        mean_signal1_amplifier_each_stage.append(np.mean(x))
        mean_signal2_amplifier_each_stage.append(np.mean(x1))
        std_signal1_at_each_stage.append(np.std(x))
        std_signal2_at_each_stage.append(np.std(x1))


    std1 = []
    std2 = []
    for i in range(len(std_signal1_at_each_stage)):
        std1.append(std_signal1_at_each_stage[i]/2)
        std2.append(std_signal2_at_each_stage[i]/2)


    num_of_iterations_for_prob1_signal1 =[]
    num_of_iterations_for_prob2_signal2 =[]
    for j in range(len(std2)):
        for i in range(len(iteration_range)):
            s1, s2, p1, p2 = 0, 0, 0, 0
            signal1 = np.random.normal(loc=mean_signal1_amplifier_each_stage[j], scale= std2[j], size=iteration_range[i])

            # log(p(v=signal1|Si))
            for k in range(len(signal1)):
                s1 += -((signal1[k]- mean_signal1_amplifier_each_stage[j])**2)/(2*(std2[j]**2))

            # log(p(v=signal2|Si))
            for l in range(len(signal1)):
                s2 += -((signal1[l] - mean_signal2_amplifier_each_stage[j])**2)/(2*(std2[j]**2))

            p1, p2 = softmax([s1, s2])

            if p1 > 0.9:
                num_of_iterations_for_prob1_signal1.append(iteration_range[i])
                break

    for j in range(len(std2)):
        for i in range(len(iteration_range)):
            s1, s2, p1, p2 = 0, 0, 0, 0
            signal2 = np.random.normal(loc=mean_signal2_amplifier_each_stage[j], scale = std2[j], size=iteration_range[i])


            # log(p(v=signal1|Si))
            for k in range(len(signal2)):
                s1 += -((signal2[k]- mean_signal1_amplifier_each_stage[j])**2)/(2*(std2[j]**2))

            # log(p(v=signal2|Si))
            for l in range(len(signal2)):
                s2 += -((signal2[l] - mean_signal2_amplifier_each_stage[j])**2)/(2*(std2[j]**2))

            p1, p2 = softmax([s1, s2])

            if p2 > 0.9:
                num_of_iterations_for_prob2_signal2.append(iteration_range[i])
                break
    return(total_gain_each_stage, num_of_iterations_for_prob1_signal1, num_of_iterations_for_prob2_signal2, signal1_after_gain, signal2_after_gain)


# In[3]:


def gain_it_results(total_gain_each_stage, num_of_iterations_for_prob1_signal1, num_of_iterations_for_prob2_signal2, signal1_after_gain, signal2_after_gain):
    fig = plt.figure(figsize=(12,12))
    fig.subplots_adjust(hspace=0.3, wspace=0.3)
    for i in range(1,len(total_gain_each_stage)+1):
        ax = fig.add_subplot(2, 2, i)
        heading = 'Gain:'+str(total_gain_each_stage[i-1])+'dB'
        ax.hist(signal1_after_gain[i-1], bins=int((250)), label='signal1')
        ax.hist(signal2_after_gain[i-1], bins=int((250)), label='signal2')
        ax.set(title=heading)
        ax.legend()

    fig, axes = plt.subplots(ncols=2, figsize=(12,4))


    ax = axes[0]
    ax.plot(total_gain_each_stage, num_of_iterations_for_prob1_signal1, 'o', label='probability of measuring signal1 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal1) > 0.9',
           xlabel='Gain(db)', ylabel='Iterations')
    #ax.legend()




    ax = axes[1]
    ax.plot(total_gain_each_stage, num_of_iterations_for_prob2_signal2, 'o', label='probability of measuring signal2 = 1')
    ax.set(title='No. of iterations required to achieve P(Signal2) > 0.9',
           xlabel='Gain(db)', ylabel='Iterations')
    #ax.legend()


    print('gain:',total_gain_each_stage)
    print( 'no.Iterations for Signal1',num_of_iterations_for_prob1_signal1)
    print('no.Iterations for Signal2',num_of_iterations_for_prob2_signal2)

