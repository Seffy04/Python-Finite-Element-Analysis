# MOI.py
# Finds Area Moment of Inertia for I, T, and rectangle beams.

from odeSolvers import *
import numpy as np

def MOI_I(b1,t1,b2,t2,h):
    I_flange = (1/12) * (b1 * t1**3)  # moment of inertia of flange
    I_web = (1/12) * (b2 * t2**3)     # moment of inertia of web
    I_central = (1/6) * b2 * t2 * (h/2)**2  # moment of inertia of central part

    return I_flange + I_web + I_central

def MOI_T(b1,t1,b2,t2,h):
    I_flange = (1/12) * b1 * t1**3  # moment of inertia of flange
    I_central = b1 * t1 * ((h/2) - (t1/2))**2  # moment of inertia of central part
    I_web = (1/12) * b2 * t2**3     # moment of inertia of web

    return I_flange + I_central + I_web
    
def MOI_rec(b,h):
    return (1/12) * b * h**3

def MOI_circle_solid(r):
    def circular_beam_section(y, r):
        if abs(y) <= r:
            return 2 * np.sqrt(r**2 - y**2)
        else:
            return 0
    
    def integrand(y, r):
        return (y**2) * (circular_beam_section(y, r)**2)  # Fixing the integrand
    
    integral_val = integral_values_rk4(lambda y: integrand(y, r), -r, r, 0.001)  # Integrating from -r to r
    return integral_val[-1]

def main():
    r = 10
    area_cal = np.pi * ((r*2)**4) / 64
    area_fun = MOI_circle_solid(r)
    print(f"Area with equation: {area_cal}\nArea with function: {area_fun}")

if __name__ == "__main__":
    main()