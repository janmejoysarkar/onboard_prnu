#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:45:38 2024

@author: janmejoyarch
"""
import numpy as np
import matplotlib.pyplot as plt
from astropy.io import fits
import os
from astropy.convolution import convolve, Box2DKernel
from skimage.morphology import dilation, disk
from scipy.ndimage import median_filter

def lighten(image_list):
    '''
    Lighten blend
    image_list= List of 2D numpy arrays
    '''
    lighten_blend=np.zeros(np.shape(image_list[0]))
    for image in image_list:
        for i in range(4096):
            for j in range(4096):
                if image[i,j] > lighten_blend[i,j]:
                    lighten_blend[i,j]=image[i,j]
    return(lighten_blend)

def blur(data, kernel): #blurring function
    return(convolve(data, Box2DKernel(kernel), normalize_kernel=True))

project_path= os.path.expanduser('~/Dropbox/Janmejoy_SUIT_Dropbox/flat_field/LED/onboard_PRNU_project/')

prnu1= fits.open(project_path+'products/2024-02-23_prnu_355_ff.fits')[0].data
prnu2= fits.open(project_path+'products/2024-02-23_prnu_355_aa.fits')[0].data

lighten_blend= lighten([prnu1, prnu2])

image= fits.open(f'{project_path}data/external/SUT_T24_0615_000304_Lev1.0_2024-03-23T11.38.55.694_0971NB06.fits')[0].data

fig, ax= plt.subplots(2,2)
ax[0,0].imshow(image, vmin=0.97, vmax=1.03, origin='lower')
ax[1,0].imshow(prnu1, vmin=0.97, vmax=1.03, origin='lower')
ax[0,1].imshow(image, origin='lower')
ax[1,1].imshow(image/prnu1,origin='lower')

print(
np.std((image/lighten_blend)[2000:2500, 500:1000]),
np.std(image[2000:2500, 500:1000]),
np.std(prnu1[100:-100, 100:-100]),
np.std(prnu2[100:-100, 100:-100]),
)

blurred= convolve(lighten_blend, Box2DKernel(4), normalize_kernel=True)
plt.imshow(blurred, vmin=0.97, vmax=1.03, origin='lower')

dust_mask= dilation(blurred<0.99, disk(5))
plt.imshow(np.invert(dust_mask), origin='lower')

med= median_filter(lighten_blend, footprint=disk(20))
plt.imshow(med, vmin=0.97, vmax=1.03, origin='lower')

filtered= (lighten_blend*(np.invert(dust_mask)))+(med*dust_mask)
plt.imshow(filtered, vmin=0.97, vmax=1.03, origin='lower')

fig, ax= plt.subplots(nrows=1,ncols=2)
ax[0].imshow(image/filtered, origin='lower')
ax[1].imshow(image/prnu1, origin='lower')