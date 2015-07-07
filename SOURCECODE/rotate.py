# -*- coding: utf-8 -*-
"""
Created on Mon Jul  6 12:20:50 2015

@author: morgan
"""

def rotatep(p, pr, angle):
        '''Rotate a single point p angle radians around pr'''
        sinr, cosr = sin(angle), cos(angle)
        x, y, z = p
        xRel, yRel, zRel = pr
        newx = x * cosr - y * sinr - xRel * cosr + yRel * sinr + xRel
        newy = x * sinr + y * cosr - xRel * sinr - yRel * cosr + yRel
        pr = (newx, newy)
        return pr

def rotatecp(cp, pr, angle):
        '''Rotate point-set cp angle radians around pr'''
        sinr, cosr = sin(angle), cos(angle)
        cpr = []
        for p in cp:
                x, y = p
                xRel, yRel = pr
                newx = x * cosr - y * sinr - xRel * cosr + yRel * sinr + xRel
                newy = x * sinr + y * cosr - xRel * sinr - yRel * cosr + yRel
                cpr.append((newx, newy))
        return cpr