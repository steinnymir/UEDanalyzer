# -*- coding: utf-8 -*-
"""

@author: Steinn Ymir Agustsson
"""
import sys, os
import numpy as np

from UEDlib import utils

Zentrum = [466 305]
Wiederholungen = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]  # [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
Messungen = 20


scan_info = {'from':'1600'


}



Start = '1600'

# %load('2012_11_23_Cu_17_73kHz_7mW-Zeitachse.mat')
# %load('F:\autosave\2012_11_21_Cu_17_73kHz_5mW\ElektronenstromzuMessung-20s.mat')
# %load([Datei 'StageVector.mat']);

Image = utils.load_mat(base_path + Name + '-' + Start + '_' + Start + '_001_001.mat')

# %load([Datei Name '_dark-' Start '_' Start '_001_001.mat']);
MapD = Image
aa, bb = np.size(MapD)
MapD = np.zeros([aa, bb])

# %StageVector

# ----------- Make average image out of all Dark Images
def make_average_of_dark_images():
# TODO: write this function
# if ~exist([Datei num2str(sprintf('%.3d', Start)) '_' Name '-' Start '_' 'AllDARKslides.mat'], 'file')
    #     hw = waitbar(0, ['Summing up']);
    #     drawnow
    #     for Wind=Wiederholungen
    #     for me =1:Messungen
    #     a = dir([Datei Name '-' Start '*' sprintf('%03d', me) '_' sprintf('%03d', Wind) '.mat']);
    #     load(a.name);
    #     a.name;
    #
    #     MapD = MapD + Image;
    #
    # end
    # end
    # waitbar(Wind / Messungen, hw, 'Summing up');
    # drawnow
    # close(hw);
    # MapD = MapD / (Messungen * size(Wiederholungen, 2));
    # save([Datei num2str(sprintf('%.3d', Start)) '_' Name '-' Start '_' 'AllDARKslides.mat'], 'MapD');
    # disp('Summing done');
    # else
    # load([Datei num2str(sprintf('%.3d', Start)) '_' Name '-' Start '_' 'AllDARKslides.mat']);
    # disp('SumMap found');
    # end
    # MapDNorm = MapD;
    pass


# if __name__ == '__main__':
#     main()
