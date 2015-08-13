# -*- coding: utf-8 -*-

"""
Created: Tue Jul  7 13:08:07 2015

Author: Morgan A. Daly


This module contains functions to parse the text file output from Cosima,
a Geant4 interface in the MEGAlib package.
Important data is organized into a ndarray to allow for further analysis.

Wall time: 3.29 s

"""

import re

import numpy as np
import pandas as pd


def pull_simdata(filename):


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

    # create list of all events as strings
    with open(filename) as fh:
        simfile = fh.read()
    all_events = event_re.findall(simfile)

    # store the total number of particles started
    particle_count = particle_count_re.search(simfile).group(0)


    def make_eventarray(one_event):
        """
        Creates a single array containing both the event and interaction data.

        Effectively, it adds the corresponding event data to the beginning of
        each row of the interaction array in order to combine the information.


        Paramerters
        ------------
            one_event -- an individual event string

        Returns
        --------
            a (# interactions, 9) ndarray of all data for a single event

        """

        # convert the values in the strings to numbers
        event_id = float(event_values_re.search(one_event).group('event_id'))

        # create empty ndarray to store data
        interaction_data = np.empty([len(interactions_re.findall(one_event)), 8])
        # store values
        interaction_data[:, 0] = event_id
        for i, interaction in enumerate(interactions_re.finditer(one_event)):
            # turn string of data values into ndarray
            all_data = np.fromstring(interaction.group('ia'), count=23, sep=';')
            # store the relevant values
            #   (interaction ID, detector ID, elapsed time, position, particle
            #    ID, kinetic energy)
            interaction_data[i, 1:] = (np.array(
                        all_data[[2, 3, 4, 5, 6, 15, 22]]))

        return interaction_data


    # build ndarray of data for all events
    sim_data = make_eventarray(all_events[0])
    for i, single_event in enumerate(all_events, 1):
        sim_data = np.concatenate(
                (sim_data, make_eventarray(single_event)))
    # convert to data frame
    sim_data = pd.DataFrame(sim_data,
                        columns=['EventID', 'DetectorID', 'ElapsedTime', 'x',
                                 'y', 'z', 'NewParticleID', 'Energy'])

    return {'data': sim_data, 'particle count': float(particle_count),
            'incident energy': sim_data.Energy[0]}



if __name__ == '__main__':
    filename = "COMPTELeffA_22MeV.inc1.id1.sim"
    data = pull_simdata(filename)

