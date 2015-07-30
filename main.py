# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:26:40 2015

Author: Morgan A. Daly
"""

import os

import Cosima_data.main
import neutron_analysis
from Cosima_data.readsimfile import particle_count
from Cosima_data.transform_data import triggered_events


def main(filename):

    Cosima_data.main.main(filename)

    neutron_analysis.effective_area(particle_count, triggered_events)



for filename in os.listdir('COMPTEL Research/Simulations'):
    main(filename)
