import matplotlib.pyplot as plt
import numpy as np
offset_l = 0.4

offset = 0.4
top_width = 0.55
top_pos = -1
depth = 5
slope = 2
tri_base = (depth+top_pos)/slope
fig,ax = plt.subplots(dpi=200,figsize=(8,3))


## SUBMERGED
# Points og the bathymetry
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset

ax.set_title('Grid Imprecision')

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

ax.plot(x_bath, z_SWL, color='blue',zorder=-1)


# FILL ELEMENTS
ax.fill_between(x_bath,z_bath,z_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey')



# Show grid
DX = 0.47
x_dense = np.arange(min(x_bath), max(x_bath) + DX, DX)
z_dense = np.interp(x_dense, x_bath, z_bath)

ax.plot(x_dense, z_dense, color='red',alpha=1,zorder=7,
           label='FUNWAVE-TVD grid',marker='s',markeredgewidth=1)

ax.scatter(x_points, z_points, color='black',alpha=1,zorder=10,
           label='Points Defining Trapezoid')

## FORMATTING
ax.set_ylabel('z')
ax.set_xlim(-offset_l,tri_base + top_width + tri_base + offset)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))

ax.legend(framealpha=1,facecolor='white',fancybox=False)
fig.savefig('../png/imprecision.png', bbox_inches="tight")
