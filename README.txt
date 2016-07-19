------------------------------------------------------------------------------

         =========================================================
           the MEGAlib Extension for Neutron Interaction Analysis
         =========================================================
                  Morgan A. Daly (mad2001@wildcats.unh.edu)
                                 Summer 2016


The program was designed in order to expand the functionality of the Medium
Energy Gamma Ray Astronomy Library (MEGAlib) for use in analyzing the neutron
response of COMPTEL. While the MEGAlib packages Geomega (used for modeling
detectors) and Cosima (a Geant4 based simulator) together handle neutron
simulations well, the included analysis packages do not. MEGAlib fails to
convert energy deposited in scintillators to its electron equivalent, making it
impossible to determine whether or not an event’s light output would trigger the
detector. To resolve this, the simulated data from Cosima was used, but all
post-processing was done externally.

The program takes the sim file created by Cosima as its input.
This can be either a single file, or a directory of sim files originating from
identical source files. The program is currently unable to read very large
files, but providing several smaller sim files allows larger amounts of data
to be produced.
First, the list of interactions provided in the sim file are converted into
“hits” that would be detected by COMPTEL.

This is done with the following process:
    1. scrape data from sim file
    2. convert energy deposited by each particle to electron equivalent
    3. identify the interaction’s detector module using the position
    4. group interactions by event and module to construct hits
    5. take energy weighted average position, average time, and summed energy
    for each hit
    6. broaden energy, position, and time of flight based on detector resolution

Events that triggered the detector are then identified based on the vetoing and
anticoincidence filtering used by COMPTEL.
A triggered event consists of one hit in D1 that deposits energy greater than
the threshold, one hit in D2 that deposits energy greater than the threshold, a
time of flight less than the maximum, and energy less than the threshold
deposited in the veto domes.
The data from a simulation is stored in an object that contains the triggered
events, the total number of particles started, and the incident energy. This
object is saved in a new directory as a binary file. This makes the processed
data easily accessible for analysis at a later point in time.

The following software is required for full functionality:
  - MEGAlib version 2.3
  - Python version 3.5 (or greater)
  - MEGAlib
  - numpy
  - pandas
  - matplotlib

It is recommended to install the required python libraries with the package
manager Anaconda (which includes all of the required libraries) or the lighter
weight version miniconda (which will then require installation of the required
libraries.)
