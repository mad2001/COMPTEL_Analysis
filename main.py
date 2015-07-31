# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:26:40 2015

Author: Morgan A. Daly
"""

import os

import numpy as np

import Cosima_data.main
from Cosima_data.readsimfile import particle_count, incident_energy
from Cosima_data.transform_data import triggered_events
from neutron_analysis.detector_efficiency import efficiency
from neutron_analysis.plotting import plot_efficiency


files = os.listdir('COMPTEL Research/Simulations')

efficiency_data = np.empty([len(files), 3])

for filename, i in enumerate(files):
    Cosima_data.main.main(filename)
    efficiency_data[i, :] = [incident_energy, particle_count, triggered_events]

eff = efficiency(efficiency_data[1], efficiency_data[2])

plot_efficiency(efficiency_data[0], eff)
