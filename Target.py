# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 11:40:41 2025

@author: Joost
"""
import numpy as np
import pandas as pd

class Target: 
    """ 
    Target object for missiles in the missile sim to hit
    Based on the 3M54 Kalibr (NATO reporting name: SS-N-27 "Sizzler"
    """
    def __init__(self):
        """Create a new missile object at the origin."""
        self.time = 0
        
        self.position = np.array([-50000, 2000])
        self.velocity = np.array([100, 0])
        self.acceleration = np.array([0, 0])

        self.orientation = 0.2  # rad

        # Mass properties
        self.dry_mass = 500.0
        self.fuel = 200.0
        self.fuel_burn_rate = 200 / 15  # kg/s 
        
        # Aerodynamic properties
        self.frontal_area = 0.12  # m² (approximate cross-section)
        self.lift_area = 0.25  # m² (reference area for lift)
        self.Cd0 = 0.15  # Base drag coefficient at zero AoA
        self.Cl_alpha = 2 * np.pi  # Lift curve slope (approximation)
        self.tail_inertia = 0.01
        self.control_surface = 0
        
        # Thrust
        self.max_thrust = 30000  # N (50 kN peak thrust)
        
        self.delay = 0
        # Logging
        self.states = pd.DataFrame(columns=[
            "time", "pos_x", "pos_y", "vel_x", "vel_y", "acc_x", "acc_y", "orientation", "fuel"
        ])
        
    def control(self, measurement, timestep):
        if (-self.position[0])>3000:
            self.control_surface = self.control_surface + timestep * (0.01 * np.clip((self.position[1] - 2000), -100,100)
                                                                      + 50.0 * self.orientation)
        else:
            target_angle = np.arctan2(-self.position[1], -self.position[0]) 
            self.control_surface = self.control_surface - timestep * 10 * np.sign(target_angle)
            
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
