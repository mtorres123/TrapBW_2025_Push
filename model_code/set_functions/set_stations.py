import numpy as np



def set_stations(var_dict):
    
    '''
    Places stations within the domain
    '''
    ## UNPACK -----------------------------------------------------------------
    # Bathymetry
    DO = var_dict['DOM']
    X = DO.X.values
    # Hydrodynamics
    L = var_dict['L']
    # Structure geometry
    x_toe_l = var_dict['x_toe_l']
    x_crest_l = var_dict['x_crest_l']
    x_crest_r = var_dict['x_crest_r']
    x_toe_r = var_dict['x_toe_r']
    ## [END] UNPACK -----------------------------------------------------------


    ## GET INDICES OF TOE/CREST POINTS ----------------------------------------
    i_toe_l =   np.argmin(np.abs(X - x_toe_l))
    i_toe_r =   np.argmin(np.abs(X - x_toe_r))
    i_crest_l = np.argmin(np.abs(X - x_crest_l))
    i_crest_r = np.argmin(np.abs(X - x_crest_r))
    ## [END] GET INDICES OF TOE/CREST POINTS ----------------------------------
    
    
    ## WAVELENGTH GEOMETRY
    pts_per_L = L/(L/70)
    pts_per_m = 1/(L/70)
    
    
    ## REFLECTION STATIONS ----------------------------------------------------
    reflection_pos = [13/9,11/9,10/9,4/9,2/9,1/9]
    reflection_sts = [int(round(i_toe_l-(p*pts_per_L))) for p in reflection_pos]
    ref_string = ['reflection']*len(reflection_sts)
    ## [END] REFLECTION STATIONS ----------------------------------------------
    
    
    
    ## TRANSMISSION STATIONS --------------------------------------------------
    numst = 4
    whichL = 4
    partial = 1/9
    intv = round(pts_per_L+(pts_per_L*partial))
    transmission_pos = round((numst+partial)*pts_per_L)
    leading_sts_per_L = np.arange(i_toe_l-transmission_pos, i_toe_l, intv)
    trailing_sts_per_L = np.arange(i_toe_r, i_toe_r+transmission_pos+intv, intv)
    transmission_sts = [leading_sts_per_L[abs(numst-whichL)], trailing_sts_per_L[abs(numst-whichL)-1]]
    transmission_sts = [int(x) for x in transmission_sts]
    print(transmission_sts)
    trans_string = ['transmission']*len(transmission_sts)
    ## [END] TRANSMISSION STATIONS --------------------------------------------
    
    
    ## RUNUP STATIONS ---------------------------------------------------------
    runup_sts = np.arange(i_toe_l, i_crest_l).astype(int)
    runup_string = ['runup']*len(runup_sts)
    ## [END] RUNUP STATIONS ---------------------------------------------------
    
    
    ## OVERTOPPING STATION ----------------------------------------------------
    overtop_sts = np.atleast_1d(i_crest_r)
    overtop_string = ['overtopping']*len(overtop_sts)
    ## OVERTOPPING STATION ----------------------------------------------------
    
    
    
    # ENTIRE STATION MATRIX
    gages_M = np.concatenate([reflection_sts, transmission_sts, runup_sts, overtop_sts])
    gages_N = np.ones_like(gages_M)
    gages_str = np.concatenate([ref_string, trans_string, runup_string, overtop_string])
    gage_file = np.column_stack([gages_M, gages_N])
    
    DO.add_stations(Mglob_pos=gages_M,
                    Nglob_pos=gages_N)
    DO["station_str"] = ("GAGE_NUM", gages_str)


    return {'reflection_sts': reflection_sts,
        'transmission_sts': transmission_sts,
        'runup_sts': runup_sts,
        'overtop_sts': overtop_sts,
        'gage_file': gage_file,
        'DOM': DO,
        'NumberStations':gage_file.shape[0]}