#!/usr/bin/env python3.5
"""Parse a *.sim file and store useful data in a ndarray.

This module contains functions to parse the text file output from Cosima,
a Geant4 interface in the MEGAlib package.
Important data is organized into a ndarray to allow for further analysis.

Created: Tue Jul  7 13:08:07 2015
Author: Morgan A. Daly (mad2001@wildcats.unh.edu)
"""
import re

import numpy as np
import pandas as pd


def pull_simdata(filename):
    """Store data from a *.sim file as a pandas dataframe.

    Parameters
    ----------
        filename -- the path to the *.sim file being parsed

    Returns
    -------
        a dictionary containing three elements:
            data -- a pandas dataframe containing 'EventID', 'DetectorID',
                    'ElapsedTime', 'x', 'y', 'z', 'NewParticleID', 'Energy' for
                    each interaction in the event
            particle count -- total number of incident particles simulated
            incident energy -- incident particle energy being simulated
    """
    # compile regex needed to parse *.sim file
    event_re = re.compile(r"""
        (?<=^SE$)                 # +lookbehind "SE" on its own line
        (?P<event>.+?)            # any amount of text
        (?=^[SE]{2}|[EN]{2}$)     # +lookahead "SE" or "EN" on its own line
        """, re.X | re.MULTILINE | re.DOTALL)
    event_values_re = re.compile(r"""
        (?<=^ID\s)                    # +lookbehind "ID\s" starts line
        (?P<event_id>\d+?)\s          # a number, then space
        (?P<out_of>\d+?$)             # a number at end of line
        \nTI\s                        # "TI" on its own line, then space
        (?P<start_time>\d+?.\d+?$)    # a number at end of line
        """, re.X | re.MULTILINE)
    interactions_re = re.compile(r"""
        (?<=^IA\s\b\w{4}\s\s)       # +lookbehind "IA [INIT]  " starts line
        (?P<ia>[-+\de\s;\.]+)       # the formatting of values in interaction
        (?:\n)                      # noncapturing "\n"
        """, re.X | re.MULTILINE)
    particle_count_re = re.compile(r"""
        (?<=^TS\s)                  # +lookbehind "TS" starts line
        (\d+?$)                     # capture number
        """, re.X | re.MULTILINE)

    with open(filename, 'r') as fh:
        simfile = fh.read()

    # create list of all events as strings
    all_events = event_re.findall(simfile)

    # store the total number of incident particles
    particle_count = particle_count_re.search(simfile).group(0)

    def make_eventarray(one_event):
        """Create a single array containing the event and interaction data.

        Converts the string containing event data into an ndarray. The array is
        formatted as shown below:
        ---------------------------------------------------------------------------------------------
        |EventID||InteractionID||DetectorID||Elapsed Time|| x || y ||  z ||ParticleID||KineticEnergy|
        ---------------------------------------------------------------------------------------------


        Parameters
        ----------
            one_event -- an individual event string

        Returns
        -------
            a (# interactions, 9) ndarray of all data for a single event
        """
        # pull event id number from string and convert it to a float
        event_id = float(event_values_re.search(one_event).group('event_id'))

        # create empty ndarray (one row per interaction, 8 columns)
        interaction_data = np.empty([len(interactions_re.findall(one_event)), 8])

        # assign event_id to interactions in event
        interaction_data[:, 0] = event_id

        # fill in the rest of the interaction data
        for i, interaction in enumerate(interactions_re.finditer(one_event)):
            # turn string of interaction data into ndarray
            all_data = np.fromstring(interaction.group('ia'), count=23, sep=';')
            # store interaction ID, detector ID, elapsed time, x, y, z,
            #    particle ID, and kinetic energy)
            # @NOTE changed particle ID from element 15 to element 7 (from "new particle" to "incident particle")
            interaction_data[i, 1:] = (np.array(
                                       all_data[[2, 3, 4, 5, 6, 7, 22]]))
        return interaction_data

    # @NOTE this bit seems silly... make a list of ndarrays, concat to one
    #       ndarray, then convert to datafram??
    sim_data = np.concatenate([make_eventarray(event) for event in all_events])
    sim_data = pd.DataFrame(sim_data,
                            columns=['EventID', 'DetectorID', 'ElapsedTime',
                                     'x', 'y', 'z', 'ParticleID', 'Energy'])

    return {'data': sim_data, 'particle count': float(particle_count),
            'incident energy': sim_data.Energy[0]}


# current wall time of ~4s processing of 30MB *.sim file
if __name__ == '__main__':
    import sys

    data = pull_simdata(sys.argv[1])

    print("\n\nSimulated {} particles at {} keV.\n".format(
          data['particle count'], data['incident energy']))
    print("Would you like to see all recorded data? (y/n)")
    ans = input()
    if ans == 'y':
        print(data['data'])
    elif ans == 'n':
        print('\nExiting now.\n')
    else:
        print("\nYour input was something other than y or n... \nExiting now.")
