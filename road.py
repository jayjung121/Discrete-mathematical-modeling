# -*- coding: utf-8 -*-
"""
Created on Mon Aug  6 17:10:23 2018

@author: ByungsuJung
"""

class Road(object):
    
    def __init__(self, name,start, destination, length):
        self.name = name #int
        self.u = start #Node u 
        self.v = destination #Node v
        self.length = length #meters, float
