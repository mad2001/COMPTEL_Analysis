#!/usr/bin/env python3.5
"""
Created on Tue Apr 5 20:50:52 2016

@author: Morgan

Script runs sets of simulations at once.
"""

import os
import subprocess


def run_sims():
    """
     Automates the running of Cosima simulations.

     Written more like a script than a function, it required the adjustment
     of parameters before use.

     source_file_path :: the full path to the Cosima source file that will be
                         used for simulations
     sim_dir :: the full path to the directory where *.sim files will be saved
     trials :: the number of simulations to run for each energy level
     energy_range :: an iterable the energy levels to simulate
    """

    source_file_path = '/Some/Path/Name'
    sim_dir = '/Volumes/MORGAN/newCOMPTEL_simulation_data'
    trials = 2
    energy_range = [1, 4, 53]

    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)
    os.chdir(sim_dir)

    source_dir, source_file = os.path.split(source_file_path)

    with open(source_file_path, 'r') as in_file:
        lines = in_file.readlines()

    for energy in energy_range:
        # change file name
        lines[16] = 'CollectData.FileName COMPTELdata_{}MeV\n'.format(energy)
        # change energy (in keV instead of MeV)
        lines[21] = 'neutron.Spectrum Mono {}\n'.format(energy*1000)

        with open(source_file_path, 'w') as out_file:
            out_file.writelines(lines)

        # run cosima
        for i in range(trials):
            subprocess.run('cosima '+source_file_path,
                           universal_newlines=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)


if __name__ == '__main__':
    run_sims()
