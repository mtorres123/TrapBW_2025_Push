import numpy as np


#%% DISPERSION RELATION
'''
Code to solve the dispersion relation using the Newton-Raphson method, a 
root-finding method, given an input period `T`, depth `h`, and initial guess
`k` for the wavenumber
'''

# Linear Dispersion
def f(k,w,h,g):
    '''
    Function to find the roots of- the Airy linear dispersion relation
    '''
    return g*k*np.tanh(k*h) - w**2
 
# Derivative wrt to k
def dfdk(k,w,h,g):
    '''
    Derivative of the dispersion relation, needed for the algorithm
    '''
    return g*(np.tanh(k*h) + h*k*np.cosh(k*h)**-2)
 
# Newton-Raphson Method
def ldis(T,h,k=1,g=9.81):
    '''
    Applies the Netwon-Raphson algorithm for a initial guess of k=1 (default)
    for an error tolerance of 10**-12 with 20 iterations maximum
    '''
    
    ## Convgerence parameters
    errorTolerance = 10**-12
    maxIterations = 20
 
    # Angular frequency
    w = 2*np.pi/T
    
    # Loop through max iterations
    for i in range(maxIterations):
           
        # Calculate correction term and add
        correction = -f(k,w,h,g)/dfdk(k,w,h,g)
        k += correction
       
        # Exit loop if solution is found within specified error tolerance.
        error = correction/k
        if ( abs(error) < errorTolerance):
            break
           
        # Calculate wavelength
        l = 2*np.pi/k
    return l

#%% CELERITY
def wavespeed(T,L):
    '''
    Calculates wave celerity for a given period `T` and wavelength `L`
    '''

    c = L / T
    return c