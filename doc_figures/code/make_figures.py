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


## SUBMERGED
ax = axes[0]
# Points og the bathymetry
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset

ax.set_title('Submerged Breakwater')

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


# FILL ELEMENTS
ax.fill_between(x_bath,z_bath,z_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey')


## PLOT SLOPE
ax.plot([tri_base/3,2*tri_base/3],  
        [-depth +slope*tri_base/3,-depth +slope*tri_base/3],
        color='black',ls='--')
ax.plot([2*tri_base/3,2*tri_base/3],  
        [-depth +slope*tri_base/3,-depth +2*slope*tri_base/3],
        color='black',ls='--')
ax.text(2*tri_base/3 + tri_base/12, 
        -depth + slope*tri_base/2,
        f'$m={slope} = \\text{{run}}/\\text{{rise}}$',color='black')


## PLOT SINE WAVE
a = 0.75
x_sine = np.linspace(-0.9*offset_l,-0.5*offset_l)
y_sine = a*np.cos(np.pi*x_sine)
ax.plot(x_sine,y_sine,color='blue')


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
    
    
    
    
arrow_dim(ax,(0,0),(0,top_pos),f'$z_{{top}}={top_pos}$',style="->")


arrow_dim(ax,(top_l,0.5),(top_r,0.5),f'$w=\pi_4\lambda_0$',color='black',pad=0.25,
          dire='horizontal')



arrow_dim(ax,(-0.45*offset_l,-a),(-0.45*offset_l,a),
          '',color='black',pad=0.25,
          dire='vertical')

arrow_dim(ax,((x_right + toe_r)/2,-depth),((x_right + toe_r)/2,0),
          f'$h={depth}$',color='black',pad=0.15,
          dire='vertical')
## PLOT LINES
ax.plot(x_bath,z_top,color='grey',lw=1,ls='--',zorder=-1)
x_sine_dim = np.linspace(-0.9*offset_l,-0.425*offset_l)
ax.text(-0.425*offset_l,a/2,f'$H_{{mo}}={2*a}$',va='center',color='black')
ax.plot(x_sine_dim,-a*np.ones_like(x_sine),color='grey',lw=1,ls='--',zorder=-1)
ax.plot(x_sine_dim,a*np.ones_like(x_sine),color='grey',lw=1,ls='--',zorder=-1)
ax.plot([top_l,top_l],[top_pos,10],color='grey',lw=1,ls='--',zorder=-1)
ax.plot([top_r,top_r],[top_pos,10],color='grey',lw=1,ls='--',zorder=-1)


## TEXTBOX
ax.text(
    -0.95*offset_l, -0.9*depth, 
   f"$\\text{{relH}} = H_{{mo}}/h$ = {2*a}/{depth} = {2*a/depth} \n" + 
     f"$\\text{{relF}} = z_{{top}}/H_{{mo}}$= {top_pos}/{2*a} = {top_pos/(2*a):.2g}",
    ha="left", va="bottom", fontsize=9,
    bbox=dict(
        boxstyle="square",   # no rounded corners
        facecolor="white",
        edgecolor="black",
        linewidth=1
    )
)

## FORMATTING
ax.set_ylabel('z')
ax.set_xlim(-offset_l,tri_base + top_width + tri_base + offset)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))


#%% EMERGENT
top_pos = 1
offset_l = 5

offset = 2
top_width = 1.25
depth = 5
slope = 2
tri_base = (depth+top_pos)/slope


ax = axes[1]
# Points og the bathymetry
x_left = -offset_l
toe_l = 0
top_l = tri_base
top_r = top_l + top_width
toe_r = top_r + tri_base
x_right = toe_r+ offset

ax.set_title('Emergent Breakwater')

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


# FILL ELEMENTS
ax.fill_between(x_bath,z_bath,z_SWL, color='aqua',alpha=0.25)
ax.fill_between(x_bath,z_bath,z_bot, color='lightgrey')


## PLOT SLOPE
ax.plot([tri_base/3,2*tri_base/3],  
        [-depth +slope*tri_base/3,-depth +slope*tri_base/3],
        color='black',ls='--')
ax.plot([2*tri_base/3,2*tri_base/3],  
        [-depth +slope*tri_base/3,-depth +2*slope*tri_base/3],
        color='black',ls='--')
ax.text(2*tri_base/3 + tri_base/12, 
        -depth + slope*tri_base/2,
        f'$m={slope} = \\text{{run}}/\\text{{rise}}$',color='black')


## PLOT SINE WAVE
a = 0.75
x_sine = np.linspace(-0.9*offset_l,-0.5*offset_l)
y_sine = a*np.cos(np.pi*x_sine)
ax.plot(x_sine,y_sine,color='blue')



    
    
    
arrow_dim(ax,(0,0),(0,top_pos),f'$z_{{top}}={top_pos}$',style="->")


arrow_dim(ax,(top_l,1.25*top_pos),(top_r,1.25*top_pos),f'$w=\pi_4\lambda_0$',color='black',pad=0.25,
          dire='horizontal',fs=10)


arrow_dim(ax,(-0.45*offset_l,-a),(-0.45*offset_l,a),
          '',color='black',pad=0.25,
          dire='vertical')

arrow_dim(ax,((x_right + toe_r)/2,-depth),((x_right + toe_r)/2,0),
          f'$h={depth}$',color='black',pad=0.15,
          dire='vertical')
## PLOT LINES
ax.plot(x_bath,z_top,color='grey',lw=1,ls='--',zorder=-1)
x_sine_dim = np.linspace(-0.9*offset_l,-0.425*offset_l)
ax.text(-0.425*offset_l,a/2,f'$H_{{mo}}={2*a}$',va='center',color='black')
ax.plot(x_sine_dim,-a*np.ones_like(x_sine),color='grey',lw=1,ls='--',zorder=-1)
ax.plot(x_sine_dim,a*np.ones_like(x_sine),color='grey',lw=1,ls='--',zorder=-1)
ax.plot([top_l,top_l],[top_pos,10],color='grey',lw=1,ls='--',zorder=-1)
ax.plot([top_r,top_r],[top_pos,10],color='grey',lw=1,ls='--',zorder=-1)


## TEXTBOX
ax.text(
    -0.95*offset_l, -0.9*depth, 
   f"$\\text{{relH}} = H_{{mo}}/h$ = {2*a}/{depth} = {2*a/depth} \n" + 
     f"$\\text{{relF}} = z_{{top}}/H_{{mo}}$= {top_pos}/{2*a} = {top_pos/(2*a):.2g}",
    ha="left", va="bottom", fontsize=9,
    bbox=dict(
        boxstyle="square",   # no rounded corners
        facecolor="white",
        edgecolor="black",
        linewidth=1
    )
)

## FORMATTING
ax.set_ylabel('z')
ax.set_xlim(-offset_l,tri_base + top_width + tri_base + offset)
ax.set_ylim(-1.1*depth,max(0.25*depth,2*top_pos))
fig.tight_layout()
fig.savefig('../png/suberged.png')
