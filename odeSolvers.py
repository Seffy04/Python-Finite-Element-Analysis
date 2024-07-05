# odeSolvers.py
# Defines functions to solve ODEs via the Euler and RK4 methods

import numpy as np

def df_Euler(f,t,dt,dfdt_func):
    '''Calculates the step Delta f that should be added to f_{i-1} to 
    calculate f_i using Euler's method. The inputs are defined as below:
    
    f = f_{i-1}
    t = t_{i-1}
    dt = t_i-t_{i-1}

    dfdt_func = a function to calculate df/dt using f and t as inputs.
    '''
    
    # Calculate the derivative at point (f_{i-1}, t_{i-1})
    # and multiply by dt to get the change in f
    df = dfdt_func(f,t) * dt
    
    # Return df
    return df

def df_RK4(f,t,dt,dfdt_func):
    '''Calculates the step Delta f that should be added to f_{i-1} to 
    calculate f_i using a 4th-order Runge-Kutta method. The inputs are 
    defined as below:
    
    f = f_{i-1}
    t = t_{i-1}
    dt = t_i-t_{i-1}

    dfdt_func = a function to calculate the derivative df/dt using f and 
    t as inputs.
    '''
    # Calculate k1-k4 using dfdt_func, f, t, and dt (YOUR CODE BELOW)
    k1 = dfdt_func(f,t)*dt
    k2 = dfdt_func(f+ 0.5*k1,t+dt*0.5)*dt
    k3 = dfdt_func(f+ 0.5*k2,t+dt*0.5)*dt
    k4 = dfdt_func(f+ k3,t+dt)*dt
    # define df based on k1-k4 (YOUR CODE BELOW)
    df_rk4 = (1/6) * (k1 + 2*k2 + 2*k3 + k4)
    # Return df (YOUR CODE BELOW)
    return df_rk4

def midpoint_riemann_sum(values, delta_x):
    """
    Calculates the partial sums of the integral of a function numerically using the midpoint Riemann sum formula.

    :param values: Array of function values.
    :param delta_x: The width of each subinterval.
    :return: List of partial sums representing the integral of the function.
    """
    partial_sums = []
    n = len(values)
    
    # Check if the length of values is divisible by 2
    if n % 2 != 0:
        raise ValueError("Length of values must be even.")
    
    # Calculate the partial sums using the midpoint Riemann sum formula
    cumulative_sum = 0.0
    for i in range(0, n, 2):
        cumulative_sum += values[i] * delta_x
        partial_sums.append(cumulative_sum)
    
    return partial_sums

def integral_values_rk4(function, x0, xn, delta_x):
    num_steps = int((xn - x0) / delta_x)
    integral_values = np.zeros(num_steps)
    x = x0
    integral_sum = 0.0

    for index in range(num_steps):
        k1 = delta_x * function(x)
        k2 = delta_x * function(x + 0.5 * delta_x)
        k3 = delta_x * function(x + 0.5 * delta_x)
        k4 = delta_x * function(x + delta_x)
        
        integral_sum += (k1 + 2 * k2 + 2 * k3 + k4) / 6.0
        integral_values[index] = integral_sum
        
        x += delta_x
    
    return integral_values
