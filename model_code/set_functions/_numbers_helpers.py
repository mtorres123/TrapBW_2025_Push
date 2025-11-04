import numpy as np
'''
Helper functions to deal with basic rounding/slope arithmetic
'''


def round_sig_figs(x, p):
    '''
    Rounds `x` to `p` significant figures. For example:
        - (x=1234.56, p=4) -> 1235.
    '''
    
    # Ensure that number is not NaN/inf
    if np.all(np.isfinite(x)):
        # Temporarily ignore errors
        eset = np.seterr(all='ignore')
        
        # Use log10 to figure out the order of magnitude
        mags = 10.0**np.floor(np.log10(np.abs(x)))  # omag's
        # Round to number of significant figures
        x = np.around(x/mags,p-1)*mags    
        # Return to default error handling         
        np.seterr(**eset)
        
        # Replace any NaNs with 0s
        x = np.where(np.isnan(x), 0.0, x)
    return x


def slope_to_degrees(m):
    '''
    NOTE: this only strictly works in the small angle limit, but for 
    consistency let's keep this.
    
    Finds the angle in degrees from the horizontal for a 1 on `m` slope.
    '''
    return np.rad2deg(1/m)