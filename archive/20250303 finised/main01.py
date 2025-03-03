# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 16:32:42 2025

@author: Joost
"""


from Missile import Missile
from Target import Target
from Simulator import Simulator
from SimPlayer import SimPlayer

#%%

# Simulation parameters
timestep = 0.05  # seconds
num_steps = 2000  # total simulation steps

# Create missile objects
target = Target()
objects = [target]
for i in range(10):
    objects.append(Missile(i*4))

missile_sim = Simulator(objects)

sim_player = SimPlayer(missile_sim)
sim_player.live_sim(num_steps)
    