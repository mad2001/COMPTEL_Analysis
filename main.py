# -*- coding: utf-8 -*-
"""
Created: Thu Aug 13 11:10:10 2015

Author: Morgan A. Daly
"""

import os

import numpy as np

from summer_research.Cosima_data import standard_output

import summer_research.neutron_analysis.analysis as ay


#
#files = os.listdir('Simulations')
#filename = files[4]
#data = standard_output.standard(os.path.join('Simulations', filename))



if __name__ == '__main__':

    files = os.listdir('Simulations')
    files = files[5]

#    efficiency_data = np.empty([len(files), 3])
#    for i, filename in enumerate(files):
    data = standard_output.standard(os.path.join('Simulations', files))
    #efficiency_data[i, :] = [data['incident energy'], data['particle count'], data['triggered']]
    print(i)
    print(filename)
    ay.energy_res(data['hits'])
    ay.angular_res(data['hits'])
    # to save data
        #data['hits'].to_csv(filename + '_output')

    #eff = ay.efficiency(efficiency_data, plot_effa=True)
    #eff.to_csv('efficiency_output')


#if __name__ == '__main__':
#    filename = 'COMPTELeffA_22MeV.inc1.id1.sim'
##    os.path.join('COMPTEL Research', filename)
#    data = standard_output.standard(filename)
#    efficiency_data = [data['incident energy'], data['particle count'], data['triggered']]
#    eff = ay.efficiency(efficiency_data, plot=True)


