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
    angles_of_attack = []
    for i in range(len(velocity_x)):
        rotated_velocity = rotate_vector([[velocity_x[i], velocity_y[i]]], orientation_data[i])
        angle_of_attack = -np.arctan2(rotated_velocity[1], rotated_velocity[0])
        angles_of_attack.append(angle_of_attack)


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
    
    # ax4.plot(time_data, orientation_data)
    # ax4.set_xlabel('Time (s)')
    # ax4.set_ylabel('Orientation (rad)')
    # ax4.grid('on')
    ax4. plot(time_data, angles_of_attack)
    ax4.set_xlabel('Time (s)')
    ax4.set_ylabel('Angle of attack (rad)')
    ax4.grid('on')

    plt.show()
    plt.draw()
    plt.pause(0.001)

def plot_all_trajectories2(missiles, timestep):
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
        # time_indices = np.where(time_data % 1 < timestep / 2)[0]  # Select indices close to whole seconds
        time_indices = np.where(abs(time_data - np.round(time_data, 0)) < 0.0502/2)
        
        ax1.scatter(x_data[time_indices], y_data[time_indices], color=color, edgecolors='black', zorder=3, label=f'Missile {i+1} (1s markers)')
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

# def draw_vector(ax, base, tip, color):
    
def draw_vector(ax, base, vector, color, scale_factor=1):
    # Normalize the vector to maintain consistent direction and scale
    norm_vector = vector / np.linalg.norm(vector)  # Normalize the vector
    scaled_vector = scale_factor * norm_vector  # Scale it by the desired factor

    # Annotate with the corrected arrow properties
    ax.annotate(
        "",  # No text, just an arrow
        xy=base + scaled_vector,  # Arrow tip (base + scaled vector)
        xytext=base,  # Base position
        arrowprops=dict(
            arrowstyle="->",  # Basic arrow style
            mutation_scale=15,  # Controls the size of the arrow
            color=color,  # Arrow color
            linewidth=2,
        ),
    )


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

        # Plot position
        ax1.plot(x_data, y_data, color=color, label=f'Missile {i+1}')
        # time_indices = np.where(time_data % 1 < timestep / 2)[0]  # Select indices close to whole seconds
        time_indices = np.where(abs(time_data - np.round(time_data, 0)) < timestep/2)
        
        ax1.scatter(x_data[time_indices], y_data[time_indices], color=color, edgecolors='black', zorder=3)
    
    time_data = missiles[1].states["time"].to_numpy()
    time_indices = np.where(abs(time_data - np.round(time_data, 0)) < timestep/2)
    
    for i in time_indices[0]:
        state = missiles[1].states.iloc[i]
        position = (state.pos_x, state.pos_y)
        velocity = (state.vel_x, state.vel_y)
        
        orientation = state.orientation
        orientation_vector = 100 * np.array([np.cos(orientation), np.sin(orientation)])
        draw_vector(ax1, position, orientation_vector, 'black', scale_factor=100)
        draw_vector(ax1, position, velocity, 'red', scale_factor=100)
        # print(f'drawing vector {i}')
    
    ax1.axis('equal')
    ax1.set_xlabel('x (m)')
    ax1.set_ylabel('y (m)')
    ax1.grid('on')
        
        

    ax1.legend()


    plt.show()
    plt.draw()
    plt.pause(0.001)

# def rotate_vector(vector, angle):
#     """
#     Rotates a 2D vector counter clockwise by the given angle (in radians).
#     Preserves the input shape (row or column vector).
#     """
#     rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
#                                 [np.sin(angle),  np.cos(angle)]])
    
#     # Ensure it's a column vector for multiplication
#     is_row_vector = vector.shape == (1, 2)  # Check if it's a row vector
#     vector = np.atleast_2d(vector).T if vector.shape == (2,) else vector

#     rotated_vector = rotation_matrix @ vector  # Matrix multiplication

#     # Convert back to original shape
#     if is_row_vector:
#         return rotated_vector.T  # Convert back to row vector
#     return rotated_vector

# def rotate_vector(vector, angle):
#     """
#     Rotates a 2D vector counterclockwise by the given angle (in radians).
#     Preserves the input shape (row or column vector).
#     """
#     rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
#                                 [np.sin(angle),  np.cos(angle)]])
    
#     vector = np.asarray(vector)  # Ensure it's a NumPy array
#     is_row_vector = vector.shape == (2,)  # Check if it's a row vector

#     rotated_vector = rotation_matrix @ vector.reshape(2, 1)  # Matrix multiplication

#     return rotated_vector.flatten() if is_row_vector else rotated_vector  # Preserve original shape


def rotate_vector(vector, angle):
    """
    Rotates a 2D vector counterclockwise by the given angle (in radians).
    Assumes input is of the form [x, y] and returns [x', y'].
    """
    rotation_matrix = np.array([[np.cos(angle), -np.sin(angle)],
                                [np.sin(angle),  np.cos(angle)]])
    
    vector = np.array(vector).reshape(2, 1)  # Convert to column vector
    rotated_vector = rotation_matrix @ vector  # Matrix multiplication

    return rotated_vector.flatten()  # Convert back to row vector
