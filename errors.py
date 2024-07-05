# errors.py
# This is a disaster, but oh well :)

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib.cm import ScalarMappable
from odeSolvers import *
import matplotlib.gridspec as gridspec
from MOI import *
from Brains_2_no_interface import weight_value,length_function,beam_E,MOI_f,L,def_function,E_value,min_E,board_w,load_type
from scipy.optimize import curve_fit

def nu_real(P,x,E,I,L):
    return (-P*x**2*(3*L-x))/(6*E*I)

nu_real_diving = nu_real(weight_value,length_function,beam_E,MOI_f,L)
residuals = nu_real_diving - def_function

def powerlaw_func(x,A,alpha):
    y = A*(x**alpha)
    return y

popt,pcov = curve_fit(powerlaw_func,length_function,def_function)
AA_best,alpha_best = popt
print(AA_best,alpha_best)
y_model_power = powerlaw_func(length_function,AA_best,alpha_best)

plt.rcParams['figure.figsize'] = (20.0, 10.0)

plt.scatter(length_function,residuals,color='green',marker='p',label='Residuals') # plot the mass on the x axis and luminosity on the y axis
plt.plot(length_function,def_function,label='Computed Deflection')
plt.plot(length_function,nu_real_diving,label='Real Values of Deflection')
# plt.axhline(0,ls='--',color='brown')

plt.xlabel("Length in meters",size=20)
plt.ylabel("Deflection in meters",size=20)
plt.xticks(size=18)
plt.yticks(size=18)
plt.legend(fontsize=16)
plt.suptitle(f"Residuals plot of a cantilevered 50MPa beam using my program vs the standard maximum deflection from Appendix D. \n Youngs Modulus = {E_value}$MPa$, Force/$m^2$ = {board_w:0,.2e}$N/m$, AMOI = {MOI_f:0,.2e} $m^4$, Minimum Allowable E = 42.38 $MPa$", fontsize=20, fontname='Arial', fontweight='bold')

plt.show()
