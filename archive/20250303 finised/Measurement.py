# -*- coding: utf-8 -*-
"""
Created on Sun Feb 16 14:41:14 2025

@author: Joost
"""
import numpy as np

from ms_toolbox01 import rotate_vector

class Measurement:
    def __init__(self, target, missile):
        """
        Calculate the measurements that a missile could do when detecting a target
        It determines the distance, at what angle it detects the target, 
        and how fast the two objects are approaching each other.
        """
        connecting_vector = target.position - missile.position
        self.distance = np.linalg.norm(connecting_vector)
        
        detection_vector = rotate_vector(connecting_vector, -missile.orientation)

        self.direction = np.arctan2(detection_vector[1], detection_vector[0]) + np.pi

        self.direction = (self.direction + np.pi) % (2 * np.pi) - np.pi
        
        self.closing_speed = np.linalg.norm(target.velocity - missile.velocity)
        