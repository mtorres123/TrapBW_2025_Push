import overtopping
import numpy as np
import xarray as xr
import pandas as pd

def trap_bw_post_overtopping(dss,ds): 
    '''
    This is a wrapper function to use Mike's post-processing code for 
    overtopping on station outputs of Ryan's file workflow. To work, it needs 
    access to both the bulk file (ds) and the station file (dss). Because of 
    this it's important to use the `xr.open_dataset() command compared to the 
    `xr.load_dataset()` since we don't want the giant file in memory!
    '''
    # UNPACK ------------------------------------------------------------------
    # 4 Columns from dss
    t = dss.t_station.values
    eta = dss.eta_sta.values
    u = dss.u_sta.values
    v = dss.v_sta.values
    
    # Other necessary information from dss
    sta_idxs = dss.Mglob_gage.values
    Z = dss.Z.values[:,0]
    DX = dss.DX
    min_depth = dss.MinDepth
    
    # From main file
    station_str = ds.station_str.values
    flat_or_trap = ds.FLAT_OR_TRAP
    # [END] UNPACK ------------------------------------------------------------
    
    # Only do trapezoidal
    if flat_or_trap == 'TRAP':
        # Get the (x,h(x)) values at each station
        x = sta_idxs*DX
        h = Z[sta_idxs]
        
        # Index out just the overtopping point
        x =                 x[station_str=='overtopping'].ravel()
        h =                 h[station_str=='overtopping'].ravel()
        sta_idxs =   sta_idxs[station_str=='overtopping'].ravel()
        eta   =           eta[station_str=='overtopping',:].ravel()
        u   =               u[station_str=='overtopping',:].ravel()
        v   =               v[station_str=='overtopping',:].ravel()
        
        # Combine 
        station_data = np.column_stack([t, eta, u, v])
        
        try:  
            # Function call
            stats, flux_data, peak_data, properties = overtopping.compute_stats(
                station_data, 
                min_depth=min_depth, 
                sta_depth=h
            )
            
            stats = {
            **{f"OT_{k}": v for k, v in stats.items()},
            }
            
            return stats
        except:
            return {}
        
    elif flat_or_trap == 'FLAT':
        print('This is a flat case! Skipping overtopping...')
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
    stats = trap_bw_post_overtopping(dss,ds)
    # Merge results with inputs and append to list
    merged = {**dss.attrs, **stats}
    results.append(merged)

# Make into dataframe
df_overtop = pd.DataFrame(results)
# Output to csv
#df_overtop.to_csv('/path_I_want.csv')

