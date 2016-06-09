# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:50:01 2016

@author: Morgan
"""

import os
import glob
import pickle

import neutron_analysis as na


def open_data(path_to_pickles):
    """
    Outputs
    """

    data = []

    for file in glob.glob(path_to_pickles):
        with open(file, 'wb') as f:
            data.append(pickle.load(f))

    return data

    # plot efficiency vs energy
    # plot angular resolution vs energy
    # plot energy distribution for one energy
    # plot angular resolution distribution for one energy
