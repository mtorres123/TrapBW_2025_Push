import funwave_amp.HPC.USACE_pbs as HPC

# Inputs to Change
env = "./envs/TRAP_BW.env"

# Files in the pipeline  
generate_file = "generate.py"
condense_file = "process.py"

# Standard Slurm Flags
pbs_defaults = {
    "-l": "nodes=1:ppn=32",              # 1 node with 32 processors
    "-q": "standard",                    # partition → queue
    "-l walltime": "00:30:00",           # time limit
    "-M": "rschanta@uw.edu",             # email address
    "-m": "abe",                         # mail on (a)bort, (b)egin, (e)nd
    "-V": "",                            # export all environment vars
}



# Initialize the pipeline
pipeline = HPC.PBS_Pipeline(pbs_vars = pbs_defaults,
                              env=env)

# Steps of the pipeline
steps = {
    HPC.run_py: {"file": generate_file, "pbs_edit": {"-N": "generate"}},
    HPC.run_fw_run_py_del_A: {"file": generate_file,"pbs_edit": {"-J": "1-8","-N": "main_array"}},
}

# Run the pipeline
pipeline.run_pipeline(steps)
