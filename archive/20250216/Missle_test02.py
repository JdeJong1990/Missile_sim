
#%%
import matplotlib.pyplot as plt
import numpy as np

from Missile import Missile
from MissileSim import MissileSim
from ms_toolbox01 import plot_missile_data


#%%

# Simulation parameters
timestep = 0.04  # seconds
num_steps = 2000  # total simulation steps

# Create missile object
missile = Missile()

objects = [missile]

missile_sim = MissileSim(objects, timestep)

# Lists to store simulation data
time_data = []
x_data = []
y_data = []

# Run simulation
print('Sim started')
step = 0
missile_sim.objects[0].position[1] = 1

while (missile_sim.objects[0].position[1])>0:
#for step in range(num_steps):
    time = step * timestep
    time_data.append(time)
    x_data.append(missile_sim.objects[0].position[0])
    y_data.append(missile_sim.objects[0].position[1])
    missile_sim.run(timestep)
    step +=1
    

print('Sim done')

#%% Plot results
plot_missile_data(missile, timestep)
plt.show()
