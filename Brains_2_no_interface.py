# Brains_2_no_interface.py

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from odeSolvers import *
import matplotlib.gridspec as gridspec
from MOI import *

g = 9.81

def beam_names(n):
    if n == 1:
        return "Rectangular Beam"
    elif n == 2:
        return "I-Shaped Beam"
    elif n == 3:
        return "T-Shaped Beam"
    elif n == 4:
        return "Circular Solid Beam"

def min_E(l,M,w,load_type):
    if load_type == 1:
        return (l**2 * w /(3*M))/(10**(6))
    elif load_type == 2:
        return (l**2 * w / (8*M))/(10**6)
    
# Beam Shape:
# 1 --> Rectangular Solid
# 2 --> I-Shaped Beam
# 3 --> T-Shaped Beam
# 4 --> Circular Solid Beam
beam_shape = 1

# Support Type:
# 1 --> Single Ended Support DONT CHANGE
# For later projects, more support types could be added.
# This project is solely focused on Cantilevered beams, specifically diving boards.
support_type = 1

# Load Type:
# 1 --> Point Force at the rightmost end
# 2 --> Uniformely distributed load in N/m
load_type = 1

# Weight Value:
# Represents the weight value of your force
weight_value = 60*g

# Length of beam in meters:
# Pretty self-explanatory :)
L = 3

# Board Weight:
# If you'd like the weight of the beam to be considered, write it here.
# Otherwise leave as zero.
board_mass = 0.048*2 #kg

# Specifications of dimensions:
if beam_shape == 1:
    rec_b = 0.5
    rec_h = 0.1
    MOI_f = MOI_rec(rec_b,rec_h)
elif beam_shape == 2: 
    # For I-Shaped Beams, these dimensions are standardized W150x14 Wide Flange Dimensions
    I_b1 = 0.1
    I_b2 = 0.1
    I_t1 = 0.0055
    I_t2 = 0.0055
    I_h = 0.15
    MOI_f = MOI_I(I_b1,I_t1,I_b2,I_t2,I_h)
elif beam_shape == 3:
    # For T-Shaped Beams, these dimensions are standardized W150x14 Wide Flange Dimensions
    T_b1 = 0.1
    T_b2 = 0.1
    T_t1 = 0.0055
    T_t2 = 0.0055
    T_h = 0.15
    MOI_f = MOI_T(T_b1,T_t1,T_b2,T_t2,T_h)
elif beam_shape == 4:
    # R represents the radius
    R = 0.05
    MOI_f = MOI_circle_solid(R)

# Youngs Modulus:
# Leave in the terminal, since it calculates a value for you that'll be handy later.

Npts = 100

board_w = board_mass*g / L # N/m

if load_type == 1:
    E_value = float(input(f"Youngs Modulus represents the ratio of how much weight a material can bear until it bends a unit length. \n Based on your criteria, the minimum Youngs' Modulus you could have before the board breaks is {min_E(L,MOI_f,weight_value,load_type):0,.2f}MPa.\n What Young's Modulus value do you want your diving board to be on the order of Mega Pascals?\n"))
elif load_type == 2:
    E_value = float(input(f"Youngs Modulus represents the ratio of how much weight a material can bear until it bends a unit length. \n Based on your criteria, the minimum Youngs' Modulus you could have before the board breaks is {min_E(L,MOI_f,board_w,load_type):0,.2f}MPa.\n What Young's Modulus value do you want your diving board to be on the order of Mega Pascals?\n"))

beam_E = E_value*(10**6)

weight_function = np.zeros(Npts)
length_function = np.arange(start=0, stop=L, step=L / (Npts))
shear_function = np.zeros(Npts)
dx = length_function[1] - length_function[0]

