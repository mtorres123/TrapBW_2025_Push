
def design_matrix_base():
    design_matrix = {
        
                "TITLE": {
                    'TITLE': 'Trapezoidal Breakwater' 
                }, 
                
                
                "PARALLEL INFO": {
                    'PX': '32',
                    'PY': '1'
                },
                
                
                "DIMENSION": {
                    'Mglob': 'DYNAMIC',
                    'Nglob': '1',
                },
                
                
                "TIME": {
                    'PLOT_INTV': '1.0',
                    'PLOT_INTV_STATION': '0.1',
                    'SCREEN_INTV': '10.0',
                    'TOTAL_TIME': 'DYNAMIC'
                }, 
                
                
                "Grid": {
                    'DX': 'DYNAMIC',
                    'DY': 'DYNAMIC',
                    'DEPTH_TYPE': 'DATA'
                }, 
                
            
                "WAVEMAKER": {
                    'WAVEMAKER': ['WK_IRR','WK_REG'],
                    'Delta_WK': '3.0',
                    'Tperiod': ['4.0'],
                    'FreqMin': '0.02',
                    'FreqMax': '0.5'
                },
                
                
                "SPONGE LAYER": {
                    'FRICTION_SPONGE': 'T',
                    'DIRECT_SPONGE': 'T',
                    'Csp': '0.0',
                },
                
                
                "NUMERICS": {
                    'HIGH_ORDER': 'THIRD',
                    'MinDepth': '0.05'
                },
                
                
                "BREAKING": {
                    'VISCOSITY_BREAKING': 'T',
                    'Cbrk1': '0.65',
                    'Cbrk2': '0.35',
                },
                
                "OUTPUT": {
                    'FIELD_IO_TYPE': 'BINARY',
                    'DEPTH_OUT': 'T',
                    'ETA': 'T',
                    'MASK': 'T',
                    'MASK9': 'T',
                    'OUT_NU': 'T'
                },
                
                
                "STRUCTURE GEOMETRY": {
                    'DEP_WK': ['3.0'],
                    'FLAT_OR_TRAP': ['TRAP','FLAT'],
                    'm_slope': '3',
                    'PI_1': '2.0',
                    'PI_2':  '2.0',
                    'PI_3':  '8.0',
                    'relF': '-1.0',
                    'relH': '0.1',
                    'PI_4': '0.03',
                    'PI_5': '12.0',
                    'PI_6': '4.0',
                    'CDBWAC': ["0.010"],
                    'USE_CDBWAC': ['CD','BWAC']
                    
                    
                }
            }
    
    return design_matrix