import numpy as np
from funwave_amp import DomainObject
from ._numbers_helpers import slope_to_degrees
from ._bathymetry_helpers import (get_slope_base,
                                 set_slope,
                                 set_flat)



def find_discrete_trap_points(var_dict):
    '''
    Create the grid, place the structure in the flat tank, remove it if flat 
    option selected, create domain object.
    '''
    ## UNPACK -----------------------------------------------------------------
    # Geometry
    DOM = var_dict['DOM']
    X = DOM.X.values
    # Trapezoid Points
    x_toe_l   = var_dict['x_toe_l']
    x_crest_l = var_dict['x_crest_l']
    x_crest_r = var_dict['x_crest_r']
    x_toe_r   = var_dict['x_toe_r']
    ## [END] UNPACK -----------------------------------------------------------
    
    
    # Find the indices of where the trapezoid points lie close to the grid
    i_toe_l   = int(np.argmin(np.abs(X-x_toe_l)))
    i_crest_l = int(np.argmin(np.abs(X-x_crest_l)))
    i_crest_r = int(np.argmin(np.abs(X-x_crest_r)))
    i_toe_r   = int(np.argmin(np.abs(X-x_toe_r)))
    
    # Find the actual x values too (F for FUNWAVE :D)
    xF_toe_l, xF_toe_r = X[i_toe_l], X[i_toe_r]
    xF_crest_l, xF_crest_r = X[i_crest_l], X[i_crest_r]
    
    
    return {'i_toe_l':   i_toe_l,   'xF_toe_l': xF_toe_l,
            'i_crest_l': i_crest_l, 'xF_crest_l': xF_crest_l, 
            'i_crest_r': i_crest_r, 'xF_crest_r': xF_crest_r, 
            'i_toe_r':   i_toe_r,   'xF_toe_r': xF_toe_r,
            }