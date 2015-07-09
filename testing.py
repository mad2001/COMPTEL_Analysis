# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod

import numpy as np


def absolute_position(daughter_position, mother_position):
    new_position = np.add(mother_position, daughter_position)
    return new_position




