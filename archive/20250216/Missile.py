# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:53:22 2025

@author: Joost
"""
import numpy as np
import pandas as pd

class Missile:
    def __init__(self):
        """Create a new missile object at the origin."""
        self.time = 0
        
        self.position = np.array([0, 0])
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])

        self.orientation = np.pi/2 #rad, initially pointing up

        self.dry_mass = 50.0
        self.fuel = 250.0
        
        self.states = pd.DataFrame(columns=[
            "time", "pos_x", "pos_y", "vel_x", "vel_y", "acc_x", "acc_y", "orientation", "fuel"
        ])

    def log(self, time):
        """Log the current state of the missile."""
        new_row = pd.DataFrame([{
            "time": time,
            "pos_x": self.position[0], "pos_y": self.position[1],
            "vel_x": self.velocity[0], "vel_y": self.velocity[1],
            "acc_x": self.acceleration[0], "acc_y": self.acceleration[1],
            "orientation": self.orientation,
            "fuel": self.fuel
        }])

        self.states = pd.concat([self.states, new_row], ignore_index=True)


            