#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 23:08:40 2023
-Ran on SUIT server
-Written to compare 4 LED images using PV phase data. 
-To see the max and min counts and to check if the data is sufficient for PRNU
estimation.
-Last modified: 2023-11-28
@author: janmejoy
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from astropy.io import fits

def comparator (filelist, led):
    mean_list=[]
    for file in filelist:
        if (fits.open(file)[0].header['LEDONOFF']==led[0]):
            data=fits.open(file)[0].data
            row, col= led[1], led[2]
            size=5
            data_crop=data[row-size:row+size, col-size:col+size]
            mean_list.append(np.mean(data_crop))
    return(mean_list)

def noise_calculator(): #for calculating poission noise
    ls=[33470, 2210, 29535, 1490, 48388, 4993, 38689, 5031]
    for counts in ls:
        frames=40
        pe= counts*3*frames
        noise= np.sqrt(pe)
        pcnoise=noise*100/pe
        print(counts, pcnoise)
        
os.chdir('/home/janmejoy/SUIT_data/level1fits_subset')
filelist= sorted(glob.glob("SUT*/*"))
i=0
for file in filelist:
    if (fits.open(file)[0].header['LEDONOFF']=='aa00'):
        data=fits.open(file)[0].data
        #row= np.where(data==np.max(data))[0][0]
        #col= np.where(data==np.max(data))[1][0]
        #size=10
        #data_crop=data[row-size:row+size, col-size:col+size]
        plt.figure()
        #plt.subplot(1,2,1)
        plt.imshow(data)
        plt.title(i)
        plt.colorbar()
        #plt.scatter(col, row, color='red')
        #plt.subplot(1,2,2)
        #plt.imshow(data_crop)
        #plt.title(str(row)+'  '+str(col))
        #plt.colorbar()
        #print(i, np.max(data), row, col)
        i=i+1

#ledid, row, col  for max counts 
led_list_255=[['1', 1200, 2200], ['4', 4000, 2000], ['10', 3500, 3000], ['40', 2000, 2000], ['2', 1500, 1000], ['8', 4000, 2000], ['20', 4000, 3000], ['80', 1000, 2200], ['55', 3700, 2500], ['aa', 3700, 2000]]
for led in led_list_255:
    meanlist= comparator(filelist, led)
    print(led[0], np.mean(meanlist), np.std(meanlist))


led_list_355=[['100',2235,2063], ['400', 1420, 2667], ['1000', 1253, 1830], ['4000', 2071, 2150], ['200', 2076, 2645], ['800', 1328, 2431], ['2000', 1263, 1746], ['8000', 1816, 1642], ['aa00', 1500, 2000], ['5500', 1282, 1943]]
for led in led_list_355:
    meanlist= comparator(filelist, led)
    print(led[0], np.mean(meanlist), np.std(meanlist))


