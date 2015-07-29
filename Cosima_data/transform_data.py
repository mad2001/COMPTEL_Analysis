# -*- coding: utf-8 -*-


"""
Created: Fri Jun 26 11:31:42 2015

Author: Morgan A. Daly


Data from simulation is transformed into detector output format.

create_hits:: Takes the simulation data and aggregates it into 'hits'. The
    position is averaged (weighted by energy), time is averaged, and energy is
    summed. Data that is no longer needed is discarded.

broaden:: Takes the hits and broadens energy and position based on the detector
    resolution.

"""
import math

import numpy as np


def electron_equivalent(sim_data):
    """
    Converts the particle's kinetic energy into its electron equivalent

    Light output from O'Neill et al. and R. A. Cecil et al.
    R. A. Cecil et al., "Improved Predictions of Neutron Detection..."
    """

    energy = sim_data['Energy']
    particle = sim_data['NewParticleID']

    # lists containing modules in each detector layer
    d1 = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
    d2 = [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11,
          2.12, 2.13, 2.14]
    veto_domes = [3.1, 3.2, 3.3, 3.4]

    # if gamma ray
    if particle == 1:
        return energy

    # if particle is alpha or He-3
    elif particle == 21 or particle == 20:
        a_1 = 0.41
        a_2 = 5.9
        a_3 = 0.065
        a_4 = 1.01
        return a_1 * energy - a_2 * (1.0 - math.exp(-a_3 * energy**a_4))

    # if particle is proton, deuteron, or triton
    elif particle == 4 or particle == 18 or particle == 19:
        # if interaction is in D1 layer (NE-213)
        if sim_data['DetectorID'] in d1:
            a_1 = 0.83
            a_2 = 2.82
            a_3 = 0.25
            a_4 = 0.93
            return a_1 * energy - a_2 * (1.0 - math.exp(-a_3 * energy**a_4))
        # if interaction is in D2 layer (NaI)
        elif sim_data['DetectorID'] in d2:
            return energy
        # if interaction is in veto dome (using NE-102 instead of NE-110)
        elif sim_data['DetectorID'] in veto_domes:
            a_1 = 0.95
            a_2 = 8.0
            a_3 = 0.1
            a_4 = 0.90
            return a_1 * energy - a_2 * (1.0 - math.exp(-a_3 * energy**a_4))

    else:
        # particle is likely heavy nucleus with neglible light output
        return 0


def create_hits(sim_data):
    """
    This turns the raw sim data into 'hits'; closer to detector output.
    """
    sim_data.drop(sim_data.columns[[2, 10, 11]], axis=1, inplace=True)
    hits = sim_data

    # quick function to be used in aggregation
    def weighted_avg(x):
        try:
            return np.average(x, weights=hits.loc[x.index, 'Energy'])
        except ZeroDivisionError:
            return x[x.first_valid_index()]

    # aggregate data; this turns the individual interactions into 'hits'
    hits = hits.groupby(['EventID', 'DetectorID']).agg(
                    {'Incidents': lambda x: x[x.first_valid_index()],
                     'ElapsedTime': np.mean,
                     'x': lambda x: weighted_avg(x),
                     'y': lambda x: weighted_avg(x),
                     'z': lambda x: weighted_avg(x),
                     'Energy': np.sum})

    # drop data with Detector ID '0.00'; these are 'INIT' interactions and
    #   interactions in passive materials
    hits.drop(0.00, level="DetectorID", inplace=True)

    return hits


def broaden(hits):
    """
    Broaden the position and energy based on the detector's resolution.
    """

    def d1energy_resolution(module):
        """
        Creates function that calculates each D1 module's energy resolutioin.

        The D1 layer's energy resolution depends on both the specific module
        and the energy of the interaction. d1energy_resolution constructs a
        function based on the module so that only energy input is needed.
        """

        if module == 1.01:
            A = -1.022
            B = 1.749
        elif module == 1.02:
            A = -7.481
            B = 2.157
        elif module == 1.03:
            A = 2.944
            B = 1.723
        elif module == 1.04:
            A = -5.822
            B = 1.935
        elif module == 1.05:
            A = -3.073
            B = 1.892
        elif module == 1.06:
            A = -8.662
            B = 2.069
        elif module == 1.07:
            A = 0.020
            B = 1.890
        return lambda x: A + (B * np.sqrt(x))

    def broaden_d1energy(energy):
        """
        Returns broadened energy for D1.
        """

        try:
            return np.random.normal(energy, energyres_function(energy))
        # skips over issues where there is division by 0
        except ValueError:
            return energy

    def broaden_d2energy(energy):
        """
        Returns broadened energy for D2.

        Uses numpy broadening function with input energy and accepted D2 energy
        resolution which is a function of energy.
        """

        try:
            return np.random.normal(energy, (1.28 * energy + 3.6 * energy **2))
        # skips over issues where there is division by 0
        except ValueError:
            return energy

    broaden = lambda x: np.random.normal(x, sigma_xy)

    # go through each module type and broaden position and energy
    for DetectorID, group in hits.groupby(level='DetectorID'):
        # if in D1
        if 1 < DetectorID < 2:
            sigma_xy = 1.6
            hits.loc[(slice(None), DetectorID), 'x'] = group.x.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'y'] = group.y.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'z'] = 102.35
            energyres_function = d1energy_resolution(DetectorID)
            hits.loc[(slice(None), DetectorID), 'Energy'] = group.Energy.map(
                        lambda x: broaden_d1energy(x))
        # if in D2
        elif 2 < DetectorID < 3:
            sigma_xy = 1.4
            hits.loc[(slice(None), DetectorID), 'x'] = group.x.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'y'] = group.y.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'z'] = -55.65

            hits.loc[(slice(None), DetectorID), 'Energy'] = group.Energy.map(
                        lambda x: broaden_d2energy(x))
        else:
            continue
    return hits
