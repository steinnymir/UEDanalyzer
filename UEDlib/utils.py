# -*- coding: utf-8 -*-
"""

@author: Steinn Ymir Agustsson
"""

import sys, os
import scipy.io as spio
import matplotlib.pyplot as plt
import numpy as np


def main():
    BASE_PATH= 'D:/data/UED/mat/'
    SCAN_NAME = '2013_07_01_Bi_800nm_1_6mW_17kHz_100µm_t0_finerSteps'

    output = import_mat_folder(BASE_PATH,SCAN_NAME)
    for key, val in output.items():
        if key =='data':
            print(output['data'].keys())
            try:
                print(output['data']['delay_1315'])
            except:
                pass
        elif key == 'dark_img':
            pass
        else:
            print(key,val)

    plt.imshow(output['data']['delay_1315']['001']['data'])

    plt.show()


def import_mat_folder(BASE_PATH,SCAN_NAME):

    # extract scan info from filenames

    list_of_files = os.listdir(BASE_PATH + SCAN_NAME)
    print('reading {} files'.format(len(list_of_files)))
    output = {
        'date': None,
        'stage_zero_position': None,
        'step_size': None,
        'total_averages': 0,
        'data': {}
    }

    other_files = []
    m_data_dict = {}
    dark_imgs = []


    for f in list_of_files:
        try:
            d = spio.loadmat(BASE_PATH + SCAN_NAME + '/' + f)
            if 'dark-' in f:
                dark_imgs.append(d['Image'])
            else:
                m_data_dict[f] = d['Image']
        except:
            other_files.append(f)

# make a dark image average:
    dark_imgs = np.array(dark_imgs,dtype='float64')
    output['dark_img'] = dark_imgs.sum(axis=0) / np.shape(dark_imgs)[0]
    print('created dark image with shape {}'.format(np.shape(output['dark_img'])))

    print('loading {} mat files'.format(len(list_of_files)-len(other_files)))
    for key,img in m_data_dict.items():

        base, index = key.split('-')

        base_list = base.split('_')
        date = [ base_list.pop(0) for n in range(2)]
        date = '_'.join(date)
        if output['date'] is None:
            output['date'] = date
        # from INDEX:

        zero_pos, current_pos, delay_num, avg_num = index.split('.')[0].split('_') #remove extension and split by _

        output['total_averages'] = max(int(avg_num), output['total_averages'])

         # create an entry in the dict for each bright scan
        pos_key = 'delay_{}'.format(current_pos)
        avg_key = 'avg_{}'.format(avg_num)
        try:
            output['data'][pos_key][avg_key]: {'img':img,'stage position':int(current_pos)}
        except:
            output['data'][pos_key] = {avg_key: {'img':img,'stage position':int(current_pos)}}


    # output['step_size'] = output['stage_positions'][1]-output['stage_positions'][0],
    # todo: implement stage position stuff

    return output



if __name__ == '__main__':
    main()