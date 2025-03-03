# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:45:53 2025

@author: Joost
"""

import pygame
import pandas as pd
import numpy as np

from ms_toolbox01 import plot_missile_data

#%%
# Constants
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (0, 0, 0)
MISSILE_COLOR = (255, 255, 255)
SCALE = 0.4  # Adjust this to fit your simulation scale

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Load simulation data (replace with actual file if saving data externally)
def load_simulation_data(missile):
    return missile.states  # Assuming missile.states is a pandas DataFrame

def transform_coordinates(x_sim, y_sim, x_data, y_data, width, height):
    """Transforms simulation coordinates to Pygame screen coordinates with equal scaling."""
    # Determine simulation bounds
    x_min, x_max = np.min(x_data), np.max(x_data)
    y_min, y_max = np.min(y_data), np.max(y_data)

    # Expand x range by 10% on both sides
    x_range = x_max - x_min
    x_min -= 0.1 * x_range
    x_max += 0.1 * x_range

    # y_min is always 0 (bottom of screen), expand y_max by 10%
    y_min = 0
    y_range = y_max - y_min
    y_max += 0.1 * y_range

    # Determine uniform scale factor
    scale_x = width / (x_max - x_min)
    scale_y = height / (y_max - y_min)
    scale = min(scale_x, scale_y)  # Ensure uniform scaling

    # Convert coordinates
    x_screen = int((x_sim - x_min) * scale)
    y_screen = int(height - (y_sim - y_min) * scale)  # Flip y-axis for screen

    return x_screen, y_screen


def run_visualization(missile, fps=60):
    data = load_simulation_data(missile)
    x_data = data['pos_x'].to_numpy()
    y_data = data['pos_y'].to_numpy()
    orientation_data = data['orientation'].to_numpy()
    
    max_index = len(x_data)
    running = True
    index = 0
    
    while running and index < max_index:
        screen.fill(BACKGROUND_COLOR)
        
        # Convert simulation coordinates to Pygame coordinates
        x, y = transform_coordinates(x_data[index], y_data[index], x_data, y_data, WIDTH, HEIGHT)
        # x = int(x_data[index] * SCALE + WIDTH // 2)
        # y = int(HEIGHT - y_data[index] * SCALE)  # Flip y-axis for screen
        
        x2 = x + 10*np.cos(orientation_data[index])
        y2 = y + 10*np.sin(orientation_data[index])
        
        pygame.draw.circle(screen, MISSILE_COLOR, (x, y), 5)
        pygame.draw.circle(screen, MISSILE_COLOR, (x2, y2), 5)
        pygame.display.flip()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(fps)
        index += 1
    
    pygame.quit()

# Example usage (replace `missile` with your actual missile object)
# run_visualization(missile)

#%%
print(f'Max x: {missile.position[0]:.5}')
run_visualization(missile)


#%% Plot results
plot_missile_data(missile, timestep)


