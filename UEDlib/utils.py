# -*- coding: utf-8 -*-
"""

@author: Steinn Ymir Agustsson
"""

import sys, os
import scipy.io as spio
import matplotlib.pyplot as plt
import numpy as np
import pickle
import h5py


def main():
    if True:
        BASE_PATH = 'D:/data/UED/mat/'
        SCAN_NAME = '2013_07_01_Bi_800nm_1_6mW_17kHz_100µm_t0_finerSteps'
        H5_NAME = 'D:/data/UED/hdf5/{}.h5'.format(SCAN_NAME)
        df = make_h5(BASE_PATH, SCAN_NAME, H5_NAME, return_h5=True)
        for name in df:
            print(name)


def make_h5(BASE_PATH, SCAN_NAME, h5_file, return_h5=True):
    # extract scan info from filenames

    list_of_files = os.listdir(BASE_PATH + SCAN_NAME)
    print('reading {} files'.format(len(list_of_files)))

    other_files = []
    bright_dict = {}
    dark_dict = {}
    bright_data = None
    dark_data = None
    delays = []

    for f in list_of_files:
        try:
            d = spio.loadmat(BASE_PATH + SCAN_NAME + '/' + f)
            if 'dark-' in f:
                dark_dict[f] = np.float32(d['Image'])
            else:
                bright_dict[f] = np.float32(d['Image'])
        except:
            other_files.append(f)

    # read metadata from file names
    names = list(bright_dict.keys())
    metadata = {
        'max_average': 0,
        'delays': [],
        'time_zero': None,
        'date': None,
        'name_base': None,
    }
    stage_positions = []
    for i, name in enumerate(names):
        base, index = name.split('-')
        if metadata['name_base'] is None:
            metadata['name_base'] = base

        base_list = base.split('_')
        date = [base_list.pop(0) for n in range(3)]
        date = '_'.join(date)
        if metadata['date'] is None:
            metadata['date'] = date

        zero_pos, current_pos, delay_num, avg_num = index.split('.')[0].split('_')  # remove extension and split by _
        if metadata['time_zero'] is None:
            metadata['time_zero'] = int(zero_pos)
        else:
            if metadata['time_zero'] != int(zero_pos):
                raise ValueError('A file has the wrong zero position value.')
        stage_positions.append(int(current_pos) - metadata['time_zero'])
        delays.append(int(delay_num))
        metadata['max_average'] = max(metadata['max_average'], int(avg_num))

    metadata['delays'] = list(set(delays))
    metadata['time_delays'] = sorted(list(set(stage_positions)))

    print('loading {} mat files'.format(len(list_of_files) - len(other_files)))

    # initialize bright and dark image arrays as (avg_n
    (x, y) = np.shape(bright_dict[list(bright_dict.keys())[0]])
    bright_data = np.ndarray((metadata['max_average'], x, y, len(metadata['time_delays'])), dtype='float32')
    dark_data = np.ndarray((metadata['max_average'], x, y, len(metadata['time_delays'])), dtype='float32')

    for key, img in bright_dict.items():
        base, index = key.split('-')
        zero_pos, current_pos, delay_num, avg_num = index.split('.')[0].split('_')  # remove extension and split by _
        bright_data[int(avg_num) - 1, ..., int(delay_num) - 1] = img
    for key, img in dark_dict.items():
        base, index = key.split('-')
        zero_pos, current_pos, delay_num, avg_num = index.split('.')[0].split('_')  # remove extension and split by _
        dark_data[int(avg_num) - 1, ..., int(delay_num) - 1] = img

    # create hdf5 file

    hfile = h5py.File(h5_file, 'w')
    print('creating hdf5 dataframe in {}'.format(h5_file))
    hfile.create_dataset('data/bright', data=bright_data)
    hfile.create_dataset('data/dark', data=dark_data)
    hfile.create_group('metadata')
    for key, val in metadata.items():
            hfile.create_dataset('metadata/{}'.format(key), data=val)
    if return_h5:
        return hfile
    else:
        hfile.close()

def cart2pol_array(cartesian, xc=None, yc=None):

    lenX = len(cartesian[:, 0])
    lenY = len(cartesian[0, :])

    if xc == None:
        xc = int(lenX / 2)
    if yc is None:
        yc = int(lenY / 2)

    polar = np.zeros((lenX, lenY))
    for xi in range(lenX):
        for yi in range(lenY):
            x = xi - xc
            y = yi - yc

            rho = int(np.sqrt(x ** 2 + y ** 2))
            phi = int((np.arctan2(y, x) + np.pi) * np.pi)
            #            print('rho:{} phi:{}'.format(rho,phi))
            polar[rho, phi] += cartesian[xi, yi]
    return polar

def max2D(array):
    return np.unravel_index(array.argmax(), array.shape)

if __name__ == '__main__':
    main()
