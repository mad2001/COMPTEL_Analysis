# -*- coding: utf-8 -*-

"""
Created: Tue Jul  7 13:08:07 2015

Author: Morgan A. Daly


This module contains functions to parse the text file output from Cosima,
a Geant4 interface in the MEGAlib package.
Important data is organized into a ndarray to allow for further analysis.

Current wall time: 7.4 s

"""


import re

import numpy as np
import pandas as pd


def compile_regex():
    """
    Compiles regular expressions that will be used to parse text file.

    The three expressions are declared global variables to allow for
    use outside the function.

    """

    # compiled regex are global so that they can be used by other functions
    global event_re
    global event_values_re
    global interactions_re

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

    return


def parse_simfile(filename):
    """
    Parse the text file output from MEGAlib's Cosima simulation program.

    Opens file by filename, read it, seperate into events, return a list of
    events from the simulation as seperate strings.

    """

    with open(filename) as fh:
        simfile = fh.read()

    return event_re.findall(simfile)


def pull_eventvalues(one_event):
    """
    Find and store relevant data about an event.

    Takes an event string and returns a tuple containing the event ID, the
    total number of incident particles, and the event's start time.

    """
    event_regexobject = event_values_re.search(one_event)

    # convert the values in the strings to numbers
    event_id = float(event_regexobject.group('event_id'))
    out_of = float(event_regexobject.group('out_of'))
    start_time = float(event_regexobject.group('start_time'))

    return tuple((event_id, out_of, start_time))


def pull_interactionvalues(one_event):
    """
    Find and store relevant data about the interactions in an event.

    Takes an event string and returns a (# interactions, 10) ndarray of the
    interaction data for interactions from a single event.

    """

    # create empty ndarray to store data
    interaction_data = np.empty([len(interactions_re.findall(one_event)), 10])

    for i, interaction in enumerate(interactions_re.finditer(one_event)):
        # turn string of data values into ndarray
        all_data = np.fromstring(interaction.group('ia'), count=23, sep=';')
        # store the relevant values
        interaction_data[i, :] = (np.array(
                    all_data[[0, 1, 2, 3, 4, 5, 6, 7, 15, 22]]))

    return interaction_data


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
        a (# interactions, 13) ndarray of all data for a single event

    """

    event_values = pull_eventvalues(one_event)
    ia_array = pull_interactionvalues(one_event)

    eventvalues_tiled = np.tile(event_values, (ia_array.shape[0], 1))

    return np.concatenate((eventvalues_tiled, ia_array), axis=1)


def make_outputarray(all_events):
    """
    Creates a single Pandas data frame containing pertinent data from all
    events. Columns are labels, each row represents an interaction.

    """

    sim_data = make_eventarray(all_events[0])

    for i, single_event in enumerate(all_events, 1):
        sim_data = np.concatenate(
                (sim_data, make_eventarray(single_event)))

    return pd.DataFrame(sim_data,
                        columns=['EventID', 'Incidents', 'StartTime',
                                 'InteractionID', 'OriginInteractionID',
                                 'DetectorID', 'ElapsedTime', 'x', 'y', 'z',
                                 'OriginalParticleID', 'NewParticleID',
                                 'Energy'])


"""  #######     Actual Function to Use     ######  """


def return_simdata(filename):

    # compiles regex used to parse *.sim file
    compile_regex()

    # create list of all events as strings
    all_events = parse_simfile(filename)

    # put events into labeled pandas data frame
    return make_outputarray(all_events)
