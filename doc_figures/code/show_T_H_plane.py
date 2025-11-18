import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import brentq
import pandas as pd

def linear_dispersion_by_roots(T,h):
    '''
    Solve the linear dispersion relation given period `T` and depth `h`
    using iterative root finding
    '''
    # Define orbital period
    sigma = 2 * np.pi / T
    # Define gravity
    g = 9.81

    # Definition of the linear dispersion relation
    def disp_relation(k):
        return sigma**2 - g * k * np.tanh(k * h)
    
    # Linear root finding
    k = brentq(disp_relation, 1e-12, 10)
    L = 2 * np.pi / k

    return k,L

# Example ranges
T_values = np.arange(2,17)
h_values = np.arange(1,21)

rows = []
for T in T_values:
    for h in h_values:
        k, L = linear_dispersion_by_roots(T, h)
        kh = k * h
        rows.append({"T": T, "h": h, "kh": kh, "L": L})

df = pd.DataFrame(rows)
df = df[(df['kh']<np.pi) & (df['L']/60>df['h']/15)]
df = df[(df['kh']<np.pi) & (df['L']/70>df['h']/15)]


def get_limit_T_axis(factor,h):
    L = factor*h
    sigma = np.sqrt(9.81*(2*np.pi/L)*np.tanh((2*np.pi/L)*h))
    T = 2*np.pi/sigma
    return T




T_lo, T_hi = 0,17
h_vals = np.linspace(0, 21, 500)


# Get the limits, construct out to end
T_val_deep = get_limit_T_axis(2,h_vals)
T_val_70 = get_limit_T_axis(70/15,h_vals)
T_val_60 = get_limit_T_axis(60/15,h_vals)


upper_line = h_vals[-1]*np.ones(len(h_vals))
lower_line =  h_vals[0]*np.ones(len(h_vals))



#%%
fig,ax = plt.subplots(dpi=300,figsize=(8,4))
# Deep Water Limit 
ax.plot(T_val_deep,h_vals,lw=2,color='red')
# L/60 = h/15 line
ax.plot(T_val_60,h_vals,lw=2,color='orange')
# L/70 = h/15 line
ax.plot(T_val_70,h_vals,lw=2,color='purple')

# Deep Water Region
ax.fill_betweenx(h_vals, 
                 T_lo, 
                 T_val_deep, 
                 color='red', alpha=0.3, label='$kh>\\pi$')

# Region between deep water and L/60 = h/15 line
ax.fill_betweenx(h_vals, 
                 T_val_deep, 
                 T_val_60, 
                 where=T_val_deep < T_val_60, 
                 color='orange', alpha=0.3, label='$\\frac{\lambda}{60}>\\frac{h}{15}$')
# Region between L/70 = h/15 and L/60 = h/15 line
ax.fill_betweenx(h_vals, 
                 T_val_70, 
                 T_val_60, 
                 where=T_val_60 < T_val_70, 
                 color='purple', alpha=0.3, label='$\\frac{\lambda}{70}>\\frac{h}{15}$')

# Valid Domain Area
ax.fill_betweenx(h_vals, 
                 T_val_70, 
                 T_hi, 
                 color='grey', alpha=0.3, label='Study\nDomain')


ax.scatter(df['T'],df['h'],zorder=5,marker='s',c='black',s=20)
ax.legend(fancybox=False,framealpha=1)
ax.grid()
ax.axvline(8.5,color='green',ls='--',lw=2)
df_small = df[df['T']<8.5]
ax.scatter(df_small['T'],df_small['h'],zorder=5,marker='o',c='green',s=4)
ax.set_xticks(range(1, 17))
ax.set_yticks(range(1, 21))
ax.set_xlim(0,16.5)
ax.set_ylim(0.5,20.5)
ax.set_xlabel('Period [s]')
ax.set_ylabel('Depth [m]')
ax.set_title(f'Valid Test Points in the $T-h$ Plane (n={len(df)})\n (n={len(df_small)}) for $T \leq 8$')
fig.savefig('../png/216_points.png', bbox_inches="tight")



#%%
'''
df = df[df['T']<8.5]
fig,ax = plt.subplots(dpi=300,figsize=(8,4))
# Deep Water Limit 
ax.plot(T_val_deep,h_vals,lw=2,color='red')
# L/60 = h/15 line
ax.plot(T_val_60,h_vals,lw=2,color='orange')
# L/70 = h/15 line
ax.plot(T_val_70,h_vals,lw=2,color='purple')

# Deep Water Region
ax.fill_betweenx(h_vals, 
                 T_lo, 
                 T_val_deep, 
                 color='red', alpha=0.3, label='$kh>\\pi$')

# Region between deep water and L/60 = h/15 line
ax.fill_betweenx(h_vals, 
                 T_val_deep, 
                 T_val_60, 
                 where=T_val_deep < T_val_60, 
                 color='orange', alpha=0.3, label='$\\frac{\lambda}{60}>\\frac{h}{15}$')
# Region between L/70 = h/15 and L/60 = h/15 line
ax.fill_betweenx(h_vals, 
                 T_val_70, 
                 T_val_60, 
                 where=T_val_60 < T_val_70, 
                 color='purple', alpha=0.3, label='$\\frac{\lambda}{70}>\\frac{h}{15}$')

# Valid Domain Area
ax.fill_betweenx(h_vals, 
                 T_val_70, 
                 T_hi, 
                 color='grey', alpha=0.3, label='Study\nDomain')


ax.scatter(df['T'],df['h'],zorder=5,marker='s',c='black',s=20)
ax.legend(fancybox=False,framealpha=1)
ax.grid()
ax.set_xticks(range(1, 17))
ax.set_yticks(range(1, 21))
ax.set_xlim(0,8.5)
ax.set_ylim(0.5,20.5)
ax.set_xlabel('Period [s]')
ax.set_ylabel('Depth [m]')
ax.set_title(f'Valid Test Points in the $T-h$ Plane (n={len(df)}) (restricted T<=8)')
fig.savefig('../png/56_points.png', bbox_inches="tight")
'''