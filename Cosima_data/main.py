# -*- coding: utf-8 -*-
"""
Created: Tue Jun 30 09:23:38 2015

Author: Morgan A. Daly
"""

import numpy as np
import readsimfile as rd
from defining_volumes import identify_COMPTELmodule

def main():

    # convert *.sim file to ndarray of data
    simulation = rd.main()
    sim = rd.Interaction(simulation)
    # change detector ID to format that identifies detector and module
    for i, interaction in np.ndenumerate(sim):
        sim.detector_id[i] = identify_COMPTELmodule(
                (sim.position[i]), sim.detector_id[i])

     convert to electron equivalent

sim = rd.main()


new = np.array(sim, dtype=labels)
