# -*- coding: utf-8 -*-
"""
Created on Sun Apr 17 02:56:40 2016

@author: tessa
"""

import os
import re
import numpy as np
from numpy import sqrt, sin, cos, tan, arccos, arctan
from scipy.constants import pi, m_n, kilo, eV
from scipy import stats
import matplotlib.pyplot as plt



def NE213detector_efficiency(sim_directory, plot=False):

    particle_count_re = re.compile(r"""
        (?<=^TS\s)                  # +lookbehind "TS" starts line
        (\d+?$)                     # capture number
        """, re.X | re.MULTILINE)

    triggered = 20000
    detector_area = pi * 12.75**2
    start_area = pi * 12.75**2

    for i, file in enumerate(os.listdir(sim_directory)):
        with open(sim_directory+file, 'r') as fh:
            simfile = fh.read()
        # total number of incident particles
        particle_count = float(particle_count_re.search(simfile).group(0))
        effective_area = start_area * (triggered / particle_count)
        efficiency = (effective_area / detector_area)*100

        print("""{}: {} particles started, effective area is {}, and
                {} efficiency.\n\n""".format(file, particle_count, effective_area, efficiency))

    #error = stats.sem(efficiency)


    return


def COMPTEL_efficiency(triggered, plot=False):

    simulated_particles = 1000000

    # measurements from simulation geometry files
    s = 16         # number of sides of scintillator's polygon volume
    R = 13.47      # apothem of scintillator's polygon volume
    r = 250        # radius of "surrounding sphere"
    # calculate geometric area of detector (here, area of D1 scintillators)
    detector_area = R**2 * s * tan(pi / s) * 7
    # calculate area from which neutrons are being started
    start_area = pi * r**2
    # calculate effective area of COMPTEL for neutrons
    effective_area = start_area * (triggered / simulated_particles)

    # calculate detector efficiency
    efficiency = (effective_area / detector_area)*100

    # O'Neill efficiency data
    comp_energy = [17.2, 22, 35.7, 77]
    comp_eff = [.127, .144, .08, .053]
    err = [.005, .006, .004, .004]

    if plot:
        plt.plot((energy / 1000), efficiency, marker='o', linestyle='None')
        plt.hold(True)
        plt.errorbar(comp_energy, comp_eff, yerr=err, fmt='.')
        plt.ylabel('Efficiency (%)')
        plt.xlabel('Energy (MeV)')
        plt.title('Detector Efficiency')
        plt.grid(True)
        plt.show()

    return

if __name__ == '__main__':
    from Cosima_data.standard_output import standard_output
    output = standard_output('/Volumes/MORGAN/newCOMPTEL_simulation_data/77MeV/')
