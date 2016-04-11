# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 11:54:48 2015

@author: Morgan
"""

import os

import numpy as np

from summer_research.Cosima_data import standard_output
import summer_research.neutron_analysis.analysis as ay

#
#if __name__ == '__main__':
#    files = os.listdir('COMPTEL Research/Simulations')
#
#    efficiency_data = np.empty([len(files), 3])
#
#    for filename, i in enumerate(files):
#        data = standard_output.standard(filename)
#        efficiency_data[i, :] = [data['incident energy'], data['particle_count'], data['triggered']]
#
#    eff = efficiency(efficiency_data, plot=True)


if __name__ == '__main__':
    filename = "summer_research/Cosima_data/COMPTELeffA_22MeV.inc1.id1.sim"
    data = standard_output.standard(filename)
    efficiency_data = [data['incident energy'], data['particle count'], data['triggered']]
    eff = ay.efficiency(efficiency_data, plot=True)
    output = ay.angular_res(data['hits'], inplace=True)
