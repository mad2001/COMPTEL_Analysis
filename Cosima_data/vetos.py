# -*- coding: utf-8 -*-
"""
Created: Wed Jul 22 13:39:34 2015

Author: Morgan A. Daly
"""
from defining_volumes import *


def construct_triggers(hits):

    """
    if triggers is true and vetos is false
        save

    if there is not one D1 hit and 1 D2 hit:
        delete
    if D1 < 50
    """

    # lists containing all modules in each detector layer
    d1 = [1.01, 1.02, 1.03, 1.04, 1.05, 1.06, 1.07]
    d2 = [2.01, 2.02, 2.03, 2.04, 2.05, 2.06, 2.07, 2.08, 2.09, 2.10, 2.11,
          2.12, 2.13, 2.14]

    for EventID, group in hits.groupby(level='EventID'):

        # to sort data
        grp_idx = group.index.get_level_values('DetectorID')
        d1_idx = grp_idx.isin(d1)
        d2_idx = grp_idx.isin(d2)
        try:
            time_of_flight = group.ElapsedTime[d2_idx].sub(
                group.ElapsedTime[d1_idx].values)
        except ValueError:

        d1_d2_hits = d1_idx.sum() == 1 and d2_idx.sum() == 1
        threshold_energy = all(group.Energy[d1_idx] > 50) and \
            all(group.Energy[d2_idx] > 100)
        tof_requirement = all(time_of_flight > 0)

        # check for any vetos
        if any(grp_idx.isin([3.01])) and VD1.check_veto(group.Energy[3.01]):
            hits.drop(EventID, level='EventID', inplace=True)
        elif any(grp_idx.isin([3.02])) and VD2.check_veto(group.Energy[3.02]):
            hits.drop(EventID, level='EventID', inplace=True)
        elif any(grp_idx.isin([3.03])) and VD3.check_veto(group.Energy[3.03]):
            hits.drop(EventID, level='EventID', inplace=True)
        elif any(grp_idx.isin([3.04])) and VD4.check_veto(group.Energy[3.04]):
            hits.drop(EventID, level='EventID', inplace=True)

        # check all trigger requirements
        elif d1_d2_hits and threshold_energy:
            if tof_requirement:
                continue
            else:
                hits.drop(EventID, level='EventID', inplace=True)
        else:
            hits.drop(EventID, level='EventID', inplace=True)

    def reformat_dataframe(data):
        d1_data = data.select(lambda x: x[1] in d1)
        d2_data = data.select(lambda x: x[1] in d2)

        tof = d2_data['ElapsedTime'].sub(d1_data['ElapsedTime'].values)
        print(tof)

        final = pd.DataFrame(
            {'D1Energy': d1_data.Energy.values,
             'D1Position': list(zip(d1_data.x.values, d1_data.y.values, d1_data.z.values)),
             'D2Energy': d2_data.Energy.values,
             'D2Position': list(zip(d2_data.x.values, d2_data.y.values, d2_data.z.values)),
             #'TimeOfFlight': tof
             })
        print(final)

    return hits
