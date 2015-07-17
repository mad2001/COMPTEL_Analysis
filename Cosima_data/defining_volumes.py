# -*- coding: utf-8 -*-

"""
Created: Summer 2015
Author: Morgan A. Daly


This module defines all necessary volumes for COMPTEL simulation data
analysis. The positions and measurements used are those in the input file
for Geomega's geometry analysis, ensuring consistency throughout the program.

It is important to note that the objects as defined in this module are not
volumes in the way that a ROOT/Geant4/ Geomega volume is. The classes and
objects were created in order to encapsulate the information necessary to
derive the desired output. As such, care should be used if attempting to
extend a defined class or object beyond its implementation in this program.
(if it sounds like this is super brute forced that's because it is)


Classses:
    Volume
    Virtural
    D1
    D2
    VetoDome1
    VetoDome2
    VetoDome3
    VetoDome4

@todo tbh this module is barely readable plz help
"""

import numpy as np


class Volume(object):
    """
    A volume; written for expressing volumes defined in MEGAlib's Geomega.

    Useful as it makes the relationship between numerous objects in various
    layers of Geomega inheritance simplified and calculates the position of
    the volumes absolutely, assuming the mother volumes are also defined.

    Attributes
    -----------
        position-- the Cartesian coordinates of the volume's center
        x-- the position's x coordinate
        y-- the position's y coordinate
        z-- the position's z coordinate
        mother-- the mother volume of the virtual volume (default argument
            is None)
        module_id-- an id to label a specific module (default argument is 0)
        id-- an id X.Y where X is a label for the volume type and Y is
            the module id

    """

    id = 1

    def __init__(self, position, mother=None):
        self.mother = mother
        if mother is not None:
            self.position = np.add(position, mother.position)
        else:
            self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]



class Virtual(Volume):
    """
    Non-detector volumes.

    These objects are passive but necessary in order to accurately
    track the chain of mother/daughter volumes.

    Attributes
    -----------
        id-- number to track all virtual volumes
        position-- the Cartesian coordinates of the volume's center
        x-- the position's x coordinate
        y-- the position's y coordinate
        z-- the position's z coordinate
        mother-- the mother volume of the virtual volume (default argument
            is None)
        module_id-- not necessary to access specific virtual volumes
        id-- ID is 0.0 for Virtual objects

    Notes
    ------
        ** the volume's position attributes are its absolute Cartesian
            coordinates, not relative to any mother volume
        ** although identification is unnecessary in the COMPTEL Analysis
            program, the feature has been left in case of future need

    """

    def __init__(self, position, mother=None):
        Volume.__init__(self, position, mother)



class D1(Volume):
    """
    The class for D1 modules.


    Attributes
    -----------
        id-- number to track all D1 modules
        position-- the Cartesian coordinates of the volume's center
        x-- the position's x coordinate
        y-- the position's y coordinate
        z-- the position's z coordinate
        mother-- the mother volume of the virtual volume (default argument
            is None)
        module_id-- an id to label a specific module (default argument is 0)
        id-- an id X.Y where X is a label for the volume type and Y is
            the module id

    Methods
    --------
        check_point-- returns True if the position falls within the volume,
            returns False if it does not.


    Notes
    -----
        ** the volume's position attributes are its absolute Cartesian
            coordinates, not relative to any mother volume
        ** the attribute 'id' corresponds to Cosima generated detector
            ID for Anger cameras.
        ** the value used for radius in D1 is an approximation, not exact
            (the modules were defined as 16-gons in Geomega, but considering
            a circle the polygon could be inscribed in is far more
            efficient both in code generation and wall time; the
            approximation is equally as accurate for the purpose of using
            the 'check_point' method)

    """

    radius = 14.56
    half_height = 4.25

    def __init__(self, position, mother=None, module_id=0):
        self.id = module_id
        Volume.__init__(self, position, mother)


    def check_point(self, point_position):
        x, y, z = point_position
        if z < (self.z - self.half_height) or z > (self.z + self.half_height):
            return False
        elif abs(x - self.x) > self.radius:
            return False
        elif abs(y - self.y) > self.radius:
            return False
        elif ((x - self.x)**2 + (y - self.y)**2) < (self.radius**2):
            return True
        else:
            return False


class D2(Volume):
    """
    The class for D2 modules.


    Attributes
    -----------
        id-- number to track all D2 modules
        position-- the Cartesian coordinates of the volume's center
        x-- the position's x coordinate
        y-- the position's y coordinate
        z-- the position's z coordinate
        mother-- the mother volume of the virtual volume (default argument
            is None)
        module_id-- an id to label a specific module (default argument is 0)
        id-- an id X.Y where X is a label for the volume type and Y is
            the module id

    Methods
    --------
        check_point-- returns True if the position falls within the volume,
            returns False if it does not.

    Notes
    -----
        ** the volume's position attributes are its absolute Cartesian
            coordinates, not relative to any mother volume
        ** the attribute 'id' corresponds to Cosima generated detector
            ID for Anger cameras.

    """

    radius = 15.085
    half_height = 3.7625

    def __init__(self, position, mother=None, module_id=0):
        self.id = module_id
        Volume.__init__(self, position, mother)

    def check_point(self, point_position):
        x, y, z = point_position
