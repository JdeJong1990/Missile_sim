
#%%
import matplotlib.pyplot as plt
import numpy as np

from Missile import Missile
from Target import Target
from MissileSim import MissileSim
from ms_toolbox01 import plot_missile_data


#%%

# Simulation parameters
timestep = 0.1  # seconds
num_steps = 2000  # total simulation steps

# Create missile object
target = Target()
missile = Missile()


objects = [target, missile]

missile_sim = MissileSim(objects, timestep)
missile_sim.sim()
# # Lists to store simulation data
# time_data = []
# x_data = []
# y_data = []

# # Run simulation
# print('Sim started')
# step = 0

# while (missile_sim.objects[1].position[1])>0:
# #for step in range(num_steps):
#     time = step * timestep
#     time_data.append(time)
#     x_data.append(missile_sim.objects[0].position[0])
#     y_data.append(missile_sim.objects[0].position[1])
#     missile_sim.run(timestep)
#     step +=1
    

print('Sim done')

#%% Plot results
plot_missile_data(missile, timestep)
plt.show()
