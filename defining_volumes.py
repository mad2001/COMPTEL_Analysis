# -*- coding: utf-8 -*-

"""

These are measurements that correspond with those used in the construction
of geometry for MEGAlib simulations.
They may vary slightly from actual COMPTEL measurements.

All measurements are in centimeters.





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

    id = 0

    def __init__(self, position, mother=None, module_id=0):
        self.mother = mother
        while mother is not None:
            position = np.add(position, mother.position)
            mother = mother.mother
        self.position = position
        self.x = self.position[0]
        self.y = self.position[1]
        self.z = self.position[2]
        self.module_id = module_id
        self.id = self.id + module_id*.1



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
        module_id-- an id to label a specific module (default argument is 0)
        id-- an id X.Y where X is a label for the volume type and Y is
            the module id

    Notes
    ------
        ** the volume's position attributes are its absolute
            Cartesian coordinates, not relative to any mother volume

    """

    id = 0

    def __init__(self, position, mother=None):
        Volume.__init__(self, position, mother)



class D1(Volume):
    """
    The class for D1 modules.


    Attributes
    -----------
        id-- number to track all
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
            (the modules were defined as 16-gons in Geomega, but treating
            them as cylinders is far more efficient both in code generation
            and wall time; the approximation is equally as accurate for
            purposes of using the 'check_point' method)

    """

    id = 7

    def __init__(self, position, mother=None):
        Volume.__init__(self, position, mother)


    def check_point(self, point_position):
        #@todo fix this
        x, y, z = point_position
        if z < (self.z - self.half_height) or z > (self.z + self.half_height):
            return False
        if abs(x - self.x) > self.radius:
            return False
        if abs(y - self.y) > self.radius:
            return False
        if (x - self.x)**2 + (y - self.y)**2 < self.radius**2:
            return True
        else:
            print("What did you doo=..?")



class D2(Volume):
    """
    The class for D2 modules.


    Attributes
    -----------
        id-- number to track all
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
    ID for Anger cameras.

    Radius is wrong
    """

    id = 7
    radius = 14.085
    half_height = 3.7625

    def __init__(self, position, mother=None):
        Volume.__init__(self, position, mother)

    def check_point(self, point_position):
        #@todo fix this
        x, y, z = point_position
        if z < (self.z - self.half_height) or z > (self.z + self.half_height):
            return False
        if abs(x - self.x) > self.radius:
            return False
        if abs(y - self.y) > self.radius:
            return False
        if (x - self.x)**2 + (y - self.y)**2 < self.radius**2:
            return True
        else:
            print("What did you doo=..?")



class VetoDome1(Volume):
    """
    The class for D1 modules.


    Attributes
    -----------
        id-- number to track all
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
    ID for Anger cameras.

    Radius is wrong
    """
    id = 4
    def __init__(self, position, mother=None):
        self.position = position
        self.mother = mother
        Volume.__init__(self, position, mother)

    def check_point():
        return True
        return False


#D1_module1 = D1((x, y, z), mother=SETU)


## The coordinates of the detectors as defined in the Geomega geometry
#SETU_coords = (0, 0, -117.4)
## SETU = Volume.Virtual((0, 0, -117.4))
#
## daughter of SETU
#DET1_coords = (0, 0, 209.45)
#
## daughter of DET1
#D1module_coords = np.empty(7)
#D1module_coords[0] = (0, 0, 10.3)
#D1module_coords[1] = (-42.3, 0, 10.3)
#D1module_coords[2] = (-26, 39.1, 10.3)
#D1module_coords[3] = (26, 39.1, 10.3)
#D1module_coords[4] = (42.3, 0, 10.3)
#D1module_coords[5] = (26, -39.1, 10.3)
#D1module_coords[6] = (-26, -39.1, 10.3)
#
## daughter of SETU
#DET2_coords = (0, 0, 52.1)
## daughter of each module
#D2SN_coords = (0, 0, 14.3375)
## daughter of DET2
#D2module_coords[0] = np.empty(14)
#D2module_coords[1] = (30.2, -41.254, -4.6875)
#D2module_coords[2] = (0, -41.254, -4.6875)
#D2module_coords[3] = (45.3, -15.1, -4.6875)
#D2module_coords[4] = (15.1, -15.1, -4.6875)
#D2module_coords[5] = (-15.1, -15.1, -4.6875)
#D2module_coords[6] = (-45.3, -15.1, -4.6875)
#D2module_coords[7] = (45.3, 15.1, -4.6875)
#D2module_coords[8] = (15.1, 15.1, -4.6875)
#D2module_coords[9] = (-15.1, 15.1, -4.6875)
#D2module_coords[10] = (-45.3, 15.1, -4.6875)
#D2module_coords[11] = (30.2, 41.254, -4.6875)
#D2module_coords[12] = (0, 41.254, -4.6875)
#D2module_coords[13] = (-30.2, 41.254, -4.6875)
#
#
#def absolute_position(daughter_position, mother_position):
#    new_position = np.add(mother_position, daughter_position)
#    return new_position
#
#absolute_position(DET)
#
#
#
#vetodome1
#z
#75.5<r<77.2
#vetodome2
#z
#68<r<69.6
#
#vetodome3
#z
#76<r<77.7
#vetodome4
#z
#68<r<69.6
#
