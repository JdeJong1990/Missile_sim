# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:23:38 2025

@author: Joost
"""
import numpy as np

class MissileSim:
    def __init__(self, objects, timestep):
        """Create a missile sim object, based on a list of missle objects."""
        self.objects = objects
        
    def get_acceleration(self, timestep, missile):
        """
        Thrust is 50 kN
        Forces: 
        - Thrust
        - Lift
        - Drag
        - Gravity
        """
        force = np.array([0,0])
        total_mass = missile.dry_mass + missile.fuel
        orientation_vector = np.array([np.cos(missile.orientation), np.sin(missile.orientation)])
        rotated_velocity = missile.velocity @ np.array([[np.cos(-missile.orientation), -np.sin(-missile.orientation)],
                                                 [np.sin(-missile.orientation),  np.cos(-missile.orientation)]])
        angle_of_attack = np.arctan2(rotated_velocity[1], rotated_velocity[0])


        # Thrust
        if missile.fuel > 0:
            thrust_force = 50000 * orientation_vector  # 50 kN in missile's direction
            fuel_burn_rate = 250 / 3  # 250 kg over 3 seconds
            missile.fuel = max(0, missile.fuel - fuel_burn_rate * timestep / 2) # Divide by two, because this function is used twice a timestep
        else:
            thrust_force = np.array([0, 0])

        force = force + thrust_force

        # Lift
        # perpendicular to the velocity
        if np.linalg.norm(missile.velocity) > 0:
            lift = np.array([missile.velocity[1], - missile.velocity[0]]) / np.linalg.norm(missile.velocity)
            C_lift = 1 * np.sin(2 * angle_of_attack)
            lift = lift * C_lift * 0.09 * np.linalg.norm(missile.velocity)**2
            force = force + lift

        # Drag (add pressure dependency)
        
        
        Acd = 0.09* (1.675 - 1.325 * np.cos(angle_of_attack * 2) - 0.15 * np.cos(angle_of_attack)) # add velocity dependency (sub, trans and super sonic)
        force = force - Acd*missile.velocity * np.linalg.norm(missile.velocity)

        # Gravity
        force += np.array([0, -9.81 * total_mass]) 

        acceleration = force / total_mass

        return acceleration

    def run(self, timestep):
        """Go through the list of objects and update their state by running the sim for one iteration."""
        for object in self.objects:
            self.update(object, timestep)
            
    def update(self, object, timestep):
        """ Update the conditions of the missle by one timestep."""
        object.acceleration = self.get_acceleration(timestep, object)
        object.velocity = object.velocity + 0.5 * object.acceleration * timestep  # Half-step velocity update
        object.position = object.position + object.velocity * timestep            # Position update with half-step velocity
        object.acceleration = self.get_acceleration(timestep, object)              # Compute new acceleration
        object.velocity = object.velocity + 0.5 * object.acceleration * timestep  # Complete the velocity update
        object.time += timestep
        
        object.orientation = (object.orientation + np.pi) % (2 * np.pi) - np.pi

        object.log(object.time)
        
        
        if (object.fuel<1) & (object.orientation > -0.5):
            object.orientation = object.orientation - 0.5*timestep