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
from read_sims import Data


def open_data(path_to_pickles):
    """
    Outputs
    """

    energy = [20, 30, 50, 100]
    angles = [0, 10, 20, 30, 40, 50, 60]
    # plt.rc('text', usetex=True)
    # plt.rc('font', family='serif')

    with open('output_test2.txt', 'w') as f:
        for E in energy:
            eff = []
            err = []
            i = 0
            for pckl in glob.iglob( path_to_pickles + '/COMPTEL{}MeV*'.format(E) ):
                with open(pckl, 'rb') as p:
                    data = pickle.load(p)
                E_A = na.effective_area(data)
                eff.append(E_A)
                err.append(E_A/sqrt(data.triggered_events))

                f.write('{}, {}, {}\n'.format(E, angles[i], E_A))
                i += 1

            # plt.errorbar(angles, eff, yerr=err, fmt='s', capthick=1.5)
            # plt.hold(True)


    # plt.xlim(-1, 61)
    # plt.ylabel(r'Effective Area (cm\textsuperscript{2})')
    # plt.xlabel(r'Neutron Incident Angle')
    # plt.title(r'COMPTEL Effective Area')
    # plt.legend([r'20 MeV', r'30 MeV', r'50 MeV', r'100 MeV'])
    # plt.grid(True)
    # plt.savefig('COMPTELeffective_area')


    # plot efficiency vs energy
    # plot angular resolution vs energy
    # plot energy distribution for one energy
    # plot angular resolution distribution for one energy

if __name__ == '__main__':
    open_data(sys.argv[1])
