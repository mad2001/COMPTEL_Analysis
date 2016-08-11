"""Data from simulation is transformed into detector output format.

Functions
---------
    identify_COMPTELmodule -- Takes an interaction data row and determines the
        detector module where the interaction took place

    create_hits -- Takes the simulation data and aggregates it into 'hits'. The
        position is averaged (weighted by energy), time is averaged, and energy
        is summed. Data that is no longer needed is discarded.

    broaden -- Takes the hits and broadens energy and position based on the
        detector resolution.

    identify_triggers -- Identifies events that meet trigger criteria; elimates
        those that meet veto critera

Created: Fri Jun 26 11:31:42 2015
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""
import numpy as np
import pandas as pd

import process_sims
from geometry import *


# lists containing modules in each detector layer
d1 = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
d2 = [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11,
      2.12, 2.13, 2.14]
veto_domes = [3.1, 3.2, 3.3, 3.4]


class Trigger_Tracker(object):

    def __init__(self, type1, type2, type3):
        self.type1 = type1
        self.type2 = type2
        self.type3 = type3

    def output(self):
        print('Type 1 triggers: {}'.format(self.type1))
        print('Type 2 triggers: {}'.format(self.type2))
        print('Type 3 triggers: {}'.format(self.type3))


def identify_COMPTELmodule(sim_data):
    """Use hit location and detector type in order to detemine detector module.

    Paramerters
    -----------
        sim_data -- a row of a DataFrame containing the information of a
                neutron interaction
                (expected to be used with "apply" method of DataFrame)

    Returns
    -------
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
                if module.check_point(position):
                    return module.id
        # check each D2 module if in lower half
        elif sim_data['z'] < 5:
            for module in d2_modules:
                if module.check_point(position):
                    return module.id
        else:
            print('Error in D1 or D2 module definition')
    # if detector is Cosima scintillator (ID: 4)
    #       these are the veto domes
    elif sim_data['DetectorID'] == 4:
        # check Veto Domes 1 and 2 if in upper half
        if sim_data['z'] > 5:
            if VD1.check_point(position):
                return VD1.id
            elif VD2.check_point(position):
                return VD2.id
            else:
                print("Error in Veto Dome 1 or 2 definition")
        # check Veto Domes 3 and 4 if in lower half
        elif sim_data['z'] < 5:
            if VD3.check_point(position):
                return VD3.id
            elif VD4.check_point(position):
                return VD4.id
            else:
                print("Error in Veto Dome 3 or 4 definition")
    elif sim_data['DetectorID'] == 0:
        return 0
    else:
        print("Error in geometry definition")
        return 99


def electron_equivalent(sim_data):
    """Convert the particle's kinetic energy into its electron equivalent.

    Light output from R. A. Cecil et al.,
    "Improved Predictions of Neutron Detection..."
    """
    # convert energy to MeV
    energy = sim_data['Energy'] * 0.001
    particle = sim_data['ParticleID']
    detectorID = sim_data['DetectorID']

    # if electron/positron
    if particle == 2 or particle == 3:
        return energy * 1000

    # if particle is alpha or He-3
    elif particle == 21 or particle == 20:
        if detectorID in d1 or detectorID in veto_domes:
            a_1 = 0.42
            a_2 = 5.9
            a_3 = 0.065
            a_4 = 1.01
            energy = a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))
            return energy * 1000
        elif detectorID in d2:
            return energy * 1000

    # if particle is proton, deuteron, or triton
    elif particle == 4 or particle == 18 or particle == 19:
        # if interaction is in D1 layer (NE-213)
        if detectorID in d1:
            a_1 = 0.83
            a_2 = 2.82
            a_3 = 0.25
            a_4 = 0.93
            energy = a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))
            return energy * 1000
        # if interaction is in D2 layer (NaI)
        elif detectorID in d2:
            return energy * 1000
        # if interaction is in veto dome (using NE-102 instead of NE-110)
        elif detectorID in veto_domes:
            a_1 = 0.95
            a_2 = 8.0
            a_3 = 0.1
            a_4 = 0.90
            energy = a_1 * energy - a_2 * (1.0 - np.exp(-a_3 * energy**a_4))
            return energy * 1000
    else:
        # particle is likely heavy nucleus with neglible light output
        # or uncharged particle
        return 0


