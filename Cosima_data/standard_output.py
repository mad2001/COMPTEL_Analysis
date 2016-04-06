# -*- coding: utf-8 -*-
"""
Created: Tue Jun 30 09:23:38 2015

Author: Morgan A. Daly
"""

import os
import pandas as pd
from .readsimfile import pull_simdata
from . import transform_data as tr


def standard_output(sim_files):

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

        hits = tr.create_hits(sim_data)
        hits = tr.broaden(hits)
        #hits.plot(x='x', y='y', kind='scatter')
        hits = tr.identify_triggers(hits)

    if os.path.isdir(sim_files):

        files = os.listdir(sim_files)
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
        #hits.plot(x='x', y='y', kind='scatter')
        hits = [tr.identify_triggers(hits)]

        for i, file in enumerate(files[1:]):


            data = pull_simdata(file[i])

            sim_data = data['data']


            if data['incident energy'] != incident_energy:
                print('Files in directory do not use the same neutron energy.')

            particle_count += data['particle count']

            # change detector ID to format that identifies detector and module
            sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

            # convert to electron equivalent
            sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

            temp_hits = tr.create_hits(sim_data)
            temp_hits = tr.broaden(temp_hits)
            #hits.plot(x='x', y='y', kind='scatter')
            hits.append(tr.identify_triggers(temp_hits))

        # concatenate all "hits" data frames in list
        hits = pd.concat(hits)


    return {'hits': hits,
            'incident energy': incident_energy,
            'particle count': particle_count,
            'triggered': len(hits.index)}

# current wall time: 15.6 s
