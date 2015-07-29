# -*- coding: utf-8 -*-
"""
Created: Tue Jun 30 09:23:38 2015

Author: Morgan A. Daly
"""

import readsimfile
import defining_volumes as vol
import transform_data


filename = "COMPTELeffA_22MeV.inc1.id1.sim"


def main(filename):

    # convert *.sim file to Pandas data frame
    sim_data = readsimfile.return_simdata(filename)

    # change detector ID to format that identifies detector and module
    sim_data['DetectorID'] = sim_data.apply(vol.identify_COMPTELmodule, axis=1)

    # convert to electron equivalent
    sim_data['Energy'] = sim_data.apply(transform_data.electron_equivalent, axis=1)

    hits = transform_data.create_hits(sim_data)
    hits = transform_data.broaden(hits)

    return hits

data = main(filename)
# current wall time: 12.9 s
