
import numpy as np
from ._bathymetry_helpers import get_cross_over
def set_CDBWAC(var_dict):
    '''
    Convert the unified notation of hydrodynamics to either WK_REG or WK_IRR
    notation and calculate hydrodynamic values based on linear theory
    '''
    # Unpack Variables-------------------------------------------------
    # CDBWAC Settings
    USE_CDBWAC = var_dict['USE_CDBWAC']
    CDBWAC = var_dict['CDBWAC']
    # Nondimensional Parameters
    i_toe_l = var_dict['i_toe_l']
    i_toe_r = var_dict['i_toe_r']
    # Domain
    DOM = var_dict['DOM']
    X = DOM['X'].values
    DX = var_dict['DX']
    #-----------------------------------------------------------------

    # Initialize array for either CD or BWAC
    array = np.zeros_like(X)
    
    # CD Case
    if USE_CDBWAC == 'CD':
        # Place CD values specified between left and right toe
        array[i_toe_l:i_toe_r] = CDBWAC
        # Construct Friction File
        DOM.friction_from_1D_array(array)
        # Specify BreakWaterAbsorbCoef
        BreakWaterAbsorbCoef = None
        
    # BWAC Case
    elif USE_CDBWAC == 'BWAC':
        # Place DX value into Breakwater File between left and right toe
        array[i_toe_l:i_toe_r] = DX
        # Construct Breakwater file
        DOM.BWAC_from_1D_array(array)
        # Specify BreakWaterAbsorbCoef
        BreakWaterAbsorbCoef = CDBWAC

    
    
    
    
    return {'DOM': DOM,
            'BreakWaterAbsorbCoef': BreakWaterAbsorbCoef}