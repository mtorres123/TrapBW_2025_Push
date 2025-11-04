import numpy as np
"""
This contains functions useful when considering the trapezoidal geometry stuff
"""

def find_trapezoid_edges(X,Z, h, DX, atol=1e-8):
    '''
    Finds the indices of the verticies of the trapezoidal breakwater.
    '''
    # Find values of the bathymetry that are -h or really close to it.
    tank_bottom_bool = np.isclose(Z, h, atol=atol)
    # Invert boolean to get emergent structure
    idx_above = np.where(~tank_bottom_bool)[0]
    # Take first and last points for the toes of the structure
    i_toe_l,i_toe_r = idx_above[0]-1, idx_above[-1]+1

    # Index out the breakwater part
    Z_stru = -Z[i_toe_l:i_toe_r]
    
    # Find the slopes within the breakwater part
    slope = np.diff(Z_stru) / DX

    # i_top_l: first part where the slop dips to near 0.
    i_top_l = np.argmax(slope < 1/5) + i_toe_l   # first flat-ish
    
    # i_top_r: find where slope is negative, grab first element.
    i_top_r = np.flatnonzero(slope < -1/5)[0] + i_toe_l
    
    
    return [i_toe_l,i_toe_r,i_top_l,i_top_r]