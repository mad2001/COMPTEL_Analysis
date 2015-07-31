# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 16:06:03 2015

@author: Morgan
"""

import matplotlib.pyplot as plt


def plot_efficiency(energy, efficiency):
    plt.plot(energy, efficiency)
    plt.ylabel('Electron Equivalent Energy (MeV)')
    plt.xlabel('Energy (MeV)')
    plt.title('Detector Efficiency')
    plt.grid(True)
    plt.show()


