# -*- coding: utf-8 -*-
"""
Created on Sat Feb 15 15:05:40 2025

@author: Joost

Some tools to work with the missile sim
"""

import matplotlib.pyplot as plt
import numpy as np

def plot_missile_data(missile, timestep):
    """Plots the missile trajectory, velocity, and acceleration using its logged states."""
    fig = plt.figure(1)
    fig.clf()

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    # Extract data from the missile's states DataFrame
    time_data = missile.states["time"].to_numpy()
    x_data = missile.states["pos_x"].to_numpy()
    y_data = missile.states["pos_y"].to_numpy()
    velocity_x = missile.states["vel_x"].to_numpy()
    velocity_y = missile.states["vel_y"].to_numpy()
    orientation_data = missile.states["orientation"].to_numpy()

    # Compute velocity magnitude
    velocity_magnitude = np.sqrt(np.diff(x_data)**2 + np.diff(y_data)**2) / timestep
    time_data_shortened = time_data[1:]

    # Compute acceleration magnitude
    acceleration_x = np.diff(velocity_x) / timestep
    acceleration_y = np.diff(velocity_y) / timestep
    acceleration_magnitude = np.sqrt(acceleration_x**2 + acceleration_y**2)
    time_data_shortened_2 = time_data_shortened[:]
    # time_data_shortened_2 = time_data[2:]  

    # Plot position
    ax1.plot(x_data, y_data, label='Position')
    ax1.axis('equal')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.grid()
    ax1.legend()

    # Plot velocity magnitude
    ax2.plot(time_data_shortened, velocity_magnitude, label='Velocity')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.set_title('Missile Speed Over Time')
    ax2.grid()
    ax2.legend()

    # Plot position over time
    ax3.plot(time_data, x_data, label='X Position')
    ax3.plot(time_data, y_data, label='Y Position')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Position')
    ax3.legend()
    ax3.set_title('Missile Trajectory Over Time')
    ax3.grid()

    # Plot acceleration magnitude
    # ax4.plot(time_data_shortened_2, acceleration_magnitude, label='Acceleration')
    # ax4.set_xlabel('Time (s)')
    # ax4.set_ylabel('Acceleration (m/s²)')
    # ax4.set_title('Missile Acceleration Over Time')
    # ax4.grid()
    # ax4.legend()
    
    ax4.plot(time_data, orientation_data)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Orientation (rad)')
    ax4.grid()

    plt.show()
    plt.draw()
    plt.pause(0.001)


