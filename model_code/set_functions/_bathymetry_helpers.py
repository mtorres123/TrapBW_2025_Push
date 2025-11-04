import numpy as np

#%% BATHYMETRIC HELPER FUNCTIONS

def get_slope_base(y0, y1, angle):
    '''
    For a given angle of inclination `angle` and vertical positions `y0`, `y1`,
    finds the distance of the adjacent side of the right triangle formed.
    '''
    rads = np.deg2rad(angle)
    m = np.tan(rads)
    dx = (y1-y0)/m
    return dx


def set_flat(x0, x1, y0, x, y):
    '''
    Sets values of `y` on the interval [x0, x1] to some uniform value `y0`.
    All other values of `y` remain unchanged.
    '''
    idx = (x0 <= x) & (x <= x1)
    y[idx] = y0
    
    return


def set_slope(x0, x1, y0, angle, x, y):
    '''
    Sets values of `y` on the interval [x0, x1] to follow a straight line
    starting at (x0, y0) with an incline of `angle` degrees from the horizontal.
    All other values of `y` remain unchanged.
    '''
    idx = (x0 <= x) & (x <= x1)
    rads = np.deg2rad(angle)
    m = np.tan(rads)
    y[idx] = y0 + m*(x[idx]-x0)    
    return 


def get_cross_over(x, x0, x1, y, y0):
    '''
    Gets the closest index of y to y0 in the range x0 and x1
    '''
    try:
        idx = (x0 <= x) & (x <= x1)
        indices = np.arange(0,len(x))
        i = np.argmin(np.abs(y[idx]-y0))
        return indices[idx][i]
    except ValueError:
        print(y)
        
        
#%% MAKE THE BATHYMETRY

