#!/usr/bin/env python3.5
"""
Created on Tue Apr  5 20:50:52 2016

@author: Morgan
"""

import os
import subprocess


def run_sims(full_path):

    # number of files to run per energy level
    trials = 1

    # provide directory to save *.sim files
    sim_dir = '/Volumes/MORGAN/NE213_simulation_data'
    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)
    os.chdir(sim_dir)

    source_dir, source_file = os.path.split(full_path)

    with open(full_path, 'r') as in_file:
        lines = in_file.readlines()

    for energy in range(1, 21, 1):

        # change file name
        lines[13] = 'testing.FileName carbon13_{}MeV\n'.format(energy)
        # change energy (in keV instead of MeV)
        lines[18] = 'neutron.Spectrum Mono {}\n'.format(energy*1000)

        with open(full_path, 'w') as out_file:
            out_file.writelines(lines)

        # run cosima
        for i in range(trials):
            subprocess.run('cosima '+full_path,
                           universal_newlines=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)


if __name__ == '__main__':
    d = '/Users/morgan/Documents/MEGAlib_Tests/COMPTEL_material_tests/test_NE213.source'
    run_sims(d)
