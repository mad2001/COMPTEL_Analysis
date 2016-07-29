------------------------------------------------------------------------------

         =========================================================
           the MEGAlib Extension for Neutron Interaction Analysis
         =========================================================
                  Morgan A. Daly (mad2001@wildcats.unh.edu)
                                 Summer 2016


    ----------
    Motivation
    ----------
The program was designed in order to expand the functionality of the Medium
Energy Gamma Ray Astronomy Library (MEGAlib) for use in analyzing the neutron
response of COMPTEL. While the MEGAlib packages Geomega (used for modeling
detectors) and Cosima (a Geant4 based simulator) together handle neutron
simulations well, the analysis packages included in MEGAlib do not. MEGAlib
fails to convert energy deposited in scintillators to its electron equivalent,
making it impossible to determine whether or not an event’s light output would
trigger the detector. To resolve this, the simulated data from Cosima was used,
but all post-processing was done externally.


    -------------
    Functionality
    -------------
Three main modules are included:
    (1) run_sims.py -- automates the running of Cosima simulations
    (2) process_sims.py -- simulates the COMPTEL neutron response
    (3) analyze_sims.py -- analyzes the simulated data

This project is still under development. Please contact Morgan with any problems
or suggestions.


    ---------------------
    Software Requirements
    ---------------------
The following software is required for full functionality:
  - MEGAlib version 2.3
  - Python version 3.5 (or greater)
  - numpy
  - pandas
  - matplotlib

It is recommended to install the required python libraries with the package
manager Anaconda (which includes all of the required libraries) or the lighter
weight version miniconda (which will then require installation of the necessary
libraries). Conda is available for download at conda.pydata.org. Be sure to
select the Python 3.5 version.
