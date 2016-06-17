# -*- coding: utf-8 -*-


"""
Created: Fri Jun 26 11:31:42 2015
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)


Data from simulation is transformed into detector output format.

create_hits:: Takes the simulation data and aggregates it into 'hits'. The
    position is averaged (weighted by energy), time is averaged, and energy is
    summed. Data that is no longer needed is discarded.

broaden:: Takes the hits and broadens energy and position based on the detector
    resolution.

identify_triggers:: Identifies events that meet trigger criteria; elimates
    those that meet veto critera

"""
import numpy as np
import pandas as pd

from .defining_volumes import *


# lists containing modules in each detector layer
d1 = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
d2 = [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11,
      2.12, 2.13, 2.14]
veto_domes = [3.1, 3.2, 3.3, 3.4]


def identify_COMPTELmodule(sim_data):
    """
    Uses hit location and detector type in order to detemine detector module.

    Paramerters
    ------------
        sim_data -- a row of a DataFrame containing the information of a
                neutron interaction
                (expected to be used with "apply" method of DataFrame)

    Returns
    --------
        the the ID of the detector module that the interaction occurred in
            format is X.Y where:
            X-- 1: D1,  2: D2,  3: VetoDome
            Y-- module id

    """

    position = (sim_data['x'], sim_data['y'], sim_data['z'])

    # if detector is Cosima Anger camera (ID: 7)
    #       these are the D1 and D2 layers
    if sim_data['DetectorID'] == 7:
        # check each D1 module if in upper half
        if sim_data['z'] > 5:
            for module in d1_modules:
                if module.check_point(position): return module.id
        # check each D2 module if in lower half
        elif sim_data['z'] < 5:
            for module in d2_modules:
                if module.check_point(position): return module.id
        else:
            print('Error in D1 or D2 module definition')
    # if detector is Cosima scintillator (ID: 4)
    #       these are the veto domes
    elif sim_data['DetectorID'] == 4:
        # check Veto Domes 1 and 2 if in upper half
        if sim_data['z'] > 5:
            if VD1.check_point(position): return VD1.id
            elif VD2.check_point(position): return VD2.id
            else:
                print("Error in Veto Dome 1 or 2 definition")
        # check Veto Domes 3 and 4 if in lower half
        elif sim_data['z'] < 5:
            if VD3.check_point(position): return VD3.id
            elif VD4.check_point(position): return VD4.id
            else:
                print("Error in Veto Dome 3 or 4 definition")
    elif sim_data['DetectorID'] == 0:
        return 0
    else:
        print("Error in geometry definition")
        return 99


def electron_equivalent(sim_data):
    """
    Converts the particle's kinetic energy into its electron equivalent

    Light output from O'Neill et al. and R. A. Cecil et al.
    R. A. Cecil et al., "Improved Predictions of Neutron Detection..."
    """

    energy = sim_data['Energy']
    particle = sim_data['NewParticleID']

    # if electron/positron
    if particle == 2 or particle == 3:
        return energy

    # if particle is alpha or He-3
    elif particle == 21 or particle == 20:
        if sim_data['DetectorID'] in d1 or sim_data['DetectorID'] in veto_domes:
            a_1 = 0.42
            a_2 = 5.9
            a_3 = 0.065
            a_4 = 1.01
            return a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))
        elif sim_data['DetectorID'] in d2:
            return energy

    # if particle is proton, deuteron, or triton
    elif particle == 4 or particle == 18 or particle == 19:
        # if interaction is in D1 layer (NE-213)
        if sim_data['DetectorID'] in d1:
            a_1 = 0.83
            a_2 = 2.82
            a_3 = 0.25
            a_4 = 0.93
            return a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))
        # if interaction is in D2 layer (NaI)
        elif sim_data['DetectorID'] in d2:
            return energy
        # if interaction is in veto dome (using NE-102 instead of NE-110)
        elif sim_data['DetectorID'] in veto_domes:
            a_1 = 0.95
            a_2 = 8.0
            a_3 = 0.1
            a_4 = 0.90
            return a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))

    else:
        # particle is likely heavy nucleus with neglible light output
        # or uncharged particle
        return 0