if load_type == 2:
    for i in range(Npts): # Remember to add g again
        weight_function[i] = -board_w*L

    for i in range(Npts):
        shear_function[i] = -board_w*L * (i/(L*Npts))

    # Calculating the moment function
    moment_function = integral_values_rk4(lambda x: np.interp(x, length_function, shear_function), 0, L,
                                        L / (Npts))

    # Calculating the slope function
    slope_function = (integral_values_rk4(lambda x: np.interp(x, length_function, moment_function), 0, L,
                                        L / (Npts))) / (beam_E * MOI_f)

    # Calculating the deflection function
    def_function = integral_values_rk4(lambda x: np.interp(x, length_function, slope_function), 0, L,
                                        L / (Npts))

    fig = plt.figure(figsize=(12, 18))
    fig.suptitle(f"Analysis of Cantilever Beam with Distributed Load\n Beam Type: {beam_names(beam_shape)}, Youngs Modulus = {E_value}$MPa$, Force/$m^2$ = {board_w:0,.2e}$N/m$, AMOI = {MOI_f:0,.2e} $m^4$, Minimum Allowable E = {min_E(L,MOI_f,board_w,load_type):0,.2f} $MPa$", fontsize=16, fontname='Arial', fontweight='bold')
    gs = gridspec.GridSpec(5, 2, width_ratios=[19, 1], wspace=0.05)

    for i, (data, label) in enumerate(zip([weight_function, shear_function, moment_function, slope_function, def_function],
                                        ['Weight Function', 'Shear Function', 'Moment Function', 'Slope Function', 'Deflection Function'])):
        ax = plt.subplot(gs[i, 0])
        cmap = plt.get_cmap('jet')
        norm = Normalize(vmin=min(moment_function), vmax=0)
        sm = ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])

        for j in range(Npts - 1):
            ax.plot(length_function[j:j + 2], data[j:j + 2], color=cmap(norm(data[j])))  # Change line color with gradient
        ax.set_ylabel(label)

    cbar_ax = plt.subplot(gs[:, 1])
    cbar = plt.colorbar(sm, cax=cbar_ax, orientation='vertical')
    cbar.set_label('Color Gradient')
    ax.set_xlabel('Length (m)')

    plt.tight_layout()
    plt.show()

elif load_type == 1:
    shear_function = np.zeros(Npts)
    length_function = np.arange(start=0, stop=L, step=L / (Npts))
    dx = length_function[1] - length_function[0]

    for i in range(Npts): # Remember to add g again
        shear_function[i] = -weight_value - (i / Npts * board_w)

    # Calculating the shear function
    moment_function = integral_values_rk4(lambda x: np.interp(x, length_function, shear_function), 0, L,
                                        L / (Npts))

    # Calculating the moment function
    slope_function = integral_values_rk4(lambda x: np.interp(x, length_function, moment_function), 0, L,
                                        L / (Npts)) / (beam_E * MOI_f)

    # Calculating the slope function
    def_function = (integral_values_rk4(lambda x: np.interp(x, length_function, slope_function), 0, L,
                                        L / (Npts))) 
    fig = plt.figure(figsize=(12, 18))
    fig.suptitle(f"Analysis of Cantilever Beam with Point Force \n Beam Type: {beam_names(beam_shape)}, Youngs Modulus = {E_value}$MPa$, Point Force = {weight_value:0,.2e}$N$, AMOI = {MOI_f:0,.2e} $m^4$, Minimum Allowable E = {min_E(L,MOI_f,weight_value,load_type):0,.2f} $MPa$", fontsize=16, fontname='Arial', fontweight='bold')
    gs = gridspec.GridSpec(4, 2, width_ratios=[19, 1], wspace=0.05)

    for i, (data, label) in enumerate(zip([shear_function, moment_function, slope_function, def_function],
                                        ['Shear Function', 'Moment Function', 'Slope Function', 'Deflection Function'])):
        ax = plt.subplot(gs[i, 0])
        cmap = plt.get_cmap('jet')
        norm = Normalize(vmin=min(moment_function), vmax=0)
        sm = ScalarMappable(norm=norm, cmap=cmap)
        sm.set_array([])

        for j in range(Npts - 1):
            ax.plot(length_function[j:j + 2], data[j:j + 2], color=cmap(norm(data[j])))  # Change line color with gradient
        ax.set_ylabel(label)

    cbar_ax = plt.subplot(gs[:, 1])
    cbar = plt.colorbar(sm, cax=cbar_ax, orientation='vertical')
    cbar.set_label('Color Gradient')
    ax.set_xlabel('Length (m)')

    plt.tight_layout()
    plt.show()