# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 15:59:34 2015

@author: morgan

I. parse text file input
    A. turn into list of event strings
        1. pull out relevant event data
        2. split into interactions
            i. pull out relevant interaction data







@todo check variable names
@todo document
@todo maybe comment?
@todo save new version without old functions

"""

import re

import numpy as np
import time


start = time.clock()

filename = "TAKE3o18_1MeV.inc2.id1.sim"


def compile_regex():

    global event_re
    global event_values_re
    global interactions_re

    event_re = re.compile(r"""
        (?<=^SE$)                # +lookbehind "SE" on its own line
        (?P<event>.+?)           # any amount of text
        (?=^[SE]{2}|[EN]{2}$)    # +lookahead "SE" or "EN" on its own line
        """, re.X | re.MULTILINE | re.DOTALL)
    event_values_re = re.compile(r"""
        (?<=^ID\s)                    # +lookbehind "ID\s" starts line
        (?P<event_id>\d+?)\s          # a number, then space
        (?P<out_of>\d+?$)             # a number at end of line
        \nTI\s                        # "TI" on its own line, then space
        (?P<start_time>\d+?.\d+?$)    # a number at end of line
        """, re.X | re.MULTILINE)
    interactions_re = re.compile(r"""
        (?<=^IA\s\b\w{4}\s\s)     # +lookbehind "IA [INIT]  " starts line
        (?P<ia>[-+\de\s;\.]+)     # the formatting of values in interaction
        (?:\n)                    # noncapturing "\n"
        """, re.X | re.MULTILINE)

    return None


# XXX this one is done!
#       wall time: 674 ms
def parse_simfile(filename):
    """
    Parse the text file output by MEGAlib's Cosima simulation program.

    Paramerters
    ------------
    filename -- the complete path to the *.sim file to be parsed

    Returns
    --------
    a list of events from the simulation as seperate strings

    """

    with open(filename) as fh:
        simfile = fh.read()
    return event_re.findall(simfile)


## XXX this one is done!
##       wall time: 73.9 ms
#def make_eventarray(event_list):
#    """
#    Identify the important values (not interactions) from each event
#    in a *.sim file.
#
#    Paramerters
#    ------------
#    event_list -- a list of the events as strings
#
#    Returns
#    --------
#    event_data -- an ndarray containing the event ID number, the number
#        of events total, and the start time of the event for each event
#
#    """
#
#    event_data = np.empty([len(event_list), 3])
#
#    for i, one_event in enumerate(event_list):
#        event_data[i, :] = event_values_re.search(one_event).group(
#                'event_id', 'out_of', 'start_time')
#    # XXX this returns numbers as strings not floats!!
#
#    return event_data


def pull_eventvalues(one_event):

    event_regexobject = event_values_re.search(one_event)

    event_id = float(event_regexobject.group('event_id'))
    out_of = float(event_regexobject.group('out_of'))
    start_time = float(event_regexobject.group('start_time'))

    # creates tuple of event values
    eventvalues = event_id, out_of, start_time

    return eventvalues


# XXX this one is done!
def pull_interactiondata(one_event):
    """
    Identify the important values in each interaction

    Paramerters
    ------------
    one_event -- an individual event string

    Returns
    --------
    interaction_data -- an ndarray of the relevent interaction data for
        interactions from a single event

    """

    interaction_data = np.empty([len(interactions_re.findall(one_event)), 10])

    for i, interaction in enumerate(interactions_re.finditer(one_event)):
        all_data = np.fromstring(interaction.group('ia'), count=23, sep=';')
        interaction_data[i, :] = (np.array(
                    all_data[[0, 1, 2, 3, 4, 5, 6, 7, 15, 22]]))

    # returns a (numberofinteractions, 10) ndarray
    return interaction_data


def make_eventarray(one_event):
    event_values = pull_eventvalues(one_event)

    ia_array = pull_interactiondata(one_event)
    eventvalues_array = np.tile(event_values, (ia_array.shape[0], 1))
    event_array = np.concatenate((eventvalues_array, ia_array), axis=1)

    return event_array

#
## XXX this one is done!
##       wall time: 1.04 s stored as list
##       wall time: 3.42 s stored as dictionary
#def make_interactionarray(all_events):
#    """
#    Compiles interaction arrays of each event into a list.
#
#    Paramerters
#    ------------
#    all_events -- a list of event strings
#
#    Returns
#    --------
#    all_interactions -- a list of event arrays the same size
#        as the input list
#
#    """
#
#    all_interactions = {}
#    for i, event in enumerate(all_events):
#        ia_event = pull_interactiondata(all_events[i])
#        all_interactions[i] = ia_event
#
#    return all_interactions


def build_array(all_events):

    output_array = make_eventarray(all_events[0])
    for i, single_event in enumerate(all_events, 1):
        output_array = np.concatenate(
                (output_array, make_eventarray(single_event)))

    return output_array


def main():

    compile_regex()
    all_events = parse_simfile(filename)
    output_array = build_array(all_events)

    return output_array


#def main():
#
#    compile_regex()
#    # create list of event strings "all_events" from *.sim file
#    all_events = parse_simfile(filename)
#    # construct ndarray of important data (sans interactions)
#    event_data = make_eventarray(all_events)
#    # construct list of ndarrays of interaction data
#    interaction_data = make_interactionarray(all_events)
#
#    return all_events

main()

end = time.clock()

time = end - start
print(time)


""" NOTES:

Tuesday run: ~86s
Thursday run: ~7.4s   (:

    An interaction from the sim file yields:
    1: interaction type
    2: ID of this interaction
    3: ID of interaction this particle originated from
    4: Detector ID
        4: scintillator (here, anticoincidence domes)
        7: anger camera (here, D1/D2 scintillators)
    5: Time since start of event in seconds
    6: x position of interaction in cm
    7: y position of interaction in cm
    8: z position of interaction in cm
    9: ID of original particle
        1: gamma
        2: positron
        3: electron
        4: proton
        6: neutron
        18: deuteron
        20: He-3
        21: alpha
    -10: new x direction of original particle
    -11: new y direction of original particle
    -12: new z direction of original particle
    -13: new x polarization of original particle
    -14: new y polarization of original particle
    -15: new z polartization of original particle
    -16: new kinetic energy of original particle in keV
    17: ID of new particle
    -18: x direction of new particle
    -19: y direction of new particle
    -20: z direction of new particle
    -21: x polarization of new particle
    -22: y polarization of new particle
    -23: z polarization of new particle
    24: kinetic energy of new particle in keV

    ** What pieces do we actually need?? **
    2, 3, 4, 5, 6, 7, 8, 9, 17, 24
"""
