------------------------------------------------------------------------------

         =========================================================
           the MEGAlib Extension for Neutron Interaction Analysis
         =========================================================
                  Morgan A. Daly (mad2001@wildcats.unh.edu)
                                 Summer 2016

    -------
    Summary
    -------
The run_sims module allows for the automation of detector simulations using
MEGAlib's Cosima package.

This is especially useful for low efficiency detectors where the processing
module will be used, as several smaller *.sim files created by the same *.source
file are handled better than a single very large one.

The *.source file specifies the particle's incident energy, so it must be edited
for each energy level simulated. This is done explicitly in the run_sims module
as a "find-and-replace" using the regex function sub(pattern, replace, string),
and must be edited in order to match the *.source file being used. Generally,
the only lines that will be changed are the lines describing the source, and
the line specifying the filename. These are shown as examples in the module.

The *.sim files that are output by Cosima will be saved in the directory
specified, where a subdirectory will be created for each energy level. This
organization allows the processing portion of the program run through all of the
sim files generated automatically.

    ----------
    How to Run
    ----------
The file run_sims.py must be edited before running. Parameters include:
    - full path to the Cosima *.source file being run
    - the full path of the directory where the output *.sim files will be saved
    - the incident energy levels to simulate
    - the number of simulations to run at each energy level
Additionally, the find-and-replace lines for the *.source file must be specified
within the run_sims module.

Use the command "python run_sims.py" to run.
