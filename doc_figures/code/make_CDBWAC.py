import matplotlib.pyplot as plt
import numpy as np
offset_l = 5

offset = 2
top_width = 1.25
top_pos = -1
depth = 5
slope = 2
tri_base = (depth+top_pos)/slope
fig,axes = plt.subplots(2,1,dpi=200,figsize=(8,6))

ax = axes[0]
# Points og the bathymetry
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset

ax.set_title('Bottom Friction Option: CDBWAC = CD')

x_bath = [x_left, toe_l,top_l,top_r,toe_r,x_right]

z_bath = [-depth,
          -depth,
          top_pos,
          top_pos,
          -depth,
          -depth]

x_points = x_bath[1:-1]
z_points = z_bath[1:-1]

z_SWL = np.zeros_like(z_bath)
z_bot = -1.1*depth*np.ones_like(z_bath)
z_top = top_pos*np.ones_like(z_bath)

## PLOT GEOMETRY
ax.plot(x_bath, z_bath, color='black')
ax.scatter(x_points, z_points, color='black',alpha=1,zorder=4)
ax.plot(x_bath, z_SWL, color='blue',zorder=-1)


# Interpolate to 100 points
x_interp = np.linspace(toe_l, toe_r, 100)
z_interp = np.interp(x_interp, x_bath, z_bath)



ax.plot([toe_l,top_l,top_r,toe_r],[-depth,top_pos,top_pos,-depth],color='red',
        lw=4,label='Bottom Friction Applied')

# FILL ELEMENTS
ax.fill_between(x_bath,z_bath,z_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey',zorder=-1)




## PLOT SINE WAVE
a = 0.75
x_sine = np.linspace(-0.9*offset_l,-0.5*offset_l)
y_sine = a*np.cos(np.pi*x_sine)
ax.plot(x_sine,y_sine,color='blue')
ax.legend()


    
#%%
## FORMATTING
ax.set_ylabel('z')
ax.set_xlim(-offset_l,tri_base + top_width + tri_base + offset)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))

ax = axes[1]
# Points og the bathymetry
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset

ax.set_title('Bottom Friction Option: CDBWAC = BWAC')

x_bath = [x_left, toe_l,top_l,top_r,toe_r,x_right]

z_bath = [-depth,
          -depth,
          top_pos,
          top_pos,
          -depth,
          -depth]

x_points = x_bath[1:-1]
z_points = z_bath[1:-1]

z_SWL = np.zeros_like(z_bath)
z_bot = -1.1*depth*np.ones_like(z_bath)
z_top = top_pos*np.ones_like(z_bath)

## PLOT GEOMETRY
ax.plot(x_bath, z_bath, color='black')
ax.scatter(x_points, z_points, color='black',alpha=1,zorder=4)
ax.plot(x_bath, z_SWL, color='blue',zorder=-1)


# Interpolate to 100 points
x_interp = np.linspace(toe_l, toe_r, 100)
z_interp = np.interp(x_interp, x_bath, z_bath)



## Flat regions for shading
x_flat_l,x_flat_r = [x_left, toe_l], [toe_r,x_right]
z_flat, z_flat_SWL = [-depth,-depth], [0,0]
# Trap region for shading
x_trapp = [toe_l,top_l,top_r,toe_r] 
z_trapp = [-depth,top_pos, top_pos, -depth]
z_trapp_SWL = [0,0,0,0]

# FILL ELEMENTS
ax.plot([toe_l,top_l,top_r,toe_r],[-depth,top_pos,top_pos,-depth],color='purple',lw=2)
ax.fill_between(x_trapp
                ,z_trapp,
                z_trapp_SWL, color='thistle',alpha=1,
                facecolor="thistle",       # transparent fill
                edgecolor="grey",        # hatch color
                hatch = 'x',
                linewidth=0.5,          # no border outline
                zorder=-3, label='BWAC Applied'
            )


ax.fill_between(x_flat_r,z_flat,z_flat_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_flat_l,z_flat,z_flat_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey',zorder=-2)




## PLOT SINE WAVE
a = 0.75
x_sine = np.linspace(-0.9*offset_l,-0.5*offset_l)
y_sine = a*np.cos(np.pi*x_sine)
ax.plot(x_sine,y_sine,color='blue')



    

## FORMATTING
ax.set_ylabel('z')
ax.set_xlim(-offset_l,tri_base + top_width + tri_base + offset)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))
ax.legend()
ax.set_xlabel('$x$')

fig.tight_layout()
fig.savefig('../png/CDBWAC.png')

