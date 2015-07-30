# -*- coding: utf-8 -*-
"""
Created: Thu Jul 30 11:25:55 2015

Author: Morgan A. Daly



function [] = efficiency( N_triggers, N_simulated )
%Calculates efficiency values for COMPTEL's neutron response
%   For MEGAlib simulation of COMPTEL
%
%   Input: number of triggered events, number of neutrons started
%   Output: effective area and detector efficiency

%Measurements from simulation geometry files
s = 16;         %number of sides of scintillator's polygon volume
R = 13.47;      %radius of scintillator's polygon volume
r = 250;        %radius of "surrounding sphere"



%calculate geometric area of detector (here, area of D1 scintillators)
    % sind is a function that calculates sin(x) with input in degrees
A_det = R^2 * s * sind(360/s) / 2;

%calculate area from which neutrons are being started
A_start = pi * r^2;

%calculate effective area of COMPTEL for neutrons
A_eff = A_start * (N_triggers / N_simulated)

%calculate detector efficiency
efficiency  = A_eff / A_det


"""
import numpy as np


def calc_effective_area(simulated_particles, triggered):

    # Measurements from simulation geometry files
    s = 16         # number of sides of scintillator's polygon volume
    R = 13.47      # radius of scintillator's polygon volume
    r = 250        # radius of "surrounding sphere"

    # calculate geometric area of detector (here, area of D1 scintillators)
    A_det = R**2 * s * np.tan(np.pi / s) * 7
    print(A_det)

    # calculate area from which neutrons are being started
    A_start = np.pi * r**2

    # calculate effective area of COMPTEL for neutrons
    A_eff = A_start * (triggered / simulated_particles)
    print(A_eff)

    # calculate detector efficiency
    efficiency = A_eff / A_det

    return efficiency*100
