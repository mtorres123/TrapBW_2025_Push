import matplotlib.pyplot as plt
import numpy as np
offset_l = 25
SWW = 5
SEW = 5
XC_from_SWW = 5
offset = 10
top_width = 3
top_pos = -1
depth = 5
slope = 2
tri_base = (depth+top_pos)/slope
fig,ax = plt.subplots(dpi=200,figsize=(8,3))


## SUBMERGED
# Points of the bathymetry
x_sponge_l = -offset_l - SWW
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset
x_sponge_r = x_right + SEW
# Point of wavemaker
Xc_WK = -offset_l + XC_from_SWW



ax.set_title('Reflection Station Placement')

x_bath = [x_sponge_l,x_left, toe_l,top_l,top_r,toe_r,x_right,x_sponge_r]

z_bath = [-depth,-depth,
          -depth,
          top_pos,
          top_pos,
          -depth,
          -depth,
          -depth]

x_points = x_bath[2:-2]
z_points = z_bath[2:-2]

z_SWL = np.zeros_like(z_bath)
z_bot = -1.1*depth*np.ones_like(z_bath)
z_top = top_pos*np.ones_like(z_bath)

## PLOT GEOMETRY
ax.plot(x_bath, z_bath, color='black')
ax.scatter(x_points, z_points, color='black',alpha=1,zorder=4)
ax.plot(x_bath, z_SWL, color='blue',zorder=-1)


# FILL ELEMENTS
ax.fill_between(x_bath[1:-1],z_bath[1:-1],z_SWL[1:-1], color='aqua',alpha=0.25)

# West Sponge
ax.fill_between(x_bath[0:2],z_bath[0:2],z_SWL[0:2], color='green',alpha=0.25)

ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey')

## PLOT SLOPE




## LINE FUNCTIONS
def arrow_dim(ax,
                        point1,
                        point2,
                        label,pad=0.15,
                        color='black',
                        style="<->",
                        dire = 'vertical',fs = 10):
    x1,y1 = point1
    x2,y2 = point2
    ax.annotate(
        "", 
        xy=point2, xytext=point1,  # arrow tail
        arrowprops=dict(
            arrowstyle=style,
            lw=1.5,
            color=color
        )
    )
    if dire == 'vertical':
        ax.text(x1+pad,0.5*(y1+y2),label,color=color,fontsize=fs)
    elif dire == 'horizontal':
        ax.text(0.5*(x1+x2),y1+pad,label,color=color,ha='center',fontsize=fs)
    
    






# MAKE REFLECTION STUFF
L = 10
fractions = [1/9,1/9,2/9,2/3,1/9,2/9]
pos = toe_l
for k,f in enumerate(fractions):
    if k == 1:
        label = 'Set 1'
    elif k == 4:
        label = 'Set 2'
    else: 
        label = None
    if k in {1,2,3}:
        color = 'red'
    elif k in {4,5,6}:
        color = 'purple'
    else:
        color = 'grey'
    ax.plot([pos, pos],[-depth,0.25*depth],ls='--',color=color,label=label)
    arrow_dim(ax,(pos,0.5),(pos - f*L,0.5),f'{int(f*9)}/9$\lambda_0$',color='black',pad=0.25,
              dire='horizontal')


    pos = pos - f*L
ax.plot([pos, pos],[-depth,0.25*depth],ls='--',color=color)   
ax.legend()
## FORMATTING
ax.set_xticks([])
ax.set_ylabel('z')
ax.set_xlabel('x')
ax.set_xlim(Xc_WK + 5,top_l+top_width/4)
ax.set_ylim(-1.1*depth,max(0.5*depth,2*top_pos))


fig.tight_layout()
fig.savefig('../png/reflection.png', bbox_inches="tight")
