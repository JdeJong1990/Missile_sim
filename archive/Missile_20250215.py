# -*- coding: utf-8 -*-
"""
Created on Fri Feb 14 11:53:22 2025

@author: Joost
"""
import numpy as np

class Missile:
    def __init__(self):
        """Create a new missile object at the origin."""
        self.position = np.array([0, 0])
        self.velocity = np.array([0, 0])
        self.acceleration = np.array([0, 0])

        self.orientation = np.pi/2 #rad, initially pointing up

        self.dry_mass = 50
        self.fuel = 250

    def get_acceleration(self, timestep):
        """
        Thrust is 50 kN
        Forces: 
        - Thrust
        - Lift
        - Drag
        - Grafity
        """
        force = np.array([0,0])
        total_mass = self.dry_mass + self.fuel
        orientation_vector = np.array([np.cos(self.orientation), np.sin(self.orientation)])
        if np.linalg.norm(self.velocity) > 0:  # Avoid division by zero
                    velocity_unit = self.velocity / np.linalg.norm(self.velocity)
                    orientation_unit = orientation_vector / np.linalg.norm(orientation_vector)
                    angle_of_attack = np.arccos(np.clip(np.dot(velocity_unit, orientation_unit), -1.0, 1.0))
        else:
            angle_of_attack = 0  # No AoA if not moving

        # Thrust
        if self.fuel > 0:
            thrust_force = 50000 * orientation_vector  # 50 kN in missile's direction
            fuel_burn_rate = 250 / 3  # 250 kg over 3 seconds
            self.fuel = max(0, self.fuel - fuel_burn_rate * timestep)
        else:
            thrust_force = np.array([0, 0])

        force = force + thrust_force

        # Lift
        # perpendicular to the velocity
        if np.linalg.norm(self.velocity) > 0:
            lift = np.array([self.velocity[1], -self.velocity[0]]) / np.linalg.norm(self.velocity)
            C_lift = 1 * np.sin(2 * angle_of_attack)
            lift = lift * C_lift * 0.09 * np.linalg.norm(self.velocity)**2
            force = force + lift

        # Drag (add pressure dependency)
        
        
        Acd = 0.09* (1.675 - 1.325 * np.cos(angle_of_attack * 2) - 0.15 * np.cos(angle_of_attack)) # add velocity dependency (sub, trans and super sonic)
        force = force - Acd*self.velocity * np.linalg.norm(self.velocity)

        # Gravity
        force += np.array([0, -9.81 * total_mass]) 

        acceleration = force / total_mass

        return acceleration

    def run(self, timestep):
        """ Update the conditions of the missle by one timestep."""
        self.acceleration = self.get_acceleration(timestep)
        self.velocity = self.velocity + 0.5 * self.acceleration * timestep  # Half-step velocity update
        self.position = self.position + self.velocity * timestep            # Position update with half-step velocity
        self.acceleration = self.get_acceleration(timestep)              # Compute new acceleration
        self.velocity = self.velocity + 0.5 * self.acceleration * timestep  # Complete the velocity update
        if (self.fuel<1) & (self.orientation > 0.6):
            self.orientation = self.orientation - 0.05