
def set_regions(var_dict):
    '''
    Set the positions of the sponges and wavemaker
    '''
    
    ## UNPACK -----------------------------------------------------------------
    # Hydrodynamics
    L = var_dict['L']
    # Nondimensional sizing 
    PI_1 = var_dict['PI_1']     # Sponge west width
    PI_2 = var_dict['PI_2']     # Distance between west sponge and Xc_WK
    PI_6 = var_dict['PI_6']     # East sponge width
    # End of tank
    x_end = var_dict['x_end']
    ## [END] UNPACK -----------------------------------------------------------
    
    # West Sponge
    Sponge_west_width = PI_1*L
    # Internal Wavemaker
    Xc_WK = (PI_1 + PI_2)*L
    # Sponge east width
    Sponge_east_width = PI_6*L 
    # Also useful: x-position of eastern sponge start
    Sponge_east_width_x = x_end - Sponge_east_width
        
    return{'Sponge_west_width': Sponge_west_width,
           'Xc_WK': Xc_WK,
           'Sponge_east_width': Sponge_east_width,
           'Sponge_east_width_x': Sponge_east_width_x}