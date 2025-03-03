# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:53:22 2025

@author: Joost
"""
import numpy as np
import pandas as pd

class Missile:
    def __init__(self, delay = 0, guidance = True):
        """Create a new missile object at the origin."""
        self.time = 0
        
        self.position = np.array([0, 10])
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])

        self.orientation = np.pi/2  # rad, initially pointing up

        # Mass properties
        self.dry_mass = 400.0
        self.fuel = 700.0
        self.fuel_burn_rate = 700 / 6  # kg/s (burns out in 6 seconds)

        # Aerodynamic properties
        self.frontal_area = 0.055 # m² (approximate cross-section)
        self.lift_area = 0.2 # m² (reference area for lift)
        self.Cd0 = 0.3  # Base drag coefficient at zero AoA
        self.Cl_alpha = 2 * np.pi  # Lift curve slope (approximation)
        self.tail_inertia = 0.01
        self.control_surface = 0
        
        # Thrust
        self.max_thrust = 200E3  # N 
        
        self.proximity = 10000
        self.delay = delay
        
        self.guidance = guidance
        # Logging
        self.states = pd.DataFrame(columns=[
            "time", "pos_x", "pos_y", "vel_x", "vel_y", "acc_x", "acc_y", "orientation", "fuel"
        ])
    
    def control(self, measurement, timestep):
        """Use the measurements of the target detection to control the missile"""
        if measurement.distance < self.proximity: self.proximity = measurement.distance
        
        if ((self.fuel<10) and (self.guidance == True)):
            self.control_surface = self.control_surface + 2.0 * timestep * (measurement.direction + -2.7)

        
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
