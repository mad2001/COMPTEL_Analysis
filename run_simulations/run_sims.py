#!/usr/bin/env python3.5
"""Script runs sets of simulations at once.

Created on Tue Apr 5 20:50:52 2016
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""

import os
import subprocess
import re


def run_sims():
    """Run Cosima simulations for a range of incident energy levels.

    The following parameters must be edited before running:
    source_file_path -- the full path to the Cosima source file that will be
                        used for simulations
    sim_dir -- the full path to the directory where *.sim files will be saved
    trials -- the number of simulations to run for each energy level
    energy -- the energy levels to simulate (this can be provided as a list or
              a range, as shown below)

    YOU MUST EDIT THE LINES THAT WILL BE UPDATED IN THE SOURCE FILE
    A regular expression for the line that will change must be provided, along
    with the string that will replace it. An example is provided in the script.
    """
    source_file_path = '/Users/morgan/Documents/COMPTEL/COMPTELpractice.source'
    sim_dir = '/Users/morgan/Documents/COMPTEL/COMPTEL_data'
    trials = 2

    """ """ """ """ """ PROVIDE PARAMETERS AS A LIST """ """ """ """ """
    # energy = [1, 5, 15, 30, 55, 100]
    energy = [20, 100]
    # angles = [0, 10, 20, 30, 40, 50, 60]
    angles = [0, 10, 20, 30, 40, 50, 60]

    """ """ """ """ """ PROVIDE PARAMETERS AS A RANGE """ """ """ """ """
    # low_energy = 1      # lowest energy simulated (in MeV)
    # high_energy = 100   # highest energy simulated (in MeV)
    # energy_step = 5     # interval
    # energy = [x for x in range(low_energy, high_energy, energy_step)]
    # min_angle = 0
    # max_angle = 60
    # angle_step = 10
    # angles = [x for x in range(min_angle, max_angle, angle_step)]

    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)

    source_dir, source_file = os.path.split(source_file_path)
    with open(source_file_path, 'r') as in_file:
        # creates a list with each line in source file as an element
        lines = in_file.read()

    for E in energy:
        """ """ """  THIS SECTION SHOULD BE EDITED BEFORE RUNNING  """ """ """
        # update incident energy (changing from MeV to keV)
        energy_regex = 'neutron\.Spectrum Mono .+\n'
        energy_write = 'neutron.Spectrum Mono {}\n'
        lines = re.sub(energy_regex, energy_write.format(E * 1000), lines)
        """ """ """ """ """ """""""" END OF SECTION """"""" """ """ """ """ """
        for theta in angles:
            """ """ """ THIS SECTION SHOULD BE EDITED BEFORE RUNNING """ """ """
            # update incident angle
            angle_regex = 'neutron.Beam FarFieldAreaSource .+\n'
            angle_write = 'neutron.Beam FarFieldAreaSource {} {} 0 360\n'
            lines = re.sub(angle_regex, angle_write.format(theta, theta+1), lines)

            # update file name
            filename_regex = 'CollectData\.FileName .+\n'
            filename_write = 'CollectData.FileName COMPTEL{}MeV_{}deg\n'
            lines = re.sub(filename_regex, filename_write.format(E, theta), lines)
            """ """ """ """ """ """""""" END OF SECTION """"""" """ """ """ """ """
            output_dir = os.path.join(sim_dir,
                                      'COMPTEL{}MeV_{}deg'.format(E, theta))
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            os.chdir(output_dir)

            with open(source_file_path, 'w') as out_file:
                out_file.write(lines)
            print('Simulating COMPTEL\'s response to {}MeV neutrons at {} degrees...'.format(E, theta))

            # run Cosima
            for i in range(trials):
                subprocess.run(['cosima', source_file_path])


if __name__ == '__main__':

    run_sims()
