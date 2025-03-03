# -*- coding: utf-8 -*-
"""
Created on Sat Mar  1 19:35:37 2025

@author: Joost
"""

#%%
import matplotlib.pyplot as plt
import numpy as np

from Missile import Missile
from Target import Target
from Simulator import Simulator
from ms_toolbox01 import plot_missile_data

from ms_toolbox01 import plot_all_trajectories


#%%

# Simulation parameters
timestep = 0.05  # seconds
num_steps = 2000  # total simulation steps

# Create missile object
target = Target()
target.position = (-10000, 10000)


objects = [target]

missile = Missile(guidance = False)
missile.fuel = 0
missile.orientation = 0
missile.position = (0, 10000)
objects.append(missile)

missile_sim = Simulator(objects)

print('Start Sim')
missile_sim.sim(num_steps, timestep)

    

print('Sim done')

#%%

# Simulation parameters
timestep = 0.05  # seconds
num_steps = 2000  # total simulation steps

# Create missile object
target = Target()
target.position = (-10000, 10000)


objects = []
for i in range(10):
    target = Target()
    target.position[1] = 2000 + i*1000
    objects.append(target)

missile = Missile(guidance = False)
missile.fuel = 0
missile.orientation = 0
missile.position = (0, 10000)
objects.append(missile)

missile_sim = Simulator(objects)

print('Start Sim')
missile_sim.sim(num_steps, timestep)

    

print('Sim done')

# plot_all_trajectories(missile_sim.objects, timestep)