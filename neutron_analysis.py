# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:25:55 2015

Author: Morgan A. Daly


@todo WRITE DOCSTRINGS

"""

from scipy.stats import norm
import matplotlib.mlab as mlab
import numpy as np
from numpy import sqrt, sin, cos, arccos, arctan
from scipy.constants import pi, m_n, kilo, eV
import matplotlib.pyplot as plt


def efficiency(data, plot=False):

    detector_area = 4042.1739633515281
        # 7 D1 scintillators
        # modeled as 16 sided polygons with an apothem of 13.47
        # detector area comes from (13.47^2)(16)(tan(pi/16))

    surrounding_sphere_radius = 250
    start_area = pi * surrounding_sphere_radius**2

    # calculate effective area of COMPTEL for neutrons
    effective_area = start_area * (data.triggered_events / data.particle_count)

    # calculate detector efficiency
    efficiency = (effective_area / detector_area)*100

    # O'Neill efficiency data
    comp_energy = [17.2, 22, 35.7, 77]
    comp_eff = [.127, .144, .08, .053]
    err = [.005, .006, .004, .004]

    if plot:
        energy = data[:, 0]
        plt.plot((energy / 1000), efficiency, marker='o', linestyle='None')
        plt.hold(True)
        plt.errorbar(comp_energy, comp_eff, yerr=err, fmt='.')
        plt.ylabel('Efficiency (%)')
        plt.xlabel('Energy (MeV)')
        plt.title('Detector Efficiency')
        plt.grid(True)
        plt.show()

    return efficiency


def energy_dist(data, plot=False):

    # normal vector from point in D1 to point in D2
    distance = (np.linalg.norm(data.hits[['x_2', 'y_2', 'z_2']].values -
                               data.hits[['x_1', 'y_1', 'z_1']].values, axis=1)) * .01

    # calculate classical kinetic energy in joules
    E_n = .5 * m_n * ((distance / data['TimeOfFlight'].values) ** 2)
    # convert to keV
    E_n = E_n / (eV * kilo)
    tot_energy = E_n + data['D1Energy'].values

    if plot:
        # best fit of data
        (mu, sigma) = norm.fit(tot_energy)

        # the histogram of the data
        n, bins, patches = plt.hist(tot_energy, bins=30, facecolor='blue')

        # add a 'best fit' line
        y = mlab.normpdf( bins, mu, sigma)
        l = plt.plot(bins, y, 'r--', linewidth=2)

        #plot
        plt.xlabel('Energy (keV)')
        plt.ylabel('Counts')
        plt.title(r'$\mathrm{\Energy \Spectrum:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
        plt.grid(True)

        plt.show()

    return E_n


def angular_res(data, inplace=False, plot=False):

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
        data['NeutronKE'] = E_n
        data['arm'] = phi_measured - phi_geo
        return data

    if plot:
        # best fit of data
        (mu, sigma) = norm.fit(data['arm'])

       # the histogram of the data
        n, bins, patches = plt.hist(data['arm'], bins=25, facecolor='blue')

        # add a 'best fit' line
        y = mlab.normpdf( bins, mu, sigma)
        l = plt.plot(bins, y, 'r--', linewidth=2)

        #plot
        plt.xlabel('Energy (MeV)')
        plt.ylabel('Counts')
        plt.title(r'$\mathrm{ARM:}\ \mu=%.3f,\ \sigma=%.3f$' %(mu, sigma))
        plt.grid(True)

        plt.show()

    else:
        return phi_measured - phi_geo
