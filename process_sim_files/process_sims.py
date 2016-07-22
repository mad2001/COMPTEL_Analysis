# -*- coding: utf-8 -*-
"""Process the sim files.

Created: Tue Jun 30 09:23:38 2015
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""

import os
import re
import glob
import pickle
import pandas as pd

from read_sims import pull_simdata
import transform_data as tr


def process_file(sim_file):

    # the Data object defined in read_sims module
    data = pull_simdata(sim_file)

    file_name = re.search('(?<=/)[\w]+?(?=\.inc)', sim_file).group(0)
    data.angle = int(re.search('[\d]{1,3}(?=deg)', sim_file).group(0))

    # the DataFrame of interaction data
    sim_data = data.hits

    # change detector ID to format that identifies detector and module
    sim_data['DetectorID'] = sim_data.apply(tr.identify_COMPTELmodule, axis=1)

    # convert to electron equivalent
    sim_data['Energy'] = sim_data.apply(tr.electron_equivalent, axis=1)

    sim_data = tr.create_hits(sim_data)
    sim_data = tr.broaden(sim_data)
    # hits.plot(x='x', y='y', kind='scatter')
    sim_data = tr.identify_triggers(sim_data)

    return data


def standard_output(sim_files):
    """Create the Hits object, then save it in a directory.

    Input is the full path to a Cosima simulation file, or a directory
    containing Cosima simulation files. If a directory is provided, all *.sim
    files should be from simulations of the same incident energy.
    """

    if os.path.isfile(sim_files):
        out_dir = os.path.join(os.path.dirname(os.path.dirname(sim_files)), 'processed_data')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        data = process_file(sim_files)

        filename = os.path.join(out_dir, 'COMPTEL{}MeV_{}deg'.format(
                                int(data.incident_energy / 1000), data.angle))

        with open(filename, 'wb') as f:
            pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

    if os.path.isdir(sim_files):
        out_dir = os.path.join(os.path.dirname(sim_files), 'processed_data')
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)

        for dirName, subdirList, fileList in os.walk(sim_files):

            filename = os.path.join(out_dir, os.path.basename(dirName))
            if os.path.exists(filename):
                continue

            sims = glob.glob(dirName + '/*.sim')

            if sims:
                data = process_file(sims[0])

                for s in sims[1:]:
                    data.combine(s)

                with open(filename, 'wb') as f:
                    pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)


if __name__ == '__main__':
    import sys
    standard_output(sys.argv[1])
