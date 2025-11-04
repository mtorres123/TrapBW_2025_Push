import os
from dotenv import load_dotenv
import sys
import funwave_amp as fds
import model_code as mod         # Model specific code


#%% Model Setup
d = fds.setup_key_dirs(name='TRAP_BW',
                   main_dir = '.', 
                   input_dir = './test_out/inputs', 
                   log_dir='./test_out/logs',
                   bathy_dir = './test_out/bathy',
                   station_dir = './test_out/stations',
                   friction_dir= './test_out/friction',
                   result_folder_dir = './test_out/output_raw',
                   breakwater_dir = './test_out/breakwater',
                   nc_dir = './test_out/nc_files',
                   nc_sta_dir='./test_out/nc_sta_files',
                   FW_ex = ".",
                   conda = ".",
                   dir_add_ons={'figs': './test_out/figures'})


load_dotenv(d['env_file'])

#%%
design_matrix = mod.design_matrix_base()

function_set = [mod.get_hydrodynamics,
                mod.find_trapezoid_geometry,
                mod.set_bathymetry,
                mod.set_regions,
                mod.find_discrete_trap_points,
                mod.set_stations,
                mod.set_CDBWAC,
                mod.set_total_time]


# Filter functions
filter_functions = [mod.filter_kh]

# Plot functions
plot_functions = [mod.plot_setup]

# Print functions
print_functions = [fds.print_FRICTION_OR_BREAKWATER_FILE,
                  fds.print_STATIONS_FILE,
                  fds.print_DEPTH_FILE]




# Write the files
df_pass,df_fail = fds.process_design_matrix(matrix_dict = design_matrix,
                                    function_set = function_set, 
                                    filter_sets = filter_functions,
                                    plot_sets = plot_functions,
                                    print_sets = print_functions,
                                    summary_formats = ['parquet','csv'])

print('File Generation Script Run!')
