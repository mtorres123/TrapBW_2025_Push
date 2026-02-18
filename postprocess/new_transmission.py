import numpy as np
import xarray as xr
import pandas as pd
from plotmaster import compute_PSD
from plotmaster import calculateHsig
from wavestructmaster import computeKt
import os

def calculate_transmission(ds,dss):
    ## GET CORRECT TRANSMISSION STATIONS --------------------------------------
    '''
    This is the fix to ensure the stations are at least exactly what we want.
    Upon setting the stations I used "station_str" to designate what each 
    station is for. So here, we explicitly only look at the station strings
    labeled "transmission". This should correspond to 2 gages and this is 
    asserted.
    
    The "incident" location is taken as the location with the smaller Mglob
    value and the "reflected" location is taken as the location with the 
    higher Mglob value. From there, we can cleanly select the correct stations.
    '''
    
    # Query the transmission stations, get Mglob of both
    ds_transmission = ds.where(ds["station_str"] == "transmission", drop=True)
    Mglob_gage = ds_transmission.Mglob_gage.values
    
    # Ensure two stations, get m value of both
    assert len(Mglob_gage) == 2
    M_in, M_tr = int(np.min(Mglob_gage)), int(np.max(Mglob_gage))
    
    # Get the incident wave 
    ds_inci = dss.where(dss["Mglob_gage"] == M_in, drop=True)
    eta_inc = ds_inci.eta_sta.values.ravel()
    
    # Get the transmitted wave
    ds_trans = dss.where(dss["Mglob_gage"] == M_tr, drop=True)
    eta_trans = ds_trans.eta_sta.values.ravel()
    
    # Debugging print for position of them
    X = ds.X.values
    i_l, i_r = int(dss.i_toe_l), int(dss.i_toe_r)
    print(f'm INC: {M_in}, m LEFT toe {i_l}, m RIGHT toe {i_r}, m TRAN: {M_tr}')
    print(f'x INC: {X[M_in]:.1f}, x LEFT toe {X[i_l]:.1f}, x RIGHT toe {X[i_r]:.1f}, x TRAN: {X[M_tr]:.1f}')
    ## [END] GET CORRECT TRANSMISSION STATIONS --------------------------------
    
    
    
    ## RUN THE TRANSMISSION ANALYSIS ------------------------------------------
    '''
    Now, we call Marissa's transmission functions from `plotmaster` and 
    `wavestructmaster` to output the actual transmission coefficients
    '''
    
    
    time = dss.t_station.values
    dt = dss.PLOT_INTV_STATION 
    
    # PSDs
    f1, S1 = compute_PSD(time, eta_inc)
    f2, S2 = compute_PSD(time, eta_trans)
    
    # Spectral stats
    Hmo1, Hrms1, E1 = calculateHsig(f1, S1)
    Hmo2, Hrms2, E2 = calculateHsig(f2, S2)
    
    
    # Transmission coefficient
    Kt = computeKt([E1, E2])
    
    # Package into nice dictionary
    trans_results = {
        "Hmo1_trans": Hmo1,
        "Hrms1_trans": Hrms1,
        "E1_trans": E1,
        "Hmo2_trans": Hmo2,
        "Hrms2_trans": Hrms2,
        "E2_trans": E2,
        "Kt": Kt
    }
    ## [END] RUN THE TRANSMISSION ANALYSIS ------------------------------------
    return trans_results

#%% MAIN
main_ds = [
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_00001.nc', 
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_18880.nc' 
        ]
sta_ds = [
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_sta_00001.nc', 
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_sta_18880.nc' 
        ]

# Loop through all files
trans_dicts = []
for _ds, _dss in zip(main_ds,sta_ds):
    # Open the datasets
    ds = xr.open_dataset(_ds)
    dss = xr.open_dataset(_dss)
    # Calculate coefficients
    trans_results = calculate_transmission(ds,dss)
    # Merge in with other attributes
    _trans_dict = {**ds.attrs, **trans_results}
    trans_dicts.append(_trans_dict)

# [EDIT] Specify path to where the spreadsheets should output
dir_out = r"."
# [EDIT] Specify what to call the output
output_name = 'New_Transmission_Stats'
# Make output folder
os.makedirs(dir_out,exist_ok=True)

# Merge into dataframe
df_results = pd.DataFrame(trans_dicts)
print('\nLoop Complete! Saving outputs...')
df_results.to_csv(os.path.join(dir_out,f'{output_name}.csv'), index=False)
print(f"\tCSV saved out to {os.path.join(dir_out,f'{output_name}.csv')}")
df_results.to_excel(os.path.join(dir_out,f'{output_name}.xlsx'), index=False)
print(f"\tXLSX saved out to {os.path.join(dir_out,f'{output_name}.xlsx')}")
df_results.to_parquet(os.path.join(dir_out,f'{output_name}.parquet'), index=False)
print(f"\tParquet saved out to {os.path.join(dir_out,f'{output_name}.parquet')}")

print("Post-processing successful!")