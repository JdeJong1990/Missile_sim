# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:40:41 2025

@author: Joost
"""
import numpy as np
import pandas as pd

class Target: 
    """ Target object for missiles in the missile sim to hit"""
    def __init__(self):
        """Create a new missile object at the origin."""
        self.time = 0
        
        self.position = np.array([-14215, 3560])
        self.velocity = np.array([100, 0])
        self.acceleration = np.array([0, 0])

        self.orientation = 0.2  # rad, initially pointing up

        # Mass properties
        self.dry_mass = 250.0
        self.fuel = 100.0
        self.fuel_burn_rate = 250 / 3  # kg/s (burns out in 3 seconds)

        # Aerodynamic properties
        self.frontal_area = 0.03  # m² (approximate cross-section)
        self.lift_area = 0.09  # m² (reference area for lift)
        self.Cd0 = 4.1  # Base drag coefficient at zero AoA
        self.Cl_alpha = 2 * np.pi  # Lift curve slope (approximation)
        
        # Thrust
        self.max_thrust = 50000  # N (50 kN peak thrust)
        
        self.delay = 0
        # Logging
        self.states = pd.DataFrame(columns=[
            "time", "pos_x", "pos_y", "vel_x", "vel_y", "acc_x", "acc_y", "orientation", "fuel"
        ])
        
    def control(self, measurement, timestep):
        pass

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
