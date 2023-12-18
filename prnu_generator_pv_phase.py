#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 13:48:51 2023
-Ran on SUIT server
-LED PRNU model generator from PV phase data.
-Same functions used for PRNU calculations as that used for FBT data.
-Level 1 data is used for analysis here.
-Bias correction is not used here.
-4LED Files are segregated based on image headers
-Last modified: 2023-11-28

@author: janmejoy
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from astropy.io import fits
from astropy.convolution import convolve
from astropy.convolution import Box2DKernel

def add(filelist):
    data_sum=0
    for file in filelist:
        data_sum=data_sum+fits.open(file)[0].data
    return(data_sum)

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

def flat_generator(filelist, kernel, name):
    stacked_led_img= add(filelist)
    led_flat_field= stacked_led_img/blur(stacked_led_img, kernel) #generates LED flat.
    #Based on previous study, kernel size of 11x11 px is used for boxcar blurring in 'blur' function.
    
    #Data visualization only.
    plt.figure(name, figsize=(10, 5))
    plt.subplot(1,2,1)
    plt.imshow(stacked_led_img)
    plt.colorbar()
    plt.title("Bias corrected Master LED Image")
    plt.subplot(1,2,2)
    plt.imshow(led_flat_field, vmin=0.97, vmax=1.03)
    plt.title(name)
    plt.colorbar()
    plt.show()
    return(led_flat_field)

#finds degree of correction implemented by PRNU correction.
def calib_stats(single, corrected, prnu, croprow, cropcol, size):
    crop_raw= single[croprow:croprow+size, cropcol:cropcol+size]
    crop_cor= corrected[croprow:croprow+size, cropcol:cropcol+size]
    crop_prnu= prnu[croprow:croprow+size, cropcol:cropcol+size]
    #plt.figure()
    #plt.imshow(crop_cor)
    
    sd_raw= np.std(crop_raw)/np.mean(crop_raw)
    sd_cor= np.std(crop_cor)/np.mean(crop_cor)
    sd_prnu= np.std(crop_prnu)/np.mean(crop_prnu)
    calc_cor= np.sqrt(np.abs(sd_raw**2-sd_prnu**2))
    
    print("[1] Sdev Raw:", sd_raw)
    print("[2] Sdev Corrected:", sd_cor)
    print("[3] Sdev PRNU: ", sd_prnu)
    print("[4] sqrt(Raw^2-PRNU^2): ", calc_cor)
    print("Avg counts=", np.mean(crop_raw))
    print("Upon good FF correction, [2] and [4] should match well")



os.chdir('/home/janmejoy/SUIT_data/level1fits_subset')
filelist= glob.glob("SUT*/*")
aa_255, ff_255=[], []
aa_355, ff_355=[], []

for file in filelist:
    ledstat=fits.open(file)[0].header['LEDONOFF']
    if (ledstat=='55'):
        print (ledstat, fits.open(file)[0].header['FW1POS'], file)
        ff_255.append(file)
    elif(ledstat=='aa'):
        print (ledstat, fits.open(file)[0].header['FW1POS'], file)
        aa_255.append(file)
    elif(ledstat=='5500'):
        print (ledstat, fits.open(file)[0].header['FW1POS'], file)
        ff_355.append(file)
    elif(ledstat=='aa00'):
        print (ledstat, fits.open(file)[0].header['FW1POS'], file)
        aa_355.append(file)
   

name='prnu_355_ff'
filelist= ff_355
croprow, cropcol= 2000, 1500

prnu= flat_generator(filelist, 11, str(filelist))
single=fits.open(filelist[1])[0].data
corrected= single/prnu
calib_stats(single, corrected, prnu, croprow, cropcol, 25)


name='prnu_255_aa'
filelist= aa_255
croprow, cropcol= 3700, 2000

prnu= flat_generator(filelist, 13, str(filelist))
single=fits.open(filelist[1])[0].data
corrected= single/prnu
calib_stats(single, corrected, prnu, croprow, cropcol, 25)
