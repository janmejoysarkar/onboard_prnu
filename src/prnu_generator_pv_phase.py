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
-Last modified:
    2023-11-28
    2023-12-18: Added write fits option.
    2024-02-21: Added single point user defined entry for save location 
    and kernel size.
    Added minor comments. Made dustmap with 25 px kernel.
-Added feature for saving PRNU images as per the raw image date.

@author: janmejoy
"""

import numpy as np
import os
import glob
from astropy.io import fits
from astropy.convolution import convolve
from astropy.convolution import Box2DKernel
import datetime
from concurrent.futures import ProcessPoolExecutor

def add(filelist):
    data_sum=0
    for file in filelist:
        data_sum=data_sum+fits.open(file)[0].data
    return(data_sum)

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

def prep_header(fname, mfg, data_date):
    header=fits.Header()
    header['VERSION']=('beta', 'Version name for the Flat Field')
    header['FNAME']=(fname, 'LED ID for SUIT')
    header['MFG_DATE']=(mfg, 'Manufacturing date for the FITS file')
    header['DATADATE']=(data_date,'Date of raw data recording')
    return (header)

def flat_generator(filelist, kernel, name, save=None):
    stacked_led_img= add(filelist)
    led_flat_field= stacked_led_img/blur(stacked_led_img, kernel) #generates LED flat.
    hdu=fits.PrimaryHDU(led_flat_field, header=prep_header(name, mfg, date))
    if save==True: hdu.writeto(f'{sav}{name}.fits', overwrite=True)
    #Based on previous study, kernel size of 11x11 px is used for boxcar blurring in 'blur' function.
    return(led_flat_field)

#finds degree of correction implemented by PRNU correction.
def calib_stats(single_filename, prnu_file, croprow, cropcol, size, name):
    single= fits.open(single_filename)[0].data
    corrected= single/prnu_file
    crop_raw= single[croprow:croprow+size, cropcol:cropcol+size]
    crop_cor= corrected[croprow:croprow+size, cropcol:cropcol+size]
    crop_prnu= prnu_file[croprow:croprow+size, cropcol:cropcol+size]
    
    sd_raw= np.std(crop_raw)/np.mean(crop_raw)
    sd_cor= np.std(crop_cor)/np.mean(crop_cor)
    sd_prnu= np.std(crop_prnu)/np.mean(crop_prnu)
    calc_cor= np.sqrt(np.abs(sd_raw**2-sd_prnu**2))
    print(f"\n{name}")
    print("[1] Sdev Raw:", sd_raw)
    print("[2] Sdev Corrected:", sd_cor)
    print("[3] Sdev PRNU: ", sd_prnu)
    print("[4] sqrt(Raw^2-PRNU^2): ", calc_cor)
    print("Avg counts=", np.mean(crop_raw))
    print("Upon good FF correction, [2] and [4] should match well \n")
    
def run(files, kernel, name, croprow, cropcol, size, save):
    print(f"\n{name}\n")
    prnu = flat_generator(files, kernel, name, save)
    calib_stats(files[1], prnu, croprow, cropcol, size, name)

if __name__=='__main__':
    project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/LED/onboard_PRNU_project/')
    filelist= glob.glob(project_path+"data/raw/SUT*")
    sav= os.path.join(project_path, 'products/')
    mfg= str(datetime.date.today()) #manufacturing date
    
    kernel_355= 11 #default is 11 for PRNU
    kernel_255= 13 # default is 13 for PRNU
    date= filelist[0][-37:-27] #date of data recording
    
    aa_255, ff_255=[], [] #aa and ff represent different sets of 4 LEDs.
    aa_355, ff_355=[], []
    
    for file in filelist: #segregating files based on LEDONOFF ID
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

    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(run, ff_355, kernel_355, f'{date}_prnu_355_ff', 2000, 1500, 25, save=True),
            executor.submit(run, aa_355, kernel_355, f'{date}_prnu_355_aa', 2000, 1500, 25, save=True),
            executor.submit(run, ff_255, kernel_255, f'{date}_prnu_255_ff', 3700, 2000, 25, save=True),
            executor.submit(run, aa_255, kernel_255, f'{date}_prnu_255_aa', 3700, 2000, 25, save=True)
        ]
        for future in futures:
            future.result() # Wait for all futures to complete