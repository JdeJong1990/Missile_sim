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

    def run(self, timestep = 0.05):
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
        total_mass = missile.dry_mass + missile.fuel
        force = np.array([0.0, 0.0])
        
        # Compute individual forces
        thrust_force = self._compute_thrust(missile, timestep)
        lift_force = self._compute_lift(missile)
        drag_force = self._compute_drag(missile)
        gravity_force = self._compute_gravity(total_mass)
    
        # Sum forces
        force += thrust_force + lift_force + drag_force + gravity_force
    
        # Compute acceleration
        acceleration = force / total_mass
        return acceleration


    def _compute_thrust(self, missile, timestep):
        """Computes the thrust force and updates fuel levels."""
        if missile.fuel > 0:
            orientation_vector = np.array([np.cos(missile.orientation), np.sin(missile.orientation)])
            thrust_force = missile.max_thrust * orientation_vector
            missile.fuel = max(0, missile.fuel - missile.fuel_burn_rate * timestep / 2)  # Half-step consumption
        else:
            thrust_force = np.array([0.0, 0.0])
        
        return thrust_force

    
    def _compute_lift(self, missile):
        """Computes the lift force acting perpendicular to velocity, considering altitude-dependent air density."""
        if np.linalg.norm(missile.velocity) == 0:
            return np.array([0.0, 0.0])
    
        altitude = missile.position[1]  # Get altitude from missile position
        air_density = self.air_density(altitude)  # Compute air density at altitude
    
        angle_of_attack = self.angle_of_attack(missile)
        lift_direction = rotate_vector(missile.velocity, np.pi/2) / np.linalg.norm(missile.velocity)
        C_lift = missile.Cl_alpha * np.sin(2 * angle_of_attack)
    
        # Incorporate air density into lift equation
        lift_force = 0.5 * air_density * missile.lift_area * C_lift * np.linalg.norm(missile.velocity) ** 2 * lift_direction
    
        return lift_force
    
    def _compute_drag(self, missile):
        """Computes the drag force opposing motion, considering altitude-dependent air density."""
        altitude = missile.position[1]  # Extract altitude from missile position
        rho = self.air_density(altitude)  # Get air density at current altitude
    
        angle_of_attack = self.angle_of_attack(missile)
        C_drag = missile.Cd0 * (1 + 1.5 * np.sin(angle_of_attack)**2)

        # Drag equation: F_drag = 0.5 * rho * v^2 * A * Cd
        drag_force = -0.5 * rho * missile.velocity * np.linalg.norm(missile.velocity) * missile.frontal_area * C_drag
    
        return drag_force
    
    def _compute_gravity(self, total_mass):
        """Computes the gravitational force acting downward."""
        return np.array([0.0, -9.81 * total_mass])


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
    
    def air_density(self, altitude):
        """
        Approximates air density (kg/m^3) as a function of altitude (meters) 
        in the range of 0 to 10 km using the International Standard Atmosphere (ISA) model.
        """
        # Constants for ISA model in the troposphere (0-10 km)
        rho0 = 1.225  # kg/m^3 (sea-level density)
        h_scale = 8500  # Scale height in meters (approximate)

        return rho0 * np.exp(-altitude / h_scale)

    