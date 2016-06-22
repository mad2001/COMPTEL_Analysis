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
    source_file_path = '/Some/Path/Name'
    sim_dir = '/Volumes/MORGAN/newCOMPTEL_simulation_data'
    trials = 2

    """ """ """ """ """ PROVIDE ENERGY AS A LIST """ """ """ """ """
    #energy = [1, 5, 15, 30, 55, 100]

    """ """ """ """ """ PROVIDE ENERGY AS A RANGE """ """ """ """ """
    low_energy = 1      # lowest energy simulated (in MeV)
    high_energy = 100   # highest energy simulated (in MeV)
    energy_step = 5     # interval
    energy = [x for x in range(low_energy, high_energy, energy_step)]

    # change to *.sim file directory
    if not os.path.exists(sim_dir):
        os.makedirs(sim_dir)
    os.chdir(sim_dir)

    source_dir, source_file = os.path.split(source_file_path)
    with open(source_file_path, 'r') as in_file:
        # creates a list with each line in source file as an element
        lines = in_file.readlines()

    for E in energy:
        """ """ """  THIS SECTION SHOULD BE EDITED BEFORE RUNNING  """ """ """
        # update file name
        line1_regex = 'CollectData\.FileName COMPTELdata_\d+.?\d*MeV\n'
        line1_write = 'CollectData.FileName COMPTELdata_{}MeV\n'
        lines = re.sub(line1_regex, line1_write.format(E), lines)

        # update incident energy (changing from MeV to keV)
        line2_regex = 'neutron\.Spectrum Mono \d+.?\d*\n'
        line2_write = 'neutron.Spectrum Mono {}\n'
        lines = re.sub(line2_regex, line2_write.format(E * 1000), lines)
        """ """ """ """ """ """""""" END OF SECTION """"""" """ """ """ """ """

        with open(source_file_path, 'w') as out_file:
            out_file.write(lines)

        # run Cosima
        for i in range(trials):
            subprocess.run('cosima ' + source_file_path,
                           universal_newlines=True,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           shell=True)


if __name__ == '__main__':
    # adjust parameters within the function itself
    run_sims()
