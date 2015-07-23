# -*- coding: utf-8 -*-


"""
Created: Fri Jun 26 11:31:42 2015

Author: Morgan A. Daly
"""

"""
STEP ONE ------> DONE
    change to electron equivalent energy
STEP TWO  ------> DONE
    weighted averages
STEP THREE
    broadening

Position
    D1xy
        position is the weighted overage of the x/y locations by energy loss
        broaden these positions by the spatial resolation (1 sig is 1.6cm)
    D1z
        equal to middle of z

    D2xy
        position is the weighted overage of the x/y locations by energy loss
        broaden these positions by the spatial resolation (1 sig is 1.4cm)
    D2z
        equal to middle of z

Time of Flight

Energy Loss
    D1
    D2
    V1
    V2
    V3
    V4

"""
from math import sqrt

import numpy as np
import pandas as pd


def create_hits(sim_data):
    # a hit is a collection of interaction in one module
    #   take sum of Eeee
    #   weighted average: x, y, z,
    #   unweighted average: hit time
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
    hits = hits.drop(hits.loc[(slice(None), 0.00), :], axis=0)

    return hits




def broaden(hits):
    """
    The reason this is so ungly is that in order to actually change the data
    frame, the values being changed must be altered very explicitly.

    Srry tessa
    """

    broaden = lambda x: np.random.normal(x, sigma_xy)


    def d1energy_resolution(module):

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
        return lambda x: A + (B * sqrt(x))


    def broaden_d1energy(energy):
        try:
            return np.random.normal(energy, energyres_function(energy))
        except ValueError:
            return energy


    def broaden_d2energy(energy):
        try:
            return np.random.normal(energy, (1.28 * energy + 3.6 * energy **2))
        except ValueError:
            return energy


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
        # if in veto domes
        elif 3 < DetectorID < 4:
            continue
        else:
            continue
    return hits






