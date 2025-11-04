
import numpy as np
from ._bathymetry_helpers import get_cross_over
def set_friction(var_dict):
    # Unpack Variables-------------------------------------------------
    # Friction
    Cd = var_dict['CDBWAC']
    # Nondimensional Parameters
    x_toe_l = var_dict['x_toe_l']
    x_toe_r = var_dict['x_toe_r']
    x_top_l = var_dict['x_top_l']
    x_top_r = var_dict['x_top_r']
    h = var_dict['TANK_DEPTH']
    # Domain
    DOM = var_dict['DO']
    #-----------------------------------------------------------------

    
    X = DOM['X'].values
    Z = -DOM['Z'].values[:,1]
    
    cd_array = np.zeros(X.shape)
    iC2 = get_cross_over(X, x_top_r, x_toe_r,Z,-h)+1
    iC1 = get_cross_over(X, x_toe_l, x_top_l, Z, -h)#-1
    cd_array[iC1:iC2] = Cd

    
    
    DOM.friction_from_1D_array(cd_array)
    
    return {'iC2': iC2,
            'iC1': iC1}