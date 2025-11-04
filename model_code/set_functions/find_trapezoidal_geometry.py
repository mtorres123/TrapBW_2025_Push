from ._numbers_helpers import slope_to_degrees
from ._bathymetry_helpers import get_slope_base



def find_trapezoid_geometry(var_dict):
    '''
    Set the bathymetry for the structure problem
    '''
    ## UNPACK -----------------------------------------------------------------
    # Slopes of the trapezoidal breakwater
    m = var_dict["m_slope"]
    # Relative wave height and freeboard
    relH = var_dict['relH']
    relF = var_dict['relF']
    # Tank depth
    h = var_dict['DEP_WK']
    # Hydrodynamics
    L = var_dict['L']
    # Nondimensional sizing 
    PI_1 = var_dict['PI_1']
    PI_2 = var_dict['PI_2']
    PI_3 = var_dict['PI_3']
    PI_4 = var_dict['PI_4']
    ## [END] UNPACK -----------------------------------------------------------
    
    
    # z-position of the structure crest
    z_crest = h* relH* relF
    # Angle in degrees of the sloping portions
    m_deg = slope_to_degrees(m)


    ## FIND x-POSITIONS OF TRAPEZOID VERTICES ---------------------------------
    # Left structure toe point
    x_toe_l = (PI_1 + PI_2 + PI_3)*L
    # Left structure crest point
    x_crest_l = x_toe_l + get_slope_base(-h, z_crest, m_deg)
    
    # Right structure crest point
    x_crest_r = x_crest_l + PI_4*L
    # Right structure toe point
    x_toe_r = x_crest_r + get_slope_base(z_crest, -h, -m_deg)
    ## FIND x-POSITIONS OF TRAPEZOID VERTICES ---------------------------------
    

    
    
    return {
            # Top z-position
            'z_crest': z_crest,
            # Left side
            'x_toe_l': x_toe_l,
            'x_crest_l': x_crest_l,
            # Right side
            'x_crest_r': x_crest_r,
            'x_toe_r': x_toe_r,
            # Slope in degrees
            'm_deg': m_deg
            }