def create_hits(sim_data):
    """
    This turns the raw sim data into 'hits'; closer to detector output.
    """

    # filter group
    hits = sim_data.groupby(['EventID', 'DetectorID']).filter(
            lambda x: x['Energy'].sum() != 0)

    # aggregate data; turns the individual interactions into 'hits'`
    hits = hits.groupby(['EventID', 'DetectorID']).agg(
                    {'ElapsedTime': np.mean,
                     'x': lambda x: np.average(x, weights=hits.loc[x.index, 'Energy']),
                     'y': lambda x: np.average(x, weights=hits.loc[x.index, 'Energy']),
                     'z': lambda x: np.average(x, weights=hits.loc[x.index, 'Energy']),
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

#    def broaden_d1energy(energy):
#        """
#        Returns broadened energy for D1.
#        """
#
#        try:
#            #return np.random.normal(energy, energyres_function(energy))
#            return np.random.normal(energy, (1.1 * energy ** .57))
#        # accounts for possibility of all energy values being zero
#        except ValueError:
#            return energy

    def broaden_d2energy(energy):
        """
        Returns broadened energy for D2.

        Uses numpy broadening function with input energy and accepted D2 energy
        resolution which is a function of energy.
        """

        try:
            # this is resolution that Mark gave
            return np.random.normal(energy, (1.28 * energy + 3.6 * energy **2))

           # not sure where this resolution came from?
            #return np.random.normal(energy, (1.72 * np.sqrt(energy) - 11.8))

       # accounts for possibility of all energy values being zero
        except ValueError:
            return energy

    # lambda function to be applied to position values for broadening
    broaden = lambda x: np.random.normal(x, sigma_xy)

    # go through each module type and broaden position and energy
    for DetectorID, group in hits.groupby(level='DetectorID'):

        if DetectorID in d1:
            sigma_xy = 1.6
            hits.loc[(slice(None), DetectorID), 'x'] = group.x.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'y'] = group.y.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'z'] = 102.35
            # CHANGED THIS FROM THE FUNCTION ABOVE, HOPEFULLY DOESN'T BREAK
            broaden_d1energy = d1energy_resolution(DetectorID)
            hits.loc[(slice(None), DetectorID), 'Energy'] = group.Energy.map(
                        lambda x: broaden_d1energy(x))

        elif DetectorID in d2:
            sigma_xy = 1.4
            hits.loc[(slice(None), DetectorID), 'x'] = group.x.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'y'] = group.y.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'z'] = -55.65

            hits.loc[(slice(None), DetectorID), 'Energy'] = group.Energy.map(
                        lambda x: broaden_d2energy(x))
        else:
            continue
    return hits


def identify_triggers(hits):

    """
    if triggers is true and vetos is false
        save

    if there is not one D1 hit and 1 D2 hit:
        delete
    if D1 < 50
    """
    import matplotlib.pyplot as plt

    # select parameters
    d1_min = 65
    d2_min = 600
    tof_max = 40.7e-9

    def filters(event):
        """
        Goes through each event and determines whether or not it is a hit.
        """

        idx = event.index.get_level_values('DetectorID')

        good_path = idx.isin(d1).sum() == 1 and idx.isin(d2).sum() == 1
        energy_thrshld = all(event.Energy[idx.isin(d1)] > d1_min) and all(
                    event.Energy[idx.isin(d2)] > d2_min)

        if good_path:
            global tof
            tof = event.ElapsedTime[idx.isin(d2)].sub(
                    event.ElapsedTime[idx.isin(d1)].values)
            tof = np.random.normal(tof, 1e-9)

            if energy_thrshld and (0 < tof < tof_max):
                pass
            else:
                return False
        else:
            return False

        veto1 = any(idx.isin([3.01])) and VD1.check_veto(event.Energy[3.01])
        veto2 = any(idx.isin([3.02])) and VD2.check_veto(event.Energy[3.02])
        veto3 = any(idx.isin([3.03])) and VD3.check_veto(event.Energy[3.03])
        veto4 = any(idx.isin([3.04])) and VD4.check_veto(event.Energy[3.04])

        if veto1 or veto2 or veto3 or veto4:
            return False

        else:
            return True

    hits = hits.groupby(level='EventID').filter(filters)

    d1_data = hits.select(lambda x: x[1] in d1)
    d2_data = hits.select(lambda x: x[1] in d2)

    tof = d2_data['ElapsedTime'].sub(d1_data['ElapsedTime'].values)
    """plt.figure()
    plt.hist(tof, bins=20)
    tof = np.random.normal(tof, 1e-9)
    plt.figure()
    plt.hist(tof, bins=20)"""

    return pd.DataFrame(
            {'D1Energy': d1_data.Energy.values,
             'x_1': d1_data.x.values, 'y_1': d1_data.y.values, 'z_1': d1_data.z.values,
             'D2Energy': d2_data.Energy.values,
             'x_2': d2_data.x.values, 'y_2': d2_data.y.values, 'z_2': d2_data.z.values,
             'TimeOfFlight': tof
             }).reset_index(level='DetectorID', drop=True)
