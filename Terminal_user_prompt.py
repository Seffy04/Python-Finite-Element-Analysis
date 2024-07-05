# Terminal_user_prompt.py

from MOI import *

def min_E(l,M,w,load_type):
    if load_type == 1:
        return (l**2 * w /(3*M))/(10**(6))
    elif load_type == 2:
        return (l**3 * w / (8*M))/(10**6)

print("Welcome to the structural analysis deflection calculator for divers! \n This interface will prompt you with some choices on the type of beam you'd like to analyze, then will present you with its results based on the numbers you provide it. It's worth mentioning there will be another interface based on the choices you've made here. \n Press any button to continue to choices...")
input()
beam_shape = int(input("Let's start with what shape beam you have for me: \n 1. Rectangular Solid Beam \n 2. I-Shaped Beam \n 3. T-Shaped Beam.\n 4. Circular Solid Beam \n"))
load_type = int(input("What load type would you like?\n 1. Point Load \n 2. Uniformely distributed Load"))
support_type = int(input("What support type would you like to have? \n 1. Single-ended support"))
weight_value = float(input("Assuming the diver is standing all the way at the end of the board, how much does the diver weight in kg?\n *Typical Divers weight between 50kg - 90kg.*\n"))*9.81
L = float(input("Finally, what's the length of your beam? *Typical Diving boards are betweeen 1m and 3m* \n"))
board_weight = float(input("Last question I promise, what's the weight of the beam? \n"))

if beam_shape == 1:
    rec_b = float(input("What's the Rectangle's Base length in meters? "))
    rec_h = float(input("What's the Rectangle's Height in meters? "))
    MOI = MOI_rec(rec_b,rec_h)
elif beam_shape == 2:
    I_b1 = float(input("What's the bottom flange's Base's length in meters? "))
    I_b2 = float(input("What's the top flange's Base's length in meters? "))
    I_t1 = float(input("What's the thicnkess of the flange in meters? "))
    I_t2 = float(input("What's the thicnkess of the web in meters? "))
    I_h = float(input("Finally, what's the height of the beam? "))
    MOI = MOI_I(I_b1,I_t1,I_b2,I_t2,I_h)
elif beam_shape == 3:
    T_b1 = float(input("What's the flange's Base's length in meters? "))
    T_b2 = float(input("What's the web's Base's length in meters? "))
    T_t1 = float(input("What's the thicnkess of the flange in meters? "))
    T_t2 = float(input("What's the thicnkess of the web in meters? "))
    T_h = float(input("Finally, what's the height of the beam? "))
    MOI = MOI_T(T_b1,T_t1,T_b2,T_t2,T_h)
elif beam_shape == 4:
    R = float(input("What's the radius of the beam?"))
    MOI = MOI_circle_solid(R)

E_value = float(input(f"Youngs' Modulus represents the ratio of how much weight a material can bear until it bends a unit length. \n Based on your criteria, the minimum Youngs' Modulus you could have before the board breaks is {min_E(L,MOI,weight_value,support_type)}MPa.\n What Young's Modulus value do you want your diving board to be on the order of Mega Pascals?\n"))