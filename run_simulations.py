# -*- coding: utf-8 -*-
"""
Created on Tue Apr  5 20:50:52 2016

@author: Morgan
"""

import os
import subprocess


def run_sims():

    os.chdir('/Users/morgan/Documents/MEGAlib_Tests/Source_Files')
    source_file = 'carbon13.txt'

    for i, energy in enumerate(range(1, 5, 5)):

        # read source file
        with open(source_file, 'r') as in_file:
            lines = in_file.readlines()

        # change file name
        lines[15] = 'testing.FileName c{}MeV\n'.format(energy)
        # change energy (converts from MeV to keV)
        lines[20] = 'neutron.Spectrum Mono {}\n'.format(energy*1000)

        with open(source_file, 'w') as out_file:
            out_file.writelines(lines)


        # change to external hard drive so that *.sim files will save there
        d = '/Volumes/MORGAN/carbon_simulation_data'
        if not os.path.exists(d):
            os.makedirs(d)
        os.chdir(d)

        # run cosima
        subprocess.run("cosima" "filename")


if __name__ == '__main__':

    os.chdir('/Users/morgan/Documents/MEGAlib_Tests/Source_Files')
    print(os.getcwd())
    source_file = 'carbon13.txt'

    f = open(source_file)
    lines = f.readlines()
    #print(lines[3])
    print(lines[3])

    f.close()