#        if z < (self.z - self.half_height) or z > (self.z + self.half_height):
#            print('part1')
#            return False
#        if abs(x) > (self.radius + abs(self.x)):
#            print('part2')
#            return False
#        elif abs(y)  > (self.radius + abs(self.y)):
#            print('part3')
#            return False
        if (((x - self.x)**2 + (y - self.y)**2)) < (self.radius**2):
            return True
            print('nice')
        else:
            return False
            print('the end')

# XXX I literally have no idea if any of this works
#   Veto dome method is definitely only guarunteed if inputting only
#   veto dome coordinate (ie. screening detector ID's)

class VetoDome1(Volume):
    """
    The class for Veto Dome 1.


    Attributes
    -----------
        id-- number to track all Veto Domes
        position-- the Cartesian coordinates of the volume's center
        x-- the position's x coordinate
        y-- the position's y coordinate
        z-- the position's z coordinate
        mother-- the mother volume of the virtual volume (default argument
            is None)
        module_id-- an id to label a specific module (default argument is 0)
        id-- an id X.Y where X is a label for the volume type and Y is
            the module id

    Methods
    --------
        check_point-- returns True if the position falls within the volume,
            returns False if it does not.

        ** Note that the volume's position attributes are its absolute
            Cartesian coordinates, not relative to any mother volume **


    The attribute 'id' corresponds to Cosima generated detector
    ID for scintillators.

    """

    id = 3.1

    def __init__(self, mother=None):
        self.mother = mother

    def check_point(self, point_position):
        x, y, z = point_position
        # if outside z range of dome return false
        if 140 < z < 35:
            return False
        # if in z range where there is no veto dome overlap return true
        elif z > 77:
            return True
        # if in z range where there is overlap but is in x, y range retrun true
        elif 73 < np.sqrt(x**2 + y**2) < 80:
            return True
        else:
            return False


class VetoDome2(Volume):
    """
    The class for Veto Dome 2.


    Documentation is functionally identical to VetoDome1. The VetoDome classes
    are defined seperate merely for ease of use. They were created with the
    intention of being used only for the analysis of COMPTEL simulation data.

    """
    id = 3.2
    def __init__(self, mother=None):
        self.mother = mother

    def check_point(self, point_position):
        x, y, z = point_position
        # if outside z range of dome return false
        if 80 < z < 25:
            return False
        # if in z range where there is no veto dome overlap return true
        elif z < 50:
            return True
        # if in z range where there is overlap but is in x, y range return true
        elif 64 < np.sqrt(x**2 + y**2) < 72:
            return True
        else:
            return False



class VetoDome3(Volume):
    """
    The class for Veto Dome 3.


    Documentation is functionally identical to VetoDome1. The VetoDome classes
    are defined seperate merely for ease of use. They were created with the
    intention of being used only for the analysis of COMPTEL simulation data.

    """
    id = 3.3
    def __init__(self, mother=None):
        self.mother = mother

    def check_point(self, point_position):
        x, y, z = point_position
        # if outside z range of dome return false
        if 2 < z < -88:
            return False
        # if in z range where there is no veto dome overlap return true
        elif z > -62:
            return True
        # if in z range where there is overlap but is in x, y range retrun true
        elif 72 < np.sqrt(x**2 + y**2) < 82:
            return True
        else:
            return False



class VetoDome4(Volume):
    """
    The class for Veto Dome 4.


    Functionally identical to VetoDome1. The VetoDome classes are defined
    seperate merely for ease of use. They were created with thE intention of
    being used only for the analysis of COMPTEL simulation data.

    """
    id = 3.4
    def __init__(self, mother=None):
        self.mother = mother

    def check_point(self, point_position):
        x, y, z = point_position
        # if outside z range of dome return false
        if -62 < z < -112:
            return False
        # if in z range where there is no veto dome overlap return true
        elif z < -86:
            return True
        # if in z range where there is overlap but is in x, y range return true
        elif 64 < np.sqrt(x**2 + y**2) < 72:
            return True
        else:
            return False






###########       COMPTEL Geometry       ################

# The entire detector
#    position relative to (0, 0, 0)
SETU = Virtual((0, 0, -117.4))

DET1 = Virtual((0, 0, 209.45), SETU)

