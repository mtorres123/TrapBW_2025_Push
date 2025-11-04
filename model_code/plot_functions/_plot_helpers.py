import matplotlib.patches as patches


#%% FUNCTIONS
def draw_hor_dim_line(ax,
                      point1,
                      point2,
                      label,
                      va = 'bottom',fontsize=30,
                      rotation=90,lw=2,offset=0):
    '''
    Draws a horizontal dimension line with arrows from point1 (x1,y1) to 
    point2 (x2,y2), with a label at the midpoint. Default anchoring is
    at the bottom.
    '''
    
    # Extract points
    x1,y1 = point1
    x2,y2 = point2
    
    # Calculate midpoing of line
    xm = (x1+x2)/2
    # Make arrowheaded line
    ax.annotate("", xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', lw=lw))

    # Add text
    text_obj = ax.text(xm,y1+offset,label,fontsize=fontsize,
            verticalalignment=va,horizontalalignment='center')
    
    return text_obj

def draw_ver_dim_line(ax,
                      point1,
                      point2,
                      label,
                      ha = 'right',
                      fontsize=30,
                      rotation=90,lw=2,offset=0,
                      va = 'center'):
    
    '''
    Draws a VERTICAL dimension line with arrows from point1 (x1,y1) to 
    point2 (x2,y2), with a label at the midpoint. Default anchoring is
    at the right of the label
    '''
    
    # Extract points
    x1,y1 = point1
    x2,y2 = point2
    
    # Calculate midpoing of line
    ym = (y1+y2)/2
    # Make arrowheaded line
    ax.annotate("", xy=(x1, y1), xytext=(x2, y2),
                arrowprops=dict(arrowstyle='<->', lw=lw))

    # Add text
    text_obj = ax.text(x1+offset,ym,label,fontsize=fontsize,
            verticalalignment=va,horizontalalignment=ha,rotation=rotation)
    
    return text_obj

def draw_c_line(ax,point1,point2,ls='--',lw=3,color='black'):
    '''
    Draws a dotted constructing line from point 1 to point 2
    '''
    
    # Extract points
    x1,y1 = point1
    x2,y2 = point2
    
    # Make line
    ax.plot([x1,x2],[y1,y2],ls=ls,lw=lw,color=color)
    
    return


def fill(ax,x_l,x_r,y_lo,y_hi,color,label,fontsize=30,alpha=0.5):
    '''
    Fills a region with the specified color between [x_l,x_r] in the x
    and [y_lo,y_hi] in the y at 50% transparency, with a label in the middle
    '''
    
    
    ax.fill_between([x_l,x_r],    
                    [y_lo,y_lo],      
                    [y_hi,y_hi],
                    color=color,alpha=alpha)  
    # Text
    x_m = (x_l+x_r)/2
    y_m = (y_lo + y_hi)/2
    ax.text(x_m,y_m,
            label,
            fontsize=fontsize,
            verticalalignment='center',
            horizontalalignment='center')
    return

def draw_hor_dim_line_outside(ax,
                              point1,
                              point2,
                              label,
                              va='bottom', fontsize=30,
                              rotation=0, lw=2, offset=0, offset_x=0.02):
    '''
    Draws a horizontal dimension line with *outside arrows* pointing inward
    from point1 (x1,y1) to point2 (x2,y2), with a label at the right end.
    '''
    
    # Extract points
    x1, y1 = point1
    x2, y2 = point2

    # Parameters for arrows
    gap = 0.01
    ext = 0.06
    
    # Left arrow (points right, inward)
    ax.annotate("", xy=(x1 + gap, y1), xytext=(x1 - ext, y1),
                arrowprops=dict(arrowstyle="->", lw=lw, color='k'))
    
    # Right arrow (points left, inward)
    ax.annotate("", xy=(x2 - gap, y1), xytext=(x2 + ext, y1),
                arrowprops=dict(arrowstyle="->", lw=lw, color='k'))
    
    # Add text at the right end
    text_obj = ax.text(x2 + ext + offset_x, y1 + offset, label,
                       fontsize=fontsize, verticalalignment=va,
                       horizontalalignment='left', rotation=rotation)
    
    return text_obj
