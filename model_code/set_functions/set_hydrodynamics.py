from ._hydrodynamics_helpers import ldis, wavespeed
import numpy as np

def get_hydrodynamics(var_dict):
    '''
    Convert the unified notation of hydrodynamics to either WK_REG or WK_IRR
    notation and calculate hydrodynamic values based on linear theory
    '''
    ## UNPACK -----------------------------------------------------------------
    T = var_dict['Tperiod']
    h = var_dict['DEP_WK']
    relH = var_dict['relH']
    WK = var_dict['WAVEMAKER']
    FreqMin = var_dict['FreqMin']
    FreqMax = var_dict['FreqMax']
    ## [END] UNPACK -----------------------------------------------------------
    
    
    ## CONVERTED UNIFIED NOTATION ---------------------------------------------
    if WK == 'WK_REG':
        # WK_REG parameters
        AMP_WK = round(relH*h/2,4)
        # Set the WK_IRR parameters to none
        FreqPeak = np.nan
        FreqMin = np.nan
        FreqMax = np.nan
        Hmo = np.nan
    elif WK == 'WK_IRR':
        # WK_IRR parameters
        Hmo = round(relH*h,4)
        FreqPeak = round(1/T,4)
        FreqMin = FreqMin
        FreqMax = FreqMax
        # Set the WK_REG parameters to none
        AMP_WK = np.nan
    else:
        raise ValueError("Wavemaker must be set as `WK_REG` or `WK_IRR`!")
    ## [END] CONVERTED UNIFIED NOTATION ---------------------------------------

    
    
    ## LINEAR HYDRODYNAMICS ---------------------------------------------------
    # Use Levi's ldis for linear dispersion
    L = round(ldis(T, h),4)
    # Calculate k and kh
    k = round(2*np.pi/L,4)
    kh = round(k*h,4)
    # Use Levi's wavespeed for celerity
    c = round(wavespeed(T,L),4)
    ## [END] LINEAR HYDRODYNAMICS ---------------------------------------------
    
    
    # Note: round these to nicer numbers
    return {
            # T-h
            'Tperiod': T,
            'DEP_WK': h,
            # WK_REG
            'AMP_WK': AMP_WK,
            # WK_IRR 
            'Hmo': Hmo,
            'FreqPeak': FreqPeak,
            'FreqMin': FreqMin,
            'FreqMax': FreqMax,
            # Hydrodynamics
            'L': L,
            'k': k,
            'kh': kh,
            'c': c}