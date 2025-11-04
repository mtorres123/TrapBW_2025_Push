import os
import textwrap
import numpy as np
from ._plot_helpers import *
from ._trapezoid import find_trapezoid_edges
import matplotlib
import textwrap
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
'''
matplotlib.use("Agg")   # must be before importing pyplot
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
plt.rcParams['text.usetex'] = False       # use LaTeX for all text
#plt.rcParams['font.family'] = 'serif'    # LaTeX default font family
#plt.rcParams['font.serif'] = ['Computer Modern Roman']
'''

def plot_setup(var_dict):
    # Initialize gridspec
    fig = plt.figure(figsize=(12, 6), dpi=150)
    gs = gridspec.GridSpec(3, 5, figure=fig, wspace=0.4, hspace=0.5)
    
    ## UNPACK ---------------------------------------------------------------------
    # Structure geometry
    x_toe_l = var_dict['xF_toe_l']
    x_crest_l = var_dict['xF_crest_l']
    x_crest_r = var_dict['xF_crest_r']
    x_toe_r = var_dict['xF_toe_r']
    z_crest = var_dict['z_crest']
    # Regions
    SWW = var_dict['Sponge_west_width']
    SEWx = var_dict['Sponge_east_width_x']
    Xc_WK = var_dict['Xc_WK']
    # Hydrodynamics
    L = var_dict['L']
    
    # Bathymetry
    DOM = var_dict['DOM']
    h = var_dict['DEP_WK']
    X = DOM.X.values
    Z = -DOM.Z.values[:,0]
    Z_bot = -1.1*h*np.ones_like(Z)
    # Conditions
    USE_CDBWAC = var_dict['USE_CDBWAC']
    FLAT_OR_TRAP = var_dict['FLAT_OR_TRAP']
    
    # End point
    x_end = var_dict['x_end']
    # Iteration
    ITER = var_dict['ITER']
    ## [END] UNPACK ---------------------------------------------------------------
    
    
    
    ## PLOT ONE: REGIONS ======================================================
    ax = fig.add_subplot(gs[0, 0:3])
    ax.set_title('Region Sizing')
    
    # Plot bathymetry and SWL
    ax.plot(DOM.X.values,Z,color='black')
    ax.axhline(0,color='blue')
    
    # Sponge shading
    ax.fill_between([0,SWW],[-h,-h],[0,0],
                    color='green',hatch='x',alpha=0.5)
    ax.fill_between([SEWx,x_end],[-h,-h],[0,0],
                    color='green',hatch='x',alpha=0.5)
    # Bottom shading
    ax.fill_between(X,Z,Z_bot,color='gray')
    
    
    
    ## DIMENSION LINES
    anc = 0.15*h
    draw_hor_dim_line(ax, (0,anc), (SWW,anc), '$\\pi_1$',fontsize=10,lw=1)
    draw_hor_dim_line(ax, (SWW,anc), (Xc_WK,anc), '$\\pi_2$',fontsize=10,lw=1)
    draw_hor_dim_line(ax, (Xc_WK,anc), (x_toe_l,anc), '$\\pi_3$',fontsize=10,lw=1)
    draw_hor_dim_line(ax, (x_toe_r,anc), (SEWx,anc), '$\\pi_5$',fontsize=10,lw=1)
    draw_hor_dim_line(ax, (SEWx,anc), (x_end,anc), '$\\pi_6$',fontsize=10,lw=1)
    
    ## CONSTRUCTION LINES
    anc = 0.25*h
    points = [SWW,Xc_WK,x_toe_l,x_toe_r,SEWx]
    for p in points:
        ax.plot([p,p],[-h,anc],ls='--',color='grey',zorder=100)
        
    
    # CD OR BWAC CONDITIONALS -------------------------------------------------
    if USE_CDBWAC == 'BWAC':
        # Show purple water column for BWAC
        ax.fill_between([x_toe_l,x_toe_r],[-h,-h],[0,0],
                        color='purple',alpha=0.25,zorder=-1)
        # Color BWAC bottom purple
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='purple',lw=2)
                
        # Color remaining areas blue
        ax.fill_between([SWW,x_toe_l],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
        ax.fill_between([x_toe_r,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
    elif USE_CDBWAC == 'CD':
        # Shade water
        ax.fill_between([SWW,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25,zorder=-1)
        # Color friction bottom orange
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='darkorange',lw=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
    
    
    # FLAT OR TRAP CONDITIONALS -----------------------------------------------
    t_color = 'grey'
    trap_x = [x_toe_l,x_crest_l,x_crest_r,x_toe_r]
    trap_z = [-h,z_crest,z_crest,-h]
    
    
    if FLAT_OR_TRAP == 'FLAT':
        ax.plot(trap_x,trap_z,color='grey',ls='--')
    elif FLAT_OR_TRAP == 'TRAP':
        ax.scatter(trap_x,trap_z,color='black',marker='o',zorder=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
     
    ax.axhline(0.15,zorder=400)
    #ax.set_xlim(220,245)
    # Limits
    ax.set_xlim(0,x_end)
    #ax.set_xlim(220,245)
    ax.set_ylim(-1.1*h,0.5*h)
    ## [END] PLOT ONE: REGIONS ================================================
    
    
    
    
    #%% PLOT TWO: STRUCTURE ZOOM ==============================================
    ax = fig.add_subplot(gs[0, 3:])
    ax.set_title('Structure Region')
    
    ax.plot(DOM.X.values,Z,color='black')
    ax.axhline(0,color='blue')
    
    # Bottom shading
    ax.fill_between(X,Z,Z_bot,color='lightgray')
    
    ## DIMENSION LINES
    anc = 0.15*h
    
    # CD OR BWAC CONDITIONALS -------------------------------------------------
    if USE_CDBWAC == 'BWAC':
        # Show purple water column for BWAC
        ax.fill_between([x_toe_l,x_toe_r],[-h,-h],[0,0],
                        color='purple',alpha=0.25,zorder=-1)
        # Color BWAC bottom purple
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='purple',lw=2)
                
        # Color remaining areas blue
        ax.fill_between([SWW,x_toe_l],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
        ax.fill_between([x_toe_r,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
    elif USE_CDBWAC == 'CD':
        # Shade water
        ax.fill_between([SWW,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25,zorder=-1)
        # Color friction bottom orange
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='darkorange',lw=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
    
    
    
    # FLAT OR TRAP CONDITIONALS -----------------------------------------------
    t_color = 'grey'
    trap_x = [x_toe_l,x_crest_l,x_crest_r,x_toe_r]
    trap_z = [-h,z_crest,z_crest,-h]
    
    # CONSTRUCTION LINES
    anc = 0.25*h
    for tx in [x_toe_l,x_toe_r]:
        ax.plot([tx,tx],[-h,anc],color='grey',ls='--')
    for tx in [x_crest_l,x_crest_r]:
        ax.plot([tx,tx],[z_crest,anc],color='grey',ls='--')
    # DIMENSION LINE
    draw_hor_dim_line_outside(ax,(x_crest_l,anc),(x_crest_r,anc),
                                  '$\\pi_4$',fontsize=10,offset=-0.25,offset_x=1.75,
                                  lw=1)    
    if FLAT_OR_TRAP == 'FLAT':
        ax.plot(trap_x,trap_z,color='grey',ls='--')
    elif FLAT_OR_TRAP == 'TRAP':
        ax.scatter(trap_x,trap_z,color='black',marker='o',zorder=2,s=10)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
     
    

    # Limits
    ax.set_xlim(x_toe_l-0.1*L,x_toe_r+0.1*L)
    ax.set_ylim(-1.1*h,0.5*h)
    ## [END] PLOT TWO: STRUCTURE ZOOM =========================================
    
    
    #%% PLOT THREE: REFLECTION STATIONS =======================================
    ax = fig.add_subplot(gs[1, 0:2])
    ax.set_title('Reflection Station Placement')
    
    ax.plot(DOM.X.values,-DOM.Z.values[:,0],color='black')
    ax.axhline(0,color='blue')
    # Bottom shading
    ax.fill_between(X,Z,Z_bot,color='lightgray')
    

    
    # CD OR BWAC CONDITIONALS -------------------------------------------------
    if USE_CDBWAC == 'BWAC':
        # Show purple water column for BWAC
        ax.fill_between([x_toe_l,x_toe_r],[-h,-h],[0,0],
                        color='purple',alpha=0.25,zorder=-1)
        # Color BWAC bottom purple
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='purple',lw=2)
                
        # Color remaining areas blue
        ax.fill_between([SWW,x_toe_l],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
        ax.fill_between([x_toe_r,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
    elif USE_CDBWAC == 'CD':
        # Shade water
        ax.fill_between([SWW,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25,zorder=-1)
        # Color friction bottom orange
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='darkorange',lw=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
    
    
    
    # FLAT OR TRAP CONDITIONALS -----------------------------------------------
    t_color = 'grey'
    trap_x = [x_toe_l,x_crest_l,x_crest_r,x_toe_r]
    trap_z = [-h,z_crest,z_crest,-h]
    
    # CONSTRUCTION LINES
    anc = 0.25*h
    for tx in [x_toe_l,x_toe_r]:
        ax.plot([tx,tx],[-h,anc],color='grey',ls='--')
    for tx in [x_crest_l,x_crest_r]:
        ax.plot([tx,tx],[z_crest,anc],color='grey',ls='--')
    
    
    if FLAT_OR_TRAP == 'FLAT':
        ax.plot(trap_x,trap_z,color='grey',ls='--')
    elif FLAT_OR_TRAP == 'TRAP':
        ax.scatter(trap_x,trap_z,color='black',marker='o',zorder=2,s=10)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
     
    
    
    ax.set_ylim(-1.1*h,0.5*h)
    
    # GAGES -------------------------------------------------------------------
    # Pull out M positions of gages
    dso_reflection = DOM.where(DOM.station_str == "reflection", drop=True)
    Xr = dso_reflection.X.values
    Mvals = dso_reflection.Mglob_gage.values.astype(int)
    for M in Mvals:
        ax.plot([Xr[M],Xr[M]],[-h,anc],color='red')
        
    # Label gage spacing in pairs
    for pair in list(zip(Mvals[0:-1], Mvals[1:])):
        m1,m2 = pair
        dist = round(9*(Xr[m2]-Xr[m1])/L)
        if dist == 1:
            draw_hor_dim_line(ax, (Xr[m1],anc), (Xr[m2],anc), '$\\lambda$/9',offset=0.1,
                              fontsize=6.5,lw=1)
        else:
            draw_hor_dim_line(ax, (Xr[m1],anc), (Xr[m2],anc), f'{round(dist)}$\\lambda$/9',offset=0.1,
                              fontsize=6.5,lw=1)        
    # Add on toe to first spacing
    draw_hor_dim_line(ax, (x_toe_l,anc), (Xr[m2],anc), '$\\lambda$/9',offset=0.1,
                      fontsize=6.5,lw=1)      
    ax.set_xlim(min(Xr[Mvals]-L/9),
                x_crest_l)
    ## [END] PLOT THREE: REFLECTION STATIONS ==================================
    
    
    #%% PLOT FOUR: TRANSMISSION STATIONS ======================================
    ax = fig.add_subplot(gs[1, 2:4])
    ax.set_title('Transmission Station Placement')
    
    # Plot bathymetry and SWL
    ax.plot(DOM.X.values,-DOM.Z.values[:,0],color='black')
    ax.axhline(0,color='blue')
    ax.fill_between(X,Z,Z_bot,color='lightgray')
    
    ## DIMENSION LINES
    anc = 0.15*h
    
    # CD OR BWAC CONDITIONALS -------------------------------------------------
    if USE_CDBWAC == 'BWAC':
        # Show purple water column for BWAC
        ax.fill_between([x_toe_l,x_toe_r],[-h,-h],[0,0],
                        color='purple',alpha=0.25,zorder=-1)
        # Color BWAC bottom purple
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='purple',lw=2)
                
        # Color remaining areas blue
        ax.fill_between([SWW,x_toe_l],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
        ax.fill_between([x_toe_r,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
    elif USE_CDBWAC == 'CD':
        # Shade water
        ax.fill_between([SWW,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25,zorder=-1)
        # Color friction bottom orange
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='darkorange',lw=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
    
    
    
    # FLAT OR TRAP CONDITIONALS -----------------------------------------------
    t_color = 'grey'
    trap_x = [x_toe_l,x_crest_l,x_crest_r,x_toe_r]
    trap_z = [-h,z_crest,z_crest,-h]
    
    # CONSTRUCTION LINES
    anc = 0.25*h
    for tx in [x_toe_l,x_toe_r]:
        ax.plot([tx,tx],[-h,anc],color='grey',ls='--')
    for tx in [x_crest_l,x_crest_r]:
        ax.plot([tx,tx],[z_crest,anc],color='grey',ls='--')
    
    
    if FLAT_OR_TRAP == 'FLAT':
        ax.plot(trap_x,trap_z,color='grey',ls='--')
    elif FLAT_OR_TRAP == 'TRAP':
        ax.scatter(trap_x,trap_z,color='black',marker='o',zorder=2,s=10)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
     
    
    
    ax.set_ylim(-1.1*h,0.5*h)
    dso_reflection = DOM.where(DOM.station_str == "transmission", drop=True)
    Xr = dso_reflection.X.values
    Mvals = dso_reflection.Mglob_gage.values.astype(int)
    for M in Mvals:
        ax.plot([Xr[M],Xr[M]],[-h,anc],color='red')
        if Xr[M] < x_toe_l:
            dist = round(9*(x_toe_l-Xr[M])/L)
            draw_hor_dim_line(ax, (x_toe_l,anc), (Xr[M],anc), f'{round(dist)}$\\lambda$/9',fontsize=10,lw=1)
        elif Xr[M] > x_toe_r:
            dist = round(9*(Xr[M]-x_toe_r)/L)
            draw_hor_dim_line(ax, (x_toe_r,anc), (Xr[M],anc), f'{round(dist)}$\\lambda$/9',fontsize=10,lw=1)   
    
    
    ax.set_xlim(min(Xr[Mvals]-L),
                max(Xr[Mvals]+L))
    ## [END] PLOT FOUR: TRANSMISSION STATIONS =====================================
    
    
    #%% PLOT FIVE: RUNUP STATIONS ===========================================
    ax = fig.add_subplot(gs[1, 4])
    ax.set_title('Runup Gages')
    
    ax.plot(DOM.X.values,-DOM.Z.values[:,0],color='black')
    ax.axhline(0,color='blue')
    
    # Bottom shading
    ax.fill_between(X,Z,Z_bot,color='lightgray')
    
    ## DIMENSION LINES
    anc = 0.15*h
    
    # CD OR BWAC CONDITIONALS -----------------------------------------------------
    if USE_CDBWAC == 'BWAC':
        # Show purple water column for BWAC
        ax.fill_between([x_toe_l,x_toe_r],[-h,-h],[0,0],
                        color='purple',alpha=0.25,zorder=-1)
        # Color BWAC bottom purple
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='purple',lw=2)
                
        # Color remaining areas blue
        ax.fill_between([SWW,x_toe_l],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
        ax.fill_between([x_toe_r,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25)
    elif USE_CDBWAC == 'CD':
        # Shade water
        ax.fill_between([SWW,SEWx],[-h,-h],[0,0],
                        color='aqua',alpha=0.25,zorder=-1)
        # Color friction bottom orange
        tbool = (X>x_toe_l) & (X< x_toe_r)
        ax.plot(X[tbool],Z[tbool],color='darkorange',lw=2)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
    
    
    
    # FLAT OR TRAP CONDITIONALS -----------------------------------------------
    trap_x = [x_toe_l,x_crest_l,x_crest_r,x_toe_r]
    trap_z = [-h,z_crest,z_crest,-h]
    
    # CONSTRUCTION LINES
    anc = 0.25*h
    for tx in [x_toe_l,x_toe_r]:
        ax.plot([tx,tx],[-h,anc],color='grey',ls='--')
    for tx in [x_crest_l,x_crest_r]:
        ax.plot([tx,tx],[z_crest,anc],color='grey',ls='--')
    
    
    if FLAT_OR_TRAP == 'FLAT':
        ax.plot(trap_x,trap_z,color='grey',ls='--')
    elif FLAT_OR_TRAP == 'TRAP':
        ax.scatter(trap_x,trap_z,color='black',marker='o',zorder=2,s=10)
    # [END] CD OR BWAC CONDITIONALS -------------------------------------------
     
    
    
    ax.set_ylim(-1.1*h,0.5*h)
    dso_reflection = DOM.where(DOM.station_str == "runup", drop=True)
    Xr = dso_reflection.X.values
    Mvals = dso_reflection.Mglob_gage.values.astype(int)
    for M in Mvals:
        M = int(M)
        ax.plot([Xr[M],Xr[M]],[-h,anc],color='red')
    ax.set_xlim(x_toe_l,x_crest_r)
    ## [END] PLOT FOUR: RUNUP STATIONS ========================================
    
    
    
    #%% HELPER
    
    def make_info_box(ax, var_dict, keys_to_extract, textwrap_width=25, fontsize=7):
        pairs = []
        for k in keys_to_extract:
            v = var_dict[k]
    
            # allow only float, int, or string without slashes
            if isinstance(v, float):
                pairs.append(f"{k}={v:.3g}")  # 3 sig figs
            elif isinstance(v, int):
                pairs.append(f"{k}={v}")
            elif isinstance(v, str) and "/" not in v and "\\" not in v:
                pairs.append(f"{k}={v}")
            else:
                continue  # skip invalid types
    
        # Join into a single long string
        all_text = ", ".join(pairs)
    
        # Wrap at chosen character width
        wrapped_text = textwrap.fill(all_text, width=textwrap_width)
    
        props = dict(boxstyle="square", facecolor="white", alpha=0.8)
        ax.text(
            0.5, 1, wrapped_text,
            fontsize=fontsize,
            verticalalignment="top",
            horizontalalignment="center",
            bbox=props
        )
    
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_axis_off()
        
    #%% PLOT SIX: HYDRODYNAMICS STATIONS ======================================
    ax = fig.add_subplot(gs[2, 0])
    ax.set_title('Hydrodynamics',fontsize=9)
    
    # Keys you want to pull values for
    hy_keys = ["k", "kh", "L", "c", "Tperiod", "DEP_WK", "relH","WAVEMAKER"]
    if var_dict['WAVEMAKER'] == 'WK_REG':
        hy_keys.append('AMP_WK')
    elif var_dict['WAVEMAKER'] == 'WK_IRR':
        hy_keys.extend(['AMP_WK','FreqPeak','FreqMin','FreqMax','Hmo'])
    
    make_info_box(ax,var_dict,hy_keys,textwrap_width = 25,fontsize = 7)
    
    #%% PLOT SEVEN: GEOMETRY ==================================================
    ax = fig.add_subplot(gs[2, 1])
    ax.set_title('Domain Setup',fontsize=9)
    
    # Keys you want to pull values for
    geo_keys = ["PI_1", "PI_2", "PI_3", "PI_4", "PI_5", "PI_6", 
                       "Xc_WK", "Sponge_west_width", 'Sponge_east_width']
    
    make_info_box(ax,var_dict,geo_keys,textwrap_width = 25,fontsize = 7)
    
    #%% PLOT SEVEN: BREAKWATER ================================================
    ax = fig.add_subplot(gs[2, 2])
    ax.set_title('Breakwater Setup',fontsize=9)
    
    # Keys you want to pull values for
    bk_keys = ["m_slope", "relF", "z_crest",
               "x_toe_l", "x_toe_r", "x_crest_l", "x_crest_r", 
               "USE_CDBWAC","CDBWAC"]
    
    make_info_box(ax,var_dict,bk_keys,textwrap_width = 25,fontsize = 7)
    
    
    
    #%% PLOT EIGHT: EVERYTHING ELSE ===========================================
    ax = fig.add_subplot(gs[2, 3:])
    ax.set_title('Other Parameters',fontsize=9)
    
    # Keys you want to pull values for
    
    combined = hy_keys + geo_keys + bk_keys
    
    filtered = {k: v for k, v in var_dict.items() if k not in combined}
    make_info_box(ax,var_dict,filtered,textwrap_width = 70,fontsize = 6)
    #%% [END] PLOT EIGHT: EVERYTHING ELSE =====================================
    
    
    
    # TITLE AND OUT
    fig.suptitle(f"Trial {ITER:05d}: Trapezoidal Breakwater Suite", fontsize=14)
    fig_path = os.getenv("figs") 
    fig.savefig(os.path.join(fig_path,f'figure_{ITER:05d}.png'))
    plt.close(fig)
    
    return