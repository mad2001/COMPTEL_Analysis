# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:50:01 2016
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""

import os
import sys
import glob
import pickle
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy import sqrt

import neutron_analysis as na

sys.path.insert(0, '/Users/morgan/summer_research/process_sim_files')
from read_sims import Data


def sort_angle(angle):
    if 0 < angle <= 5:
        return 0
    elif 5 < angle <= 15:
        return 10
    elif 15 < angle <= 25:
        return 20
    elif 25 < angle <= 35:
        return 30
    elif 35 < angle <= 45:
        return 40
    elif 45 < angle <= 55:
        return 50
    elif 55 < angle <= 65:
        return 60
    else:
        print('ERROR: ANGLE OUT OF EXPECTED RANGE')


def sort_energy(energy):
    if 0 < angle <= 5:
        return 0
    elif 5 < angle <= 15:
        return 10
    elif 15 < angle <= 25:
        return 20
    elif 25 < angle <= 35:
        return 30
    elif 35 < angle <= 45:
        return 40
    elif 45 < angle <= 55:
        return 50
    elif 55 < angle <= 65:
        return 60
    else:
        print('ERROR: ENERGY OUT OF EXPECTED RANGE')



def output_data(path_to_pickles):
    """
    Outputs
    """

    energy = [20, 25, 30, 40, 50, 75, 100]
    angles = [0, 10, 20, 30, 40, 50, 60]

    index = pd.MultiIndex.from_product([energy, angles],
                                       names=['measured energy', 'measured angle'])
    columns = pd.MultiIndex.from_product([energy, angles],
                                         names=['incident energy', 'incident angle'])

    df = pd.DataFrame(index=index, columns=columns)
    print(df)

    for pckl in glob.iglob( path_to_pickles + '/COMPTEL{}MeV*'.format(E) ):
        with open(pckl, 'rb') as p:
            data = pickle.load(p)

        df[data.incident_energy, data.angle]



# if __name__ == '__main__':
