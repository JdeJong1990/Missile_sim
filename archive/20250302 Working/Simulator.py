# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:23:38 2025

@author: Joost
"""
import numpy as np
from Measurement import Measurement
from ms_toolbox01 import rotate_vector

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
            print(self.objects[1].control_surface)
                
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
        
        obj.orientation = obj.orientation + self.get_torque(obj)
        
        # Wrap orientation angle
        obj.orientation = (obj.orientation + np.pi) % (2 * np.pi) - np.pi
        obj.control_surface = np.clip(obj.control_surface, -1, 1)
        
        obj.log(obj.time)
        
        # Sent measurements of the target to the missile
        obj.control(Measurement(self.objects[0], obj), timestep)
      
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
            lift_direction = rotate_vector(missile.velocity, np.pi/2) / np.linalg.norm(missile.velocity)
            # lift_direction = np.array([missile.velocity[1], -missile.velocity[0]]) / np.linalg.norm(missile.velocity) # Velocity direction rotated 90° clockwise
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
        """ Determine the angle of attack of a missile in its current state"""
        orientation = missile.orientation
        velocity = missile.velocity
        
        rotated_velocity = rotate_vector(velocity, -orientation)

        angle_of_attack = -np.arctan2(rotated_velocity[1], rotated_velocity[0])
        return angle_of_attack
         
    def get_torque(self, missile):
        """Determine the torque that is applied on the missile as a result of the tail and controll surfaces"""
        torque = - missile.tail_inertia * np.sin(self.angle_of_attack(missile) + missile.control_surface)
        
        return torque