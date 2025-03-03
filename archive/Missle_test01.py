
#%%
import matplotlib.pyplot as plt
import numpy as np

from Missile import Missile


#%%

# Simulation parameters
timestep = 0.02  # seconds
num_steps = 2000  # total simulation steps

# Create missile object
missile = Missile()

# Lists to store simulation data
time_data = []
x_data = []
y_data = []

# Run simulation
print('Sim started')
for step in range(num_steps):
    time = step * timestep
    time_data.append(time)
    x_data.append(missile.position[0])
    y_data.append(missile.position[1])
    missile.run(timestep)
print('Sim done')

#%% Plot results
fig = plt.figure(1)
fig.clf()

ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax1.cla()
ax2.cla()

ax1.plot(x_data, y_data, label='Position')
ax1.axis('equal')
ax1.set_xlabel('x (m)')
ax1.set_ylabel('y (m)')
ax1.grid('on')

velocity_data_x = np.diff(x_data) / timestep
velocity_data_y = np.diff(y_data) / timestep
velocity_magnitude = np.sqrt(velocity_data_x**2 + velocity_data_y**2)
time_data_shortened = time_data[1:]

ax2.plot(time_data_shortened, velocity_magnitude, 'o', label='Velocity')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Velocity (m/s)')
ax2.set_title('Missile Speed Over Time')
ax2.grid()
ax2.legend()

ax3.plot(time_data, x_data, label='X Position')
ax3.plot(time_data, y_data, label='Y Position')
# plt.plot(x_data, y_data)
# plt.axis('equal')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Position')
ax3.legend()
ax3.set_title('Missile Trajectory Over Time')
ax3.grid()

acceleration_data_x = np.diff(velocity_data_x) / timestep
acceleration_data_y = np.diff(velocity_data_y) / timestep
acceleration_magnitude = np.sqrt(acceleration_data_x**2 + acceleration_data_y**2)
time_data_shortened_2 = time_data_shortened[1:]

ax4 = fig.add_subplot(224)
ax4.plot(time_data_shortened_2, acceleration_magnitude, '-o', label='Acceleration')
ax4.set_xlabel('Time (s)')
ax4.set_ylabel('Acceleration (m/s²)')
ax4.set_title('Missile Acceleration Over Time')
ax4.grid()
ax4.legend()


plt.show()

#%% Plot results
plt.figure(figsize=(10, 5))
plt.plot(x_data, y_data, label='Position')
# plt.plot(x_data, y_data)
plt.axis('equal')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.legend()
plt.title('Missile Trajectory Over Time')
plt.grid()
plt.show()
# %%
