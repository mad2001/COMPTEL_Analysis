# -*- coding: utf-8 -*-


"""
Created on Fri Jun 26 11:31:42 2015

@author: morgan
"""

"""
STEP ONE
    change to electron equivalent energy


Position
    D1xy
        position is the weighted overage of the x/y locations by energy loss
        broaden these positions by the spatial resolation (1 sig is 1.6cm)
    D1z
        equal to middle of z

    D2xy
        position is the weighted overage of the x/y locations by energy loss
        broaden these positions by the spatial resolation (1 sig is 1.4cm)
    D2z
        equal to middle of z

Time of Flight

Energy Loss
    D1
    D2
    V1
    V2
    V3
    V4

"""
import math

def broaden_d1energy(interaction):
    if module == 1:
        A = -1.022
        B = 1.749
    if module == 2:
        A = -7.481
        B = 2.157
    if module == 3:
        A = 2.944
        B = 1.723
    if module == 4:
        A = -5.822
        B = 1.935
    if module == 5:
        A = -3.073
        B = 1.892
    if module == 6:
        A = -8.662
        B = 2.069
    if module == 7:
        A = 0.020
        B = 1.890
    sigma = A + B * math.sqrt(energy)
    return np.random.normal(energy, sigma)


def broaden_d2energy(interaction):
    sigma = math.sqrt(1.28*energy + 3.6*energy**2)
    return np.random.normal(energy, sigma)


