# -*- coding: utf-8 -*-
"""
Created: Tue Jun 30 09:23:38 2015

Author: Morgan A. Daly
"""

import numpy as np
import pandas as pd
import readsimfile as rd
from defining_volumes import *


filename = "COMPTELeffA_22MeV.inc1.id1.sim"

def main(filename):

    # convert *.sim file to data frame
    sim_data = rd.return_simdata(filename)

    # change detector ID to format that identifies detector and module
    sim_data['DetectorID'] = sim_data.apply(identify_COMPTELmodule, axis=1)

    return sim_data
#     convert to electron equivalent


