# -*- coding: utf-8 -*-
"""
Created: Tue Jun 30 09:23:38 2015

Author: Morgan A. Daly
"""

from .readsimfile import pull_simdata
from . import transform_data as tr


def standard(filename):

    # convert *.sim file to Pandas data frame
    data = pull_simdata(filename)
    sim_data = data['data']

    # change detector ID to format that identifies detector and module
    sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

    # convert to electron equivalent
    sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

    hits = tr.create_hits(sim_data)
    hits = tr.broaden(hits)
    hits = tr.identify_triggers(hits)

    return {'hits': hits,
            'incident energy': data['incident energy'],
            'particle count': data['particle count'],
            'triggered': hits.shape[0]}

# current wall time: 15.6 s
