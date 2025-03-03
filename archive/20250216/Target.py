# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:40:41 2025

@author: Joost
"""
import numpy as np

class Target: 
    """ Target object for missiles in the missile sim to hit"""
    def __init__(self):
        self.position = np.array([-3000, 0])
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])
        self.orientation = 0
        self.dry_mass = 1000
        self.fuel = 0
        self.time = 0

    def log(self, time):
        pass  # Implement logging if needed
