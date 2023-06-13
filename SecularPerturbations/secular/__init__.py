import numpy as np
from scipy.integrate import quad

def blap(a, s, j):
    #Integrand in b_s^j definition
    func = lambda x: np.cos(j*x)/(1-2*a*np.cos(x)+a**2)**s
    
    return (1/np.pi)*quad(func, 0, 2*np.pi)[0]

def blap_dot(a, s, j):
    #Recursive first derivative
    dot = blap(a, s+1, j-1) - 2*a*blap(a, s+1, j) + blap(a, s+1, j+1) 
    
    return s*dot

def blap_ddot(a, s, j):
    #Recursive second derivative
    ddot = blap_dot(a, s+1, j-1) - 2*a*blap_dot(a, s+1, j) + blap_dot(a, s+1, j+1) - 2*blap(a, s+1, j)
    
    return s*ddot
