import numpy as np



def set_total_time(var_dict):
    ## UNPACK -----------------------------------------------------------------
    L = var_dict['L']
    c = var_dict['c']
    ## [END] UNPACK -----------------------------------------------------------


    # Round wavelength
    bl = round(L)
    # Compute time total
    TIME_TOTAL = float(round((150*bl)/c)) + 0.9
    
    
    return {'TOTAL_TIME': TIME_TOTAL}