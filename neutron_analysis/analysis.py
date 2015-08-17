# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:25:55 2015

Author: Morgan A. Daly


@todo WRITE DOCSTRINGS

"""

import numpy as np
from numpy import sqrt, sin, cos, tan, arccos, arctan
from scipy.constants import pi, m_n, kilo, eV
import matplotlib.pyplot as plt


def efficiency(data, plot=False):

    simulated_particles = data[1]
    triggered = data[2]

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

    if plot:
        energy = data[0]
        plt.plot(energy, efficiency)
        plt.ylabel('Efficiency (%)')
        plt.xlabel('Energy (MeV)')
        plt.title('Detector Efficiency')
        plt.grid(True)
        plt.show()

    return efficiency


def angular_res(data, inplace=False):

    phi_src = 0
    theta_src = 0

    distance = np.linalg.norm(data[['x_2', 'y_2', 'z_2']].values -
                    data[['x_1', 'y_1', 'z_1']].values, axis=1)

    # calculate classical kinetic energy
    E_n = .5 * m_n * (distance / data['TimeOfFlight'].values)

    # measured scattered angle derived from n-p scattering kinematics
    phi_measured = arccos(sqrt(data['D1Energy'].values * eV / (E_n * kilo)))

    # calculate geometric scatter angle
    a = (data['x_1'] - data['x_2']) / distance
    b = (data['y_1'] - data['y_2']) / distance
    c = (data['z_2'] - data['z_1']) / distance
    theta_scttrd = arccos(c)
    phi_scttrd = 360 - arctan(b / a)

    phi_geo = arccos(cos(theta_scttrd) * cos(theta_src) + sin(theta_scttrd)
                * sin(theta_src) * cos(phi_scttrd - phi_src))

    if inplace:
        data['arm'] = phi_measured - phi_geo
        return data
    else:
        return phi_measured - phi_geo
