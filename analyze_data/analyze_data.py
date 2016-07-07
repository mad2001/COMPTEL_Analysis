# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 15:50:01 2016
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""

import os
import sys
import glob
import pickle
import matplotlib.pyplot as plt
from numpy import sqrt

import neutron_analysis as na

sys.path.insert(0, '/Users/morgan/summer_research/process_sim_files')
from process_sims import Data

def open_data(path_to_pickles):
    """
    Outputs
    """

    eff30 = []
    err30 = []
    for pckl in glob.iglob(path_to_pickles + '/COMPTEL30MeV*_processed'):

        angles = [0, 10, 20, 30, 40, 50, 60]
        with open(pckl, 'rb') as f:
            data = pickle.load(f)
        eff = na.effective_area(data)
        eff30.append(eff)
        err30.append(eff/sqrt(data.triggered_events))


    eff50 = []
    err50 = []
    for pckl in glob.iglob(path_to_pickles + '/COMPTEL50MeV*_processed'):

        angles = [0, 10, 20, 30, 40, 50, 60]
        with open(pckl, 'rb') as f:
            data = pickle.load(f)
        eff = na.effective_area(data)
        eff50.append(eff)
        err50.append(eff/sqrt(data.triggered_events))

    plt.rc('text', usetex=True)
    plt.rc('font', family='serif')
    plt.plot(angles, eff30, 'bo', angles, eff50, 'ro')
    plt.hold(True)
    plt.xlim(-1, 61)
    plt.errorbar(angles, eff30, yerr=err30, fmt='.', capthick=1.5)
    plt.errorbar(angles, eff50, yerr=err50, fmt='r.', ecolor='r', capthick=1.5)
    plt.ylabel(r'Effective Area (cm\textsuperscript{2})')
    plt.xlabel(r'Neutron Incident Angle')
    plt.title(r'COMPTEL Effective Area')
    plt.legend([r'30 MeV', r'50 MeV'])
    plt.grid(True)
    plt.savefig('COMPTELeffective_area')
    plt.show()





    # plot efficiency vs energy
    # plot angular resolution vs energy
    # plot energy distribution for one energy
    # plot angular resolution distribution for one energy

if __name__ == '__main__':
    open_data(sys.argv[1])
