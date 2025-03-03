# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 14:10:29 2025

@author: Joost
"""
import numpy as np
import pygame

from Mapper import Mapper
from Missile import Missile
from Target import Target


class SimPlayer:
    def __init__(self, missile_sim):
        self.sim = missile_sim
        self.width = 1200
        self.height = 600
        self.mapper = Mapper(self.width, self.height)
        
        self.screen = None
        self.clock = None
        
        # Load the image (do this once, e.g., during initialization)
        self.my_image = pygame.image.load("naval_ship_indicator.png")
            
    def live_sim(self, numloops, fps=60):
        """Show the last state and run the sim one step."""
        self.initiate_window()
        
        for _ in range(numloops):
            self.screen.fill((0, 0, 0))
            self.sim.run()          # No time step means 0.05 seconds
            self.show_step(-1)      # Show the last time step
            self.show_icon()        # Show naval ship icon
            pygame.display.flip()
            self.clock.tick(fps)
            self.respond()
        pygame.quit()
        
    def respond(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
                # exit()
        
    def initiate_window(self):
        # Constants
        WIDTH = self.width
        HEIGHT = self.height

        # Initialize Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        
        self.wait_for_click()
    
    def show_step(self, index):
        """ Go through all objects and visualize them."""
        for obj in self.sim.objects:
            self.show_object(obj, index)
        
    def show_object(self, obj, index):
        """ Visualize an object """
        color = self.object_color(obj)
        
        state = obj.states.iloc[-1]
        x, y = state.pos_x, state.pos_y
        uv = self.mapper.transform((x, y))
        
        missile_length_pixels = 400
        uv2 = self.mapper.transform((x + missile_length_pixels * np.cos(state.orientation), 
                                     y + missile_length_pixels * np.sin(state.orientation)))

        pygame.draw.line(self.screen, color, uv, uv2, 4)

        if state.fuel > 0:
            pygame.draw.circle(self.screen, (255, 255, 0), uv, 5)
    
    def object_color(self, obj):
        """Determine the visualization color of an object. Target is red, missile is white."""
        if isinstance(obj, Target):
            return "red"
        elif isinstance(obj, Missile):
            return "white"
        else:
            return "gray"  # Default color for unknown objects

    def wait_for_click(self):
        """Wait for a mouse click before starting the simulation."""
        waiting = True
        while waiting:
            self.screen.fill((30, 30, 30))  # Slightly different background color to show it's in waiting mode
            font = pygame.font.Font(None, 36)
            text = font.render("Click anywhere to start simulation", True, (255, 255, 255))
            self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2))
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    # exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting = False
    
    def show_icon(self):
        """Display an icon at the transformed (0,0) coordinate with a fixed scaling factor of 0.1."""
        
        # Scale the image (fixed factor of 0.1)
        image_width, image_height = self.my_image.get_size()
        scaled_size = (int(image_width * 0.2), int(image_height * 0.2))
        scaled_image = pygame.transform.scale(self.my_image, scaled_size)
        
        # Get the new rectangle
        image_rect = scaled_image.get_rect()
    
        # Transform simulation coordinates to window coordinates
        uv = self.mapper.transform((0, 0))
    
        # Adjust the rectangle so that its bottom-left is at the desired coordinate
        image_rect.topleft = (uv[0], uv[1] - image_rect.height)
    
        # Blit the scaled image onto the screen
        self.screen.blit(scaled_image, image_rect)

                
    