# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:25:55 2015

Author: Morgan A. Daly

"""
import numpy as np
import matplotlib.pyplot as plt


def efficiency(data, plot=False):

    simulated_particles = data[1]
    triggered = data[2]

    # measurements from simulation geometry files
    s = 16         # number of sides of scintillator's polygon volume
    R = 13.47      # apothem of scintillator's polygon volume
    r = 250        # radius of "surrounding sphere"
    # calculate geometric area of detector (here, area of D1 scintillators)
    detector_area = R**2 * s * np.tan(np.pi / s) * 7
    # calculate area from which neutrons are being started
    start_area = np.pi * r**2
    # calculate effective area of COMPTEL for neutrons
    effective_area = start_area * (triggered / simulated_particles)

    # calculate detector efficiency
    efficiency = (effective_area / detector_area)*100

    if plot:
        energy = data[0]
        plt.plot(energy, efficiency)
        plt.ylabel('Efficiency (%)')
        plt.xlabel('Energy (MeV)')
        plt.title('Detector Efficiency')
        plt.grid(True)
        plt.show()

    return efficiency
