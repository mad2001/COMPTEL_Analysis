# -*- coding: utf-8 -*-



"""
    if (particle ID == #):
        energy = E_eee


"""
import math

def electron_equivalent(sim_data):
    """
    input is one row of data frame

    data from paper
    """
    energy = sim_data['Energy']
    particle = sim_data['NewParticleID']

    # if interaction is in D1 layer
    if 1 <= sim_data['DetectorID'] < 2:
        d1_particles = [4, 18, 19, 13027, 6012, 53125, 53126]
        # if particle is proton, deuteron, or triton
        if particle in d1_particles:
            a_1 = 0.83
            a_2 = 2.82
            a_3 = 0.25
            a_4 = 0.93
        # if particle is alpha or He-3
        # elif particle == 21 or particle == 20:
        else:
            a_1 = 0.42
            a_2 = 5.9
            a_3 = 0.065
            a_4 = 1.01
        return a_1 * energy - a_2 * (1.0 - math.exp( -a_3 * energy**a_4 ))
    # if interaction is in D2 layer
    elif 2 <= sim_data['DetectorID'] < 3:
        return energy
    # if interaction is in veto dome
    elif 3 <= sim_data['DetectorID'] < 4:
        return energy
    else:
        return energy

