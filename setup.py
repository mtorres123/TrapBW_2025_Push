import os
import funwave_amp as fds



#%% MAIN
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

