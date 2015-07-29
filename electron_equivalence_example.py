# -*- coding: utf-8 -*-
"""
Created: Mon Jul 27 12:17:44 2015

Author: Morgan A. Daly
"""

import math

import numpy as np
import matplotlib.pyplot as plt

T_e = lambda x: a_1 * x - a_2 * (1.0 - math.exp( -a_3 * x**a_4 ))

energy = np.arange(0.25, 10, .1)

# for protons in NE-213
a_1 = 0.83
a_2 = 2.82
a_3 = 0.25
a_4 = 0.93

E_1 = np.array([T_e(x) for x in energy])

# for protons in NE-102
a_1 = 0.95
a_2 = 8.0
a_3 = 0.1
a_4 = 0.9

E_2 = np.array([T_e(x) for x in energy])

# for alpha particles
a_1 = 0.41
a_2 = 5.9
a_3 = 0.056
a_4 = 1.01

E_3 = np.array([T_e(x) for x in energy])

plt.loglog(energy, E_1, 'g',  energy, E_2, 'b', energy, E_3, 'r')
plt.xlim(0.25, 10)
plt.ylabel('Electron Equivalent Energy (MeV)')
plt.xlabel('Particle Kinetic Energy (MeV)')
plt.title('Electron Equivalent Energy')
plt.legend(['Protons in NE-213', 'Protons in NE-102', 'Alpha Particles'])
plt.grid(True)
plt.show()

