# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:45:53 2025

@author: Joost
"""
import pygame
import numpy as np

from ms_toolbox01 import plot_all_trajectories
from Mapper import Mapper
#%%
# Constants

WIDTH, HEIGHT = 1200, 600
BACKGROUND_COLOR = (0, 0, 0)
MISSILE_COLOR = (255, 255, 255)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()


def wait_for_click():
    """Wait for a mouse click before starting the simulation."""
    waiting = True
    while waiting:
        screen.fill((30, 30, 30))  # Slightly different background color to show it's in waiting mode
        font = pygame.font.Font(None, 36)
        text = font.render("Click anywhere to start simulation", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False


def run_visualization(sim, fps=60):
    """Visualize multiple missiles from a MissileSim instance."""
    mapper = Mapper(WIDTH, HEIGHT, sim)

    missiles = sim.objects
    max_steps = max(len(missile.states) for missile in missiles)

    # Wait for user click before starting
    wait_for_click()

    running, step = True, 0

    while running and step < max_steps:
        screen.fill(BACKGROUND_COLOR)
        
        for i, missile in enumerate(missiles):
            if step < len(missile.states):
                state = missile.states.iloc[step]
                x, y = state.pos_x, state.pos_y
                uv = mapper.transform((x, y))
                uv2 = mapper.transform((x + 400 * np.cos(state.orientation), 
                                        y + 400 * np.sin(state.orientation)))

                color = (255, 0, 0) if i == 0 else MISSILE_COLOR
                pygame.draw.line(screen, color, uv, uv2, 4)

                if state.fuel > 0:
                    pygame.draw.circle(screen, (255, 255, 0), uv, 5)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        clock.tick(fps)
        step += 1

    pygame.quit()


# Run the visualization
run_visualization(missile_sim)


#%%
plot_all_trajectories(missile_sim.objects, timestep)

#%% Plot results
plot_missile_data(missile_sim.objects[1], timestep)
#%%
plot_missile_data(missile_sim.objects[1], timestep)

