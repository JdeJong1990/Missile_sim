# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:23:38 2025

@author: Joost
"""
import numpy as np
from Measurement import Measurement

class Simulator:
    def __init__(self, objects):
        """Create a missile sim object, based on a list of missile objects."""
        self.objects = objects
    
    def sim(self, num_loops, timestep):
        """ Run num_loops of timesteps with the given objects"""
        for _ in range(num_loops):
            self.run(timestep)
            if self.objects[0].position[1]<-1:
                break

    def run(self, timestep):
        """Go through the list of objects and update their state by running the sim for one iteration."""
        for obj in self.objects:
            if (obj.delay > 0) or obj.position[1]<-1:
                self.delay(obj, timestep)
            else: 
                self.update(obj, timestep)
                
    def delay(self, obj, timestep):
        """ When a missile is delayed, we don't update its physics, just let its delay run out"""
        obj.delay = obj.delay - timestep 
        obj.time = obj.time + timestep
        obj.log(obj.time)
        
        
    def update(self, obj, timestep):
        """Update the conditions of the missile by one timestep."""
        obj.acceleration = self.get_acceleration(timestep, obj)
        obj.velocity = obj.velocity + 0.5 * obj.acceleration * timestep  # Half-step velocity update
        obj.position = obj.position + obj.velocity * timestep            # Position update with half-step velocity
        obj.acceleration = self.get_acceleration(timestep, obj)  # Compute new acceleration
        obj.velocity = obj.velocity + 0.5 * obj.acceleration * timestep  # Complete the velocity update
        obj.time = obj.time + timestep

        # Wrap orientation angle
        obj.orientation = (obj.orientation + np.pi) % (2 * np.pi) - np.pi
        
        obj.log(obj.time)
        
        # Sent measurements of the target to the missile
        obj.control(Measurement(self.objects[0], obj), timestep)
        # if obj.fuel < 1 and obj.orientation > -0.2:
        #     obj.orientation = obj.orientation - 0.2 * timestep
      
    def get_acceleration(self, timestep, missile):
        """
        Compute acceleration considering:
        - Thrust
        - Lift
        - Drag
        - Gravity
        """
        force = np.array([0.0, 0.0])
        total_mass = missile.dry_mass + missile.fuel
        orientation_vector = np.array([np.cos(missile.orientation), np.sin(missile.orientation)])
        angle_of_attack = self.angle_of_attack(missile)

        # Thrust
        if missile.fuel > 0:
            thrust_force = missile.max_thrust * orientation_vector
            missile.fuel = max(0, missile.fuel - missile.fuel_burn_rate * timestep / 2)  # Half-step consumption, happens twice per timestep
        else:
            thrust_force = np.array([0.0, 0.0])

        force = force + thrust_force

        # Lift (perpendicular to velocity)
        if np.linalg.norm(missile.velocity) > 0:
            lift_direction = np.array([missile.velocity[1], -missile.velocity[0]]) / np.linalg.norm(missile.velocity) # Velocity direction rotated 90° clockwise
            C_lift = missile.Cl_alpha * np.sin(2 * angle_of_attack)
            lift_force = lift_direction * C_lift * missile.lift_area * np.linalg.norm(missile.velocity) ** 2
            force = force + lift_force

        # Drag (pressure dependency added later)
        # aoa_drag = min(abs(angle_of_attack),np.pi/2)
        aoa_drag = angle_of_attack
        C_drag = missile.Cd0 * (1.675 - 1.325 * np.cos(aoa_drag * 2) - 0.15 * np.cos(aoa_drag))
        drag_force = -C_drag * missile.velocity * np.linalg.norm(missile.velocity) * missile.frontal_area
        force = force + drag_force

        # Gravity
        force = force + np.array([0.0, -9.81 * total_mass]) 
        
        acceleration = force / total_mass
        return acceleration

    def angle_of_attack(self, missile):
        rotated_velocity = missile.velocity @ np.array([[np.cos(-missile.orientation), -np.sin(-missile.orientation)],
                                                        [np.sin(-missile.orientation),  np.cos(-missile.orientation)]])
        angle_of_attack = np.arctan2(rotated_velocity[1], rotated_velocity[0])
        
        
        # orientation = missile.orientation
        # velocity = missile.velocity
        
        # rotation_matrix = np.array([[np.cos(-orientation), -np.sin(-orientation)],
        #                             [np.sin(-orientation),  np.cos(-orientation)]])
        
        # velocity = np.atleast_2d(velocity).T  # Convert (2,) to (2,1) if needed
        # rotated_velocity = rotation_matrix @ velocity  # Correct transformation
        # rotated_velocity = rotated_velocity.flatten()  # Convert back to (2,) if needed

        # angle_of_attack = -np.arctan2(rotated_velocity[1], rotated_velocity[0])
        return angle_of_attack
         
