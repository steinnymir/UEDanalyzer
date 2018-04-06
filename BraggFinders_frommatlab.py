# -*- coding: utf-8 -*-
"""

@author: Steinn Ymir Agustsson
"""
import sys, os
import numpy as np
import h5py
from UEDlib import utils
import time
import matplotlib.pyplot as plt
import scipy.fftpack as spfft
time.sleep(.2)
print('----RUN----')

Zentrum = [320, 466]
Wiederholungen = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]  # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
Messungen = 20

BASE_PATH = 'D:/data/UED/mat/'
SCAN_NAME = '2013_07_01_Bi_800nm_1_6mW_17kHz_100µm_t0_finerSteps'
H5_NAME = 'D:/data/UED/hdf5/{}.h5'.format(SCAN_NAME)

df = h5py.File(H5_NAME)
print('h5 structure:')
for name in df:
    try:
        for nname in df[name]:
            print(name + ' - ' + nname)
    except:
        print(name)

dark_avg = df['data']['dark'][:].sum(axis=(0,3)) / (20*40)

plt.imshow(dark_avg, cmap='gist_ncar')
plt.colorbar()
plt.scatter(Zentrum[0],Zentrum[1],s=10)
plt.show()

# add fft filter to remove outliers

peaks_only = np.empty_like(dark_avg)
threshold = 8000
for x in range(len(dark_avg[:,0])):
    for y in range(len(dark_avg[0,:])):
        if dark_avg[x,y] > threshold:
            peaks_only[x,y] = dark_avg[x,y]
        else:
            peaks_only[x,y] = 0

peaks_pol = utils.cart2pol_array(peaks_only,xc=320,yc=466)

maxima = []
temp_array = dark_avg.copy()
radius = 20

plt.imshow(dark_avg)
for i in range(12):
    x_max, y_max = utils.max2D(temp_array)
    maxima.append((x_max,y_max))
    temp_array[x_max-radius:x_max+radius,y_max-radius:y_max+radius] = 0
    plt.scatter(x_max,y_max, s=radius, c='red')
plt.show()

def find_maxima(array,radius,number):
    maxima = []
    temp_array = array.copy()
    peaks = np.ndarray((number,radius*2 ,radius*2 ))
    plt.imshow(dark_avg)
    for i in range(number):
        x_max, y_max = utils.max2D(temp_array)
        maxima.append((x_max, y_max))
        peaks[i,...] =temp_array[x_max - radius:x_max + radius, y_max - radius:y_max + radius]
        temp_array[x_max - radius:x_max + radius, y_max - radius:y_max + radius] = 0
        plt.scatter(y_max, x_max, s=radius, c='red')
    plt.show()
    return maxima, peaks

maxima, peaks = find_maxima(dark_avg,12,23)
plt.imshow(peaks[0,...])
plt.show()
# ----------- Make average image out of all Dark Images
# dark_avg = df['dark_img']


# if __name__ == '__main__':
#     main()
