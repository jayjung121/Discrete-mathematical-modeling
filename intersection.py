# -*- coding: utf-8 -*-sel
"""
Created on Sat Aug  4 18:14:22 2018

@author: ByungsuJung
"""

class Intersection(object):
    
    def __init__(self, name, x, y, weight, zipcode, map=None):
        self.name = name
        self.x = x
        self.y = y
        self.weight = weight
        self.zipcode = zipcode
        self.map = map

        
    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)