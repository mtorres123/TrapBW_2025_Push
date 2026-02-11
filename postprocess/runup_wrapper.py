import numpy as np
import xarray as xr
import pandas as pd
#%% FUNCTION DEFINITION
import runup
def trap_bw_post_runup(dss,ds):
    '''
    This is a wrapper function to use Mike's post-processing code for runup on
    station outputs of Ryan's file workflow. To work, it needs access to both
    the bulk file (ds) and the station file (dss). Because of this it's 
    important to use the `xr.open_dataset() command compared to the 
    `xr.load_dataset()` since we don't want the giant file in memory!
    '''
    # UNPACK ------------------------------------------------------------------
    # From the station files
    t = dss.t_station.values
    sta_idxs = dss.Mglob_gage.values
    runup_data = dss.eta_sta.values
    Z = dss.Z.values[:,0]
    DX = dss.DX
    # From main file
    station_str = ds.station_str.values
    # Flat or Trap?
    flat_or_trap = ds.FLAT_OR_TRAP
    # [END] UNPACK ------------------------------------------------------------
    
    # Only do trapezoidal
    if flat_or_trap == 'TRAP':
        # Get the (x,h(x)) values at each station
        x = sta_idxs*DX
        h = Z[sta_idxs]
        
        # Index out just the runup strings
        x =                 x[station_str=='runup']
        h =                 h[station_str=='runup']
        sta_idxs =   sta_idxs[station_str=='runup']
        runup_data = runup_data[station_str=='runup',:].T
        
        # Try block in case of failure to find runup.
        try:        
            # Function call
            stats_x, stats_h, *_ = runup.compute_stats(
                t=t,
                x=x,
                h=h,
                runup_data=runup_data,
                sta_idxs=sta_idxs
            )
            
            # Combine into one dictionary, name for clarity
            stats = {
            **{f"x_RUN_{k}": v for k, v in stats_x.items()},
            **{f"h_RUN_{k}": v for k, v in stats_h.items()},
            }
        
            return stats
        
        # If runup isn't found, return {}
        except:
            return {}
            
    
    # Catch cases that are actually flat so runup isn't sensible
    elif flat_or_trap == 'FLAT':
        print('This is a flat case- no runup possble! Skipping')
        return {}
        


#%% Define the paths


main_ds = [
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_00001.nc', 
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_18880.nc' 
        ]

sta_ds = [
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_sta_00001.nc', 
            r'/Users/ryanschanta/Work/Projects/USACE/Email Attachments and DoD Safe/Marissa Emergent/tri_sta_18880.nc' 
        ]




#%% Loop through the files
results = [] 
for ds_path, ds_sta_path in zip(main_ds,sta_ds):
    # Open the data
    dss = xr.open_dataset(ds_sta_path)
    ds =  xr.open_dataset(ds_path)
    # Run post-processing from Mike
    stats = trap_bw_post_runup(dss,ds)
    # Merge results with inputs and append to list
    merged = {**dss.attrs, **stats}
    results.append(merged)

# Make into dataframe
df_runup = pd.DataFrame(results)
# Output to csv
#df_runup.to_csv('/path_I_wint')





