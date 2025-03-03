
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


objects = [Target()]
for i in range(10):
    objects.append(Missile(i*2))

missile_sim = Simulator(objects)

print('Start Sim')
missile_sim.sim(num_steps, timestep)

    

print('Sim done')

# plot_all_trajectories(missile_sim.objects, timestep)