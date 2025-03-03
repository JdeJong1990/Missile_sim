
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


objects = [target]
for i in range(1):
    objects.append(Missile(i*2))

missile_sim = Simulator(objects)

print('Start Sim')
missile_sim.sim(num_steps, timestep)

    

print('Sim done')

for obj in missile_sim.objects:
    try:
        print(f'Shortest proximity: {obj.proximity}')
    except: 
        pass
