# -*- coding: utf-8 -*-

"""
Created: Mon Jul  6 14:52:13 2015
Author: Morgan A. Daly

This is painfully brute forced I'm sorry @everyone
"""
import numpy as np

from defining_volumes import *




def identify_detector(position):
    module = 0

    # if it is a veto dome
    if detector_id == 4:
        if z > 50:
            module += 1
        elif z < 50:
            module += 2
    # if it is a scintillator
    if detector_id == 7:
        module += 3
        if z > 50:
            module += .1
        elif z < 50:
            module += .2
    else:
        print('ERROR: weird detector stuff?')


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