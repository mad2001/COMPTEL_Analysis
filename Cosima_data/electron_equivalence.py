# -*- coding: utf-8 -*-



"""
    if (particle ID == #):
        energy = E_eee


"""


def electron_equivalent(energy, detector, particle):
    if D1(p, d, t):
        a_1 = 0.83
        a_2 = 2.82
        a_3 = 0.25
        a_4 = 0.93
    if D1(alpha, He3):
        a_1 = 0.42
        a_2 = 5.9
        a_3 = 0.065
        a_4 = 1.01
    if D2:
        return energy
    return a_1 * energy - a_2 * ( 1.0 - exp( -a_3 * energy**a_4 ) )
