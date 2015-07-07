# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 14:52:13 2015

@author: morgan

This is painfully brute forced I'm sorry @everyone
"""
import numpy as np

# The coordinates of the detectors as defined in the Geomega geometry
SETU_coords = (0, 0, -117.4)

# daughter of SETU
DET1_coords = (0, 0, 209.45)

# daughter of DET1
D1module_coords = np.empty(7))
D1module_coords[0] = (0, 0, 10.3)
D1module_coords[1] = (-42.3, 0, 10.3)
D1module_coords[2] = (-26, 39.1, 10.3)
D1module_coords[3] = (26, 39.1, 10.3)
D1module_coords[4] = (42.3, 0, 10.3)
D1module_coords[5] = (26, -39.1, 10.3)
D1module_coords[6] = (-26, -39.1, 10.3)

# daughter of SETU
DET2_coords = (0, 0, 52.1)
# daughter of each module
D2SN_coords = (0, 0, 14.3375)
# daughter of DET2
D2module_coords[0] = np.empty(14)
D2module_coords[1] = (30.2, -41.254, -4.6875)
D2module_coords[2] = (0, -41.254, -4.6875)
D2module_coords[3] = (45.3, -15.1, -4.6875)
D2module_coords[4] = (15.1, -15.1, -4.6875)
D2module_coords[5] = (-15.1, -15.1, -4.6875)
D2module_coords[6] = (-45.3, -15.1, -4.6875)
D2module_coords[7] = (45.3, 15.1, -4.6875)
D2module_coords[8] = (15.1, 15.1, -4.6875)
D2module_coords[9] = (-15.1, 15.1, -4.6875)
D2module_coords[10] = (-45.3, 15.1, -4.6875)
D2module_coords[11] = (30.2, 41.254, -4.6875)
D2module_coords[12] = (0, 41.254, -4.6875)
D2module_coords[13] = (-30.2, 41.254, -4.6875)


def absolute_position(daughter_position, mother_position):
    new_position = np.add(mother_position, daughter_position)
    return new_position


def identify_detector(position):
    if detector_id == 4:
        V1
        V2
        V3
        V4
    if detector_id == 7:
        if 85<z<115:
        if z:
            D2


def identify_module():
    for module in D1 if D1:
        if check_module():
            return module



def check_module(x, y, module_x, module_y, radius):
    """
    Returns true if point is in the correct module.
    """
    if abs(x - module_x) > radius:
        return False
    if abs(y - module_y) > radius:
        return False
    if (x - module_x)**2 + (y - module_y)**2 < radius**2:
        return True
    else:
        return False