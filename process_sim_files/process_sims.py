# -*- coding: utf-8 -*-
"""Process the sim files.

Created: Tue Jun 30 09:23:38 2015
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""

import os
import glob
import pickle
import pandas as pd

from read_sims import pull_simdata
import transform_data as tr


class Data:
    """Class to contain data from processed simulation file."""

    def __init__(self, hits, particle_count, incident_energy):
        self.hits = hits
        self.particle_count = particle_count
        self.incident_energy = incident_energy
        self.triggered_events = len(hits.index)


def standard_output(sim_files):
    """Create the Hits object, then save it in a directory.

    Input is the full path to a Cosima simulation file, or a directory
    containing Cosima simulation files. If a directory is provided, all *.sim
    files should be from simulations of the same incident energy.
    """
    if os.path.isfile(sim_files):
        # convert *.sim file to Pandas data frame
        data = pull_simdata(sim_files)

        sim_data = data['data']
        particle_count = data['particle count']
        incident_energy = data['incident energy']

        # change detector ID to format that identifies detector and module
        sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

        # convert to electron equivalent
        sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

        hits_df = tr.create_hits(sim_data)
        hits_df = tr.broaden(hits_df)
        # hits.plot(x='x', y='y', kind='scatter')
        hits_df = tr.identify_triggers(hits_df)

        # convert into the "hits" object
        data = Data(hits_df, particle_count, incident_energy)

    if os.path.isdir(sim_files):

        files = glob.glob(sim_files + '*.sim')
        data = pull_simdata(files[0])
        sim_data = data['data']
        particle_count = data['particle count']
        incident_energy = data['incident energy']

        # change detector ID to format that identifies detector and module
        sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

        # convert to electron equivalent
        sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

        hits = tr.create_hits(sim_data)
        hits = tr.broaden(hits)
        # hits.plot(x='x', y='y', kind='scatter')
        hits = [tr.identify_triggers(hits)]

        for i, file in enumerate(files[1:]):
            data = pull_simdata(file)
            sim_data = data['data']

            # error catching
            if data['incident energy'] != incident_energy:
                print('Files in directory do not use the same neutron energy.')

            particle_count += data['particle count']

            # change detector ID to format that identifies detector and module
            sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

            # convert to electron equivalent
            sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

            temp_hits = tr.create_hits(sim_data)
            temp_hits = tr.broaden(temp_hits)
            # hits.plot(x='x', y='y', kind='scatter')
            hits.append(tr.identify_triggers(temp_hits))

        # concatenate all "hits" data frames in list
        hits_df = pd.concat(hits)
        # convert into the "Hits" object
        data = Data(hits_df, particle_count, incident_energy)

    # hits.to_csv('COMPTEL_dataframe_{}MeV'.format(incident_energy/1000))
    with open('COMPTEL_{}MeV'.format(incident_energy / 1000), 'wb') as f:
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

# current wall time: 15.6 s