def create_hits(sim_data):
    """Turn the raw sim data into 'hits'; closer to detector output."""
    # create groups of interactions occurring in the same module
    # filter out those that deposit no energy
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
    """Broaden the position and energy based on the detector's resolution."""
    def d1energy_resolution(module):
        """Create function that calculate each D1 module's energy resolution.

        The D1 layer's energy resolution depends on both the specific module
        and the energy of the interaction. d1energy_resolution returns a
        function based on the module so that only energy input is needed.

        Energy must be in units of keV.
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

    def broaden_d2energy(energy):
        """Return broadened energy for D2.

        Uses numpy broadening function with input energy and accepted D2 energy
        resolution which is a function of energy.

        Energy must be in units of MeV.
        """
        # convert from keV to MeV
        energy = energy / 1000

        try:
            sigma = 0.01 * np.sqrt(9.86 * energy + 4.143 * energy**2)
            return np.random.normal(energy, sigma) * 1000

        # accounts for possibility of all energy values being zero
        except ValueError:
            return energy

    def broaden(x):
        """Broaden the input by an assigned sigma."""
        return np.random.normal(x, sigma_xy)

    # go through each module type and broaden position and energy
    for DetectorID, group in hits.groupby(level='DetectorID'):
        if DetectorID in d1:
            sigma_xy = 1.6
            hits.loc[(slice(None), DetectorID), 'x'] = group.x.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'y'] = group.y.apply(broaden)
            hits.loc[(slice(None), DetectorID), 'z'] = 102.35

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
    """Identify interactions that would trigger COMPTEL.

    Basic Functionality
    -------------------
        if not (one D1 hit and one D2 hit):
            delete

        if ('triggers' and not 'vetos'):
            save
    """
    # select parameters
    d1_min = 65
    d2_min = 600
    tof_max = 40.7e-9

    tracked = Trigger_Tracker(0, 0, 0,)

    def COMPTEL_filters(event):
        """Go through each event and determines whether or not it is a hit."""

        idx = event.index.get_level_values('DetectorID')

        # true if there is one hit in D1 and one hit in D2
        good_path = idx.isin(d1).sum() == 1 and idx.isin(d2).sum() == 1

        # true if energy deposited in D1 and D2 are above the energy minimums
        energy_thrshld = all(event.Energy[idx.isin(d1)] > d1_min) and all(
            event.Energy[idx.isin(d2)] > d2_min)

        def veto_check(event, idx):
            """ Determines whether or not a veto dome was triggered.

            Returns True if a veto dome is trigged.
            """
            if not any(idx.isin(veto_domes)):
                return False
            elif any(idx.isin([3.1])):
                return VD1.check_veto(event.loc[(slice(None), 3.1),
                                                'Energy'].values)
            elif any(idx.isin([3.2])):
                return VD2.check_veto(event.loc[(slice(None), 3.2),
                                                'Energy'].values)
            elif any(idx.isin([3.3])):
                return VD3.check_veto(event.loc[(slice(None), 3.3),
                                                'Energy'].values)
            elif any(idx.isin([3.4])):
                return VD4.check_veto(event.loc[(slice(None), 3.4),
                                                'Energy'].values)

        if good_path:
            # initialized here as only makes sense if there is a hit in D1 and D2
            global tof      # "time of flight"
            # tof is the time of the D2 hit minus the time of the D1 hit
            tof = event.ElapsedTime[idx.isin(d2)].sub(
                event.ElapsedTime[idx.isin(d1)].values)
            # broaden tof
            tof = np.random.normal(tof, 1e-9)

            if energy_thrshld and (0 < tof < tof_max):
                pass
            else:
                tracked.type2 += 1
                return False
        else:
            tracked.type1 += 1
            return False

        if veto_check(event, idx):
            tracked.type3 += 1
            return False
        else:
            return True

    hits = hits.groupby(level='EventID').filter(COMPTEL_filters)

    d1_data = hits.select(lambda x: x[1] in d1)
    d2_data = hits.select(lambda x: x[1] in d2)

    # this works but is a bad way to handle time of flight
    # need to calculate and broaden same time as other values
    tof = d2_data['ElapsedTime'].sub(d1_data['ElapsedTime'].values)
    tracked.output()

    return pd.DataFrame({'D1Energy': d1_data.Energy.values,
                         'x_1': d1_data.x.values,
                         'y_1': d1_data.y.values,
                         'z_1': d1_data.z.values,
                         'D2Energy': d2_data.Energy.values,
                         'x_2': d2_data.x.values,
                         'y_2': d2_data.y.values,
                         'z_2': d2_data.z.values,
                         'TimeOfFlight': tof}
                        ).reset_index(level='DetectorID', drop=True)
