------------------------------------------------------------------------------

         =========================================================
           the MEGAlib Extension for Neutron Interaction Analysis
         =========================================================
                  Morgan A. Daly (mad2001@wildcats.unh.edu)
                                 Summer 2016

    -------
    Summary
    -------
The process_sims module is where MEGAlib's functionality is extended to
the handling of neutrons.

Particle interaction data in the form of the Cosima *.sim file is provided as
input. Based on the COMPTEL geometry outline (found in the geometry module), the
energy deposited from each particle interaction is converted to its electron
equivalence. The position, energy, and time of flight (ToF) are then broadened
based on the detector's resolution. Finally, events that would successfully
trigger COMPTEL are selected based on criteria defined in the geometry module.

A *.sim file or a directory of *.sim files is taken as input. The program
currently reads the entire input file at once, so the size that can
be handled is limited by this (though text files of upwards of 1GB are handled
without issue on most computers). However, several smaller files can be
processed and combined, allowing for larger amounts of data to be produced. This
can be done easily using the run_sims module.


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

Events that triggered the detector are identified based on COMPTEL's
anticoincidence filtering. A triggered event consists of:
    - one hit in D1 that deposits energy greater than the threshold
    - one hit in D2 that deposits energy greater than the threshold
    - a time of flight less than the maximum
    - energy less than the threshold deposited in the veto domes
The data from a simulation is stored in an object that contains the triggered
events, the total number of particles started, and the incident energy. This
object is saved in a new directory as a binary file. This makes the processed
data easily accessible for analysis at a later point in time.


The output of the program is an object containing:
    - the DataFrame with the interaction data from triggered events
    - the incident energy
    - the number of triggered events
    - the total number of particles started
The object is saved as a pickle so that the processed data is accessible without
having to run the process_sims module more than once.


    ----------
    How to Run
    ----------
This module can be run "as is" for COMPTEL neutron simulations. Other types of
simulations could require significant revision*.

Use the command "python process_sims.py </full/path/to/simfiles>" to run.


* note that the program will likely run without issue and process the Cosima
    output files from any simulation; the output, however, will be physically
    nonsensical
