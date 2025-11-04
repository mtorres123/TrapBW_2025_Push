import numpy as np
from funwave_amp import DomainObject
from ._numbers_helpers import slope_to_degrees
from ._bathymetry_helpers import (get_slope_base,
                                 set_slope,
                                 set_flat)



def set_bathymetry(var_dict):
    '''
    Create the grid, place the structure in the flat tank, remove it if flat 
    option selected, create domain object.
    '''
    ## UNPACK -----------------------------------------------------------------
    # Geometry
    h = var_dict['DEP_WK']
    m_deg = var_dict['m_deg']
    # Crest Position
    z_crest   = var_dict['z_crest']
    # Trapezoid Points
    x_toe_l   = var_dict['x_toe_l']
    x_crest_l = var_dict['x_crest_l']
    x_crest_r = var_dict['x_crest_r']
    x_toe_r   = var_dict['x_toe_r']
    # Hydrodynamics 
    L = var_dict['L']
    # Nondimensional sizing 
    PI_5 = var_dict['PI_5']
    PI_6 = var_dict['PI_6']
    # Flat Option
    FLAT_OR_TRAP = var_dict['FLAT_OR_TRAP']
    Nglob = var_dict['Nglob']
    ## [END] UNPACK -----------------------------------------------------------
    
    
    # Find the rightward edge of the domain- toe + propagation room + sponge
    x_end = x_toe_r + (PI_5+PI_6)*L
    
    ## MAKE THE GRID -------------------------------------------------------
    # Use DX = \lambda/70, rounded
    DX = round(L/70,2)
    # Use arange
    n = int(x_end // DX) + 1
    x = np.arange(0,n) * DX
    # Correct x_end
    x_end = x[-1]
    ## [END] MAKE THE GRID -------------------------------------------------
    
    
    
    ## MAKE BATHYMETRY --------------------------------------------------------
    # Intialize array
    bathy = np.zeros(x.shape)
    
    # Region from left edge to left structure toe: flat
    set_flat(0, x_toe_l, -h, x, bathy)
    
    # Left slope of structure: slope
    set_slope(x_toe_l, x_crest_l, -h, m_deg, x, bathy)
    # Top of structure: flat
    set_flat(x_crest_l, x_crest_r, z_crest, x, bathy)
    # Right slope of structure: slope
    set_slope(x_crest_r, x_toe_r, z_crest, -m_deg, x, bathy)
    
    # Region from right structure toe to right edge: flat
    set_flat(x_toe_r, x_end, -h, x, bathy)
    
    # Invert z elevations created to depths
    bathy = -bathy
    ## [END] MAKE BATHYMETRY --------------------------------------------------
    
    
    ## FLATTEN BATHYMETRY IF SELECTED -----------------------------------------
    if FLAT_OR_TRAP == 'FLAT':
        bathy = h*np.ones_like(bathy)
    elif FLAT_OR_TRAP == 'TRAP':
        bathy = bathy
    else:
        raise ValueError("FLAT_OR_TRAP must be set as `FLAT` or `TRAP`!")
    
    ## [END] MAKE BATHYMETRY --------------------------------------------------
    
    
    ## MAKE DOMAIN OBJECT -----------------------------------------------------
    # Mglob and Nglob for 1D
    Mglob,Nglob = len(bathy),Nglob
    # Use the same DX/DY
    DX,DY = DX,DX
    # Domain object initialization
    DO = DomainObject(Mglob = Mglob, Nglob = Nglob,
                       DX = DX, DY = DY)
    # Add bathymetry
    DO.z_from_1D_array(bathy)
    ## [END] MAKE DOMAIN OBJECT -----------------------------------------------
    
    return {'DOM': DO,
            'Mglob': len(bathy), 'Nglob': Nglob,
            'DX': DX, 'DY': DX,
            'x_end': x_end
            }