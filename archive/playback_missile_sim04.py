# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:45:53 2025

@author: Joost
"""
import pygame
import numpy as np
from ms_toolbox01 import plot_all_trajectories
#%%
# Constants
WIDTH, HEIGHT = 1200, 600
BACKGROUND_COLOR = (0, 0, 0)
MISSILE_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def get_global_bounds(missiles):
    """Compute global min and max values for x and y across all missiles."""
    x_min = min(np.min(missile.states["pos_x"]) for missile in missiles)
    x_max = max(np.max(missile.states["pos_x"]) for missile in missiles)
    y_min = 0  # Always keep y_min at ground level
    y_max = max(np.max(missile.states["pos_y"]) for missile in missiles)

    # Expand bounds by 10% for better visibility
    x_range = x_max - x_min
    y_range = y_max - y_min
    x_min -= 0.1 * x_range
    x_max += 0.1 * x_range
    y_max += 0.1 * y_range

    return x_min, x_max, y_min, y_max

def transform_coordinates(x, y, x_min, x_max, y_min, y_max, width, height):
    """Convert simulation coordinates to Pygame screen coordinates with uniform scaling."""
    scale_x = width / (x_max - x_min)
    scale_y = height / (y_max - y_min)
    scale = min(scale_x, scale_y)  # Maintain aspect ratio

    x_screen = int((x - x_min) * scale)
    y_screen = int(height - (y - y_min) * scale)  # Flip y-axis for screen

    return x_screen, y_screen

def run_visualization(sim, fps=60):
    """Visualize multiple missiles from a MissileSim instance."""
    missiles = sim.objects
    x_min, x_max, y_min, y_max = get_global_bounds(missiles)

    max_steps = max(len(missile.states) for missile in missiles)
    running, step = True, 0

    while running and step < max_steps:
        screen.fill(BACKGROUND_COLOR)
        
        pygame.draw.circle(screen, (0,0,255), (100,100), 10)
        pygame.draw.circle(screen, (0,255,255), (100,700), 10)
        pygame.draw.circle(screen, (255,0,255), (700,100), 10)
        pygame.draw.circle(screen, (255,255,255), (700,700), 10)
        
        for i,missile in enumerate(missiles):
            if step < len(missile.states):
                state = missile.states.iloc[step]
                x, y = transform_coordinates(state.pos_x, state.pos_y, x_min, x_max, y_min, y_max, WIDTH, HEIGHT)
                
                # Compute missile orientation point
                x2 = x - 10 * np.cos(state.orientation)
                y2 = y - 10 * np.sin(state.orientation)
                
                color = (255, 0, 0) if i == 0 else MISSILE_COLOR
                pygame.draw.line(screen, color, (x, y), (x2, y2), 2)
                
                if state.fuel>0:
                    pygame.draw.circle(screen, (255,255,0), (x, y), 5)
                    # pygame.draw.circle(screen, color, (x2, y2), 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        step += 1

    pygame.quit()



#%%

run_visualization(missile_sim)

#%%
plot_all_trajectories(missile_sim.objects, timestep)

#%% Plot results
plot_missile_data(missile, timestep)
#%%
plot_missile_data(missile_sim.objects[1], timestep)

