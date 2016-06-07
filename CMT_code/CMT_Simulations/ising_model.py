# -*- coding: utf-8 -*-
"""
Created on Sat Apr 30 20:12:01 2016

@author: Morgan


Implementation of Metropolis algorithm to simulate Ising model.
"""

import numpy as np
from scipy.constants import k



J = 1              # coupling constant
n = 10             # size of lattice
L = np.ones(n)     # lattice

def print_lattice(array):
    for i in array:
        if i > 0: print('+', end=' ')
        else: print('-', end=' ')

print_lattice(L)

# choose random spot on lattice
    # if dE<=0
        # flip spin
    # if RandomNumber <= exp(-dE/kT)
        # flip spin





