# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:45:53 2025

@author: Joost
"""
import pygame

import numpy as np
#%%

# Constants
WIDTH, HEIGHT = 1200, 800
BACKGROUND_COLOR = (0, 0, 0)
MISSILE_COLOR = (255, 255, 255)
SCALE = 0.4  # Adjust to fit your simulation scale

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def transform_coordinates(x_sim, y_sim, x_data, y_data, width, height):
    """Transforms simulation coordinates to Pygame screen coordinates with equal scaling."""
    x_min, x_max = np.min(x_data), np.max(x_data)
    y_min, y_max = np.min(y_data), np.max(y_data)
    
    x_range = x_max - x_min
    x_min -= 0.1 * x_range
    x_max += 0.1 * x_range
    
    y_min = 0
    y_range = y_max - y_min
    y_max += 0.1 * y_range
    
    scale_x = width / (x_max - x_min)
    scale_y = height / (y_max - y_min)
    scale = min(scale_x, scale_y)
    
    x_screen = int((x_sim - x_min) * scale)
    y_screen = int(height - (y_sim - y_min) * scale)  # Flip y-axis for screen
    
    return x_screen, y_screen

def run_visualization(sim, fps=60):
    """Visualize multiple missiles from a MissileSim instance."""
    data_list = [missile.states for missile in sim.objects]

    x_data_all = [data["pos_x"].to_numpy() for data in data_list]
    y_data_all = [data["pos_y"].to_numpy() for data in data_list]
    orientation_all = [data["orientation"].to_numpy() for data in data_list]
    
    max_index = max(len(data) for data in data_list)
    running = True
    index = 0

    while running and index < max_index:
        screen.fill(BACKGROUND_COLOR)
        
        for i, missile in enumerate(sim.objects):
            data = data_list[i]
            if index < len(data):
                x_data = x_data_all[i]
                y_data = y_data_all[i]
                orientation_data = orientation_all[i]
                
                x, y = transform_coordinates(x_data[index], y_data[index], x_data, y_data, WIDTH, HEIGHT)
                x2 = x + 10 * np.cos(orientation_data[index])
                y2 = y + 10 * np.sin(orientation_data[index])
                
                pygame.draw.circle(screen, MISSILE_COLOR, (x, y), 5)
                pygame.draw.circle(screen, MISSILE_COLOR, (x2, y2), 5)
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        clock.tick(fps)
        index += 1
    
    pygame.quit()


#%%
print(f'Max x: {missile.position[0]:.5}')
run_visualization(missile_sim)


#%% Plot results
plot_missile_data(missile, timestep)
#%%
plot_missile_data(target, timestep)