D1_module1 = D1((0, 0, 10.3), DET1, 1.01)
D1_module2 = D1((-42.3, 0, 10.3), DET1, 1.02)
D1_module3 = D1((-26, 39.1, 10.3), DET1, 1.03)
D1_module4 = D1((26, 39.1, 10.3), DET1, 1.04)
D1_module5 = D1((42.3, 0, 10.3), DET1, 1.05)
D1_module6 = D1((26, -39.1, 10.3), DET1, 1.06)
D1_module7 = D1((-26, -39.1, 10.3), DET1, 1.07)

DET2 = Virtual((0, 0, 52.1), SETU)
D2shift = Virtual((0, 0, 14.3375), DET2)

D2_module1 = D2((30.2, -41.254, -4.6875), D2shift, 2.01)
D2_module2 = D2((0, -41.254, -4.6875), D2shift, 2.02)
D2_module3 = D2((-30.2, -41.254, -4.6875), D2shift, 2.03)
D2_module4 = D2((45.3, -15.1, -4.6875), D2shift, 2.04)
D2_module5 = D2((15.1, -15.1, -4.6875), D2shift, 2.05)
D2_module6 = D2((-15.1, -15.1, -4.6875), D2shift, 2.06)
D2_module7 = D2((-45.3, -15.1, -4.6875), D2shift, 2.07)
D2_module8 = D2((45.3, 15.1, -4.6875), D2shift, 2.08)
D2_module9 = D2((15.1, 15.1, -4.6875), D2shift, 2.09)
D2_module10 = D2((-15.1, 15.1, -4.6875), D2shift, 2.10)
D2_module11 = D2((-45.3, 15.1, -4.6875), D2shift, 2.11)
D2_module12 = D2((30.2, 41.254, -4.6875), D2shift, 2.12)
D2_module13 = D2((0, 41.254, -4.6875), D2shift, 2.13)
D2_module14 = D2((-30.2, 41.254, -4.6875), D2shift, 2.14)

VD1 = VetoDome1(SETU)
VD2 = VetoDome2(SETU)
VD3 = VetoDome3(SETU)
VD4 = VetoDome4(SETU)




def identify_COMPTELmodule(sim_data):
    """
    Uses hit location and detector type in order to detemine detector module.

    Paramerters
    ------------
        sim_data -- a row of a DataFrame containing the information of a
                neutron interaction
                (generally used with "apply" method of DataFrame)

    Returns
    --------
        the the ID of the detector module that the interaction occurred in
            format is X.Y where:
            X-- 1: D1,  2: D2,  3: VetoDome
            Y-- module id

    """
    position = (sim_data['x'], sim_data['y'], sim_data['z'])

    # if detector is Cosima Anger camera (ID: 7)
    #       these are the D1 and D2 layers
    if sim_data['DetectorID'] == 7:
        if sim_data['z'] > 5:
            if D1_module1.check_point(position): return D1_module1.id
            elif D1_module2.check_point(position): return D1_module2.id
            elif D1_module3.check_point(position): return D1_module3.id
            elif D1_module4.check_point(position): return D1_module4.id
            elif D1_module5.check_point(position): return D1_module5.id
            elif D1_module6.check_point(position): return D1_module6.id
            elif D1_module7.check_point(position): return D1_module7.id
            else: print("IN D1!!")
        elif sim_data['z'] < 5:
            if D2_module1.check_point(position): return D2_module1.id
            elif D2_module2.check_point(position): return D2_module2.id
            elif D2_module3.check_point(position): return D2_module3.id
            elif D2_module4.check_point(position): return D2_module4.id
            elif D2_module5.check_point(position): return D2_module5.id
            elif D2_module6.check_point(position): return D2_module6.id
            elif D2_module7.check_point(position): return D2_module7.id
            elif D2_module8.check_point(position): return D2_module8.id
            elif D2_module9.check_point(position): return D2_module9.id
            elif D2_module10.check_point(position): return D2_module10.id
            elif D2_module11.check_point(position): return D2_module11.id
            elif D2_module12.check_point(position): return D2_module12.id
            elif D2_module13.check_point(position): return D2_module13.id
            elif D2_module14.check_point(position): return D2_module14.id
            else: print("IN D2!!")
        else:
            print('help')
            return 17
    # if detector is Cosima scintillator (ID: 4)
    #       these are the veto domes
    elif sim_data['DetectorID'] == 4:
        if sim_data['z'] > 5:
            if VD1.check_point(position): return VD1.id
            elif VD2.check_point(position): return VD2.id
            else:
                print("IN VETO DOME 1 or 2!!")
        elif sim_data['z'] < 5:
            if VD3.check_point(position): return VD3.id
            elif VD4.check_point(position): return VD4.id
            else:
                print("IN VETO DOME 3 o4 4!!")
    elif sim_data['DetectorID'] == 0:
         return 0
    else:
        print("wut")
        return 99

