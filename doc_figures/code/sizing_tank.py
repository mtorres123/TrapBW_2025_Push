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



ax.set_title('Domain Sizing')

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
ax.text(np.mean(x_bath[0:2]),-0.5*depth,'West\nSponge',color='green',ha='center')
# East Sponge
ax.fill_between(x_bath[-2:],z_bath[-2:],z_SWL[-2:], color='green',alpha=0.25)
ax.text(np.mean(x_bath[-2:]),-0.5*depth,'East\nSponge',color='green',ha='center')

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
    
    
# PI_1 
arrow_dim(ax,(-offset_l-SWW,0.5),(-offset_l,0.5),f'$\pi_1\lambda_0$',color='black',pad=0.25,
          dire='horizontal')
ax.plot([-offset_l,-offset_l],[-depth,0.25*depth],ls='--',color='gray')
# PI_2 
arrow_dim(ax,(-offset_l,0.5),(Xc_WK,0.5),f'$\pi_2\lambda_0$',color='black',pad=0.25,
          dire='horizontal')
# PI_3 
arrow_dim(ax,(Xc_WK,0.5),(toe_l,0.5),f'$\pi_3\lambda_0$',color='black',pad=0.25,
          dire='horizontal')
ax.plot([toe_l,toe_l],[-depth,0.25*depth],ls='--',color='gray')
# PI_4
ax.plot([top_l,top_l],[top_pos,0.25*depth],ls='--',color='gray')
arrow_dim(ax,(top_l,0.5),(top_r,0.5),f'$\pi_4\lambda_0$',color='black',pad=0.25,
          dire='horizontal')
ax.plot([top_r,top_r],[top_pos,0.25*depth],ls='--',color='gray')
# PI_5 
ax.plot([toe_r,toe_r],[-depth,0.25*depth],ls='--',color='gray')
arrow_dim(ax,(toe_r,0.5),(x_bath[-2],0.5),f'$\pi_5\lambda_0$',color='black',pad=0.25,
          dire='horizontal')
ax.plot([x_bath[-2],x_bath[-2]],[-depth,0.25*depth],ls='--',color='gray')
# PI_6
arrow_dim(ax,(x_bath[-2],0.5),(x_bath[-1],0.5),f'$\pi_6\lambda_0$',color='black',pad=0.25,
          dire='horizontal')




# LINES
ax.plot([Xc_WK,Xc_WK],[-depth,0.25*depth],color='red')
ax.text(Xc_WK,-0.9*depth,'Xc_WK',color='red',rotation=90,ha='right')



## FORMATTING
ax.set_ylabel('z')
ax.set_xlabel('x')
ax.set_xlim(-offset_l-SWW,tri_base + top_width + tri_base + offset+ SEW)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))


fig.tight_layout()
fig.savefig('../png/sizing.png', bbox_inches="tight")
