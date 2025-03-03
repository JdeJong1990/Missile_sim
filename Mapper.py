# -*- coding: utf-8 -*-
"""
Created on Mon Feb 24 19:41:43 2025

@author: Joost

Map from simulation space to screen space. 
"""

class Mapper:
    def __init__(self, width, height, sim = None, padding=0.1):
        """Initialize the coordinate mapper with padding in the x-direction and extra space above."""
        self.width = width
        self.height = height
        self.padding = padding
        
        # Get global bounds
        if sim == None:
            x_min = -50000
            x_max = 1000
            y_min = -200
            y_max = 12000
        else:
            x_min, x_max, y_min, y_max = self.get_global_bounds(sim.objects)

        # Expand x bounds by 10% on each side
        x_range = x_max - x_min
        self.x_min = x_min - padding * x_range
        self.x_max = x_max + padding * x_range

        # Expand y bounds by 10% on the top only
        y_range = y_max - y_min
        self.y_min = y_min  # Keep the bottom as it is
        self.y_max = y_max + padding * y_range  

        # Compute uniform scale to maintain aspect ratio
        scale_x = self.width / (self.x_max - self.x_min)
        scale_y = self.height / (self.y_max - self.y_min)
        self.scale = min(scale_x, scale_y)  # Maintain aspect ratio

    def get_global_bounds(self, missiles):
        """Find the min and max values for x and y from all missiles."""
        x_min = min(min(missile.states["pos_x"]) for missile in missiles)
        x_max = max(max(missile.states["pos_x"]) for missile in missiles)
        y_min = min(min(missile.states["pos_y"]) for missile in missiles)
        y_max = max(max(missile.states["pos_y"]) for missile in missiles)
        return x_min, x_max, y_min, y_max

    def transform(self, coordinate):
        """Convert simulation coordinates to screen coordinates."""
        x = coordinate[0]
        y = coordinate[1]
        
        x_screen = int((x - self.x_min) * self.scale)
        y_screen = int(self.height - (y - self.y_min) * self.scale)  # Flip y-axis for screen
        return x_screen, y_screen
