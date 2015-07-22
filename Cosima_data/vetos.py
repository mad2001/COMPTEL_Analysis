# -*- coding: utf-8 -*-
"""
Created: Wed Jul 22 13:39:34 2015

Author: Morgan A. Daly
"""
from defining_volumes import *

def check_vetos(hits):
    for EventID, group in hits.groupby(level='EventID'):
        if any(group.index.get_level_values('DetectorID').isin([3.01])) and \
                VD1.check_veto(group.Energy[3.01]):
            hits.drop(EventID, level='EventID', inplace=True)
            print('v1')
        elif any(group.index.get_level_values('DetectorID').isin([3.02])) and \
                VD1.check_veto(group.Energy[3.02]):
            hits.drop(EventID, level='EventID', inplace=True)
            print('v2')
        elif any(group.index.get_level_values('DetectorID').isin([3.03])) and \
                VD1.check_veto(group.Energy[3.03]):
            hits.drop(EventID, level='EventID', inplace=True)
            print('v3')
        elif any(group.index.get_level_values('DetectorID').isin([3.04])) and \
                VD1.check_veto(group.Energy[3.04]):
            hits.drop(EventID, level='EventID', inplace=True)
            print('v4')
    return hits


def construct_triggers(hits):

        """
        if triggers is true and vetos is false
            save

        if there is not one D1 hit and 1 D2 hit:
            delete
        if D1 < 50
        """

        d1 = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
        d2 = [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11,
              2.12, 2.13, 2.14]

        for EventID, group in hits.groupby(level='EventID'):
            if group.index.get_level_values('DetectorID').isin(d1).sum() == 1\
                    and group.index.get_level_values(
                    'DetectorID').isin(d2).sum() == 1:
                continue
            else:
                hits.drop(group.index)