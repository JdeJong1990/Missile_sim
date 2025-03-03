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
    fig = plt.figure()
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
    ax1.grid('on')
    ax1.legend()

    # Plot velocity magnitude
    ax2.plot(time_data_shortened, velocity_magnitude, label='Velocity')
    ax2.set_xlabel('Time (s)')
    ax2.set_ylabel('Velocity (m/s)')
    ax2.set_title('Missile Speed Over Time')
    ax2.grid('on')
    ax2.legend()

    # Plot position over time
    ax3.plot(time_data, x_data, label='X Position')
    ax3.plot(time_data, y_data, label='Y Position')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Position')
    ax3.legend()
    ax3.set_title('Missile Trajectory Over Time')
    ax3.grid('on')

    # Plot acceleration magnitude
    # ax4.plot(time_data_shortened_2, acceleration_magnitude, label='Acceleration')
    # ax4.set_xlabel('Time (s)')
    # ax4.set_ylabel('Acceleration (m/s²)')
    # ax4.set_title('Missile Acceleration Over Time')
    # ax4.grid('on')
    # ax4.legend()
    
    ax4.plot(time_data, orientation_data)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Orientation (rad)')
    ax4.grid('on')

    plt.show()
    plt.draw()
    plt.pause(0.001)

def plot_all_trajectories(missiles, timestep):
    """Plots the trajectory, velocity, and orientation for multiple missiles."""
    fig = plt.figure(figsize=(12, 8))
    fig.clf()

    ax1 = fig.add_subplot(111)
    # ax1 = fig.add_subplot(221)
    # ax2 = fig.add_subplot(222)
    # ax3 = fig.add_subplot(223)
    # ax4 = fig.add_subplot(224)

    colors = ['b', 'r', 'g', 'm', 'c', 'y', 'k']  # Different colors for different missiles

    for i, missile in enumerate(missiles):
        color = colors[i % len(colors)]  # Cycle through colors
        
        time_data = missile.states["time"].to_numpy()
        x_data = missile.states["pos_x"].to_numpy()
        y_data = missile.states["pos_y"].to_numpy()
        velocity_x = missile.states["vel_x"].to_numpy()
        velocity_y = missile.states["vel_y"].to_numpy()
        orientation_data = missile.states["orientation"].to_numpy()

        # Compute velocity magnitude
        diff_x = np.diff(np.array(x_data, dtype=float))
        diff_y = np.diff(np.array(y_data, dtype=float))
        valid_mask = (x_data[:-1] != 0) | (y_data[:-1] != 0)  # Exclude cases where both are zero
        
        velocity_magnitude = np.where(
            valid_mask, 
            np.sqrt(diff_x**2 + diff_y**2) / timestep, 
            0
            )

        time_data_shortened = time_data[1:]

        # Compute acceleration magnitude
        # acceleration_x = np.diff(velocity_x) / timestep
        # acceleration_y = np.diff(velocity_y) / timestep
        # acceleration_magnitude = np.sqrt(acceleration_x**2 + acceleration_y**2)

        # Plot position
        ax1.plot(x_data, y_data, color=color, label=f'Missile {i+1}')
        ax1.axis('equal')
        ax1.set_xlabel('x (m)')
        ax1.set_ylabel('y (m)')
        ax1.grid('on')

    #     # Plot velocity magnitude
    #     ax2.plot(time_data_shortened, velocity_magnitude, color=color, label=f'Missile {i+1}')
    #     ax2.set_xlabel('Time (s)')
    #     ax2.set_ylabel('Velocity (m/s)')
    #     ax2.set_title('Speed Over Time')
    #     ax2.grid('on')

    #     # Plot position over time
    #     ax3.plot(time_data, x_data, color=color, linestyle='--', label=f'X Missile {i+1}')
    #     ax3.plot(time_data, y_data, color=color, label=f'Y Missile {i+1}')
    #     ax3.set_xlabel('Time (s)')
    #     ax3.set_ylabel('Position (m)')
    #     ax3.grid('on')

    #     # Plot orientation over time
    #     ax4.plot(time_data, orientation_data, color=color, label=f'Missile {i+1}')
    #     ax4.set_xlabel('Time (s)')
    #     ax4.set_ylabel('Orientation (rad)')
    #     ax4.grid('on')

    # # ax1.legend()
    # ax2.legend()
    # ax3.legend()
    # ax4.legend()

    plt.show()
    plt.draw()
    plt.pause(0.001)
