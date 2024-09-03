import pickle
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.interpolate import griddata

with open('CP_data.pkl', 'rb') as save_cp_file:
    cp_dict = pickle.load(save_cp_file)
with open('r_R_list', 'rb') as save_r_R:
    r_R = pickle.load(save_r_R)
with open('aoa_list', 'rb') as save_aoa:
    aoa = pickle.load(save_aoa)

aoa = [float(i) for i in aoa]
aoa = np.round(aoa,2)
r_R = [float(j) for j in r_R]
r_R = np.round(r_R,2)

x_coord = []
y_coord = []
z_coord = []

i = 0
#generate the coordinates x,y,z for each;
for key in cp_dict.keys():
    x_coord.append(cp_dict[key]['x/c'])
    z_coord.append(cp_dict[key]['CP'])

    #the y has to be the r_R multiplied by how many points each cp graph has
    y_coord_values = np.full(len(cp_dict[key]['x/c']), r_R[i])
    y_coord.append(y_coord_values)
    i+=1


x_coord = np.asarray(x_coord) #flatten the list
x_coord = np.ravel(np.sort(x_coord)[::-1])
x_series = pd.Series(x_coord)
y_coord = np.ravel(y_coord)#flatten the list
y_series = pd.Series(y_coord)
z_coord = np.asarray(z_coord)
z_coord = np.ravel(np.sort(z_coord))
z_series = pd.Series(z_coord)
df = {'x/c':x_series, 'r/R': y_series, 'CP':z_series}

#first plot option:
xi = np.linspace(min(df['x/c']), max(df['x/c']))
yi = np.linspace(min(df['r/R']), max(df['r/R']))
x_grid, y_grid = np.meshgrid(xi,yi)
z_grid = griddata((df['x/c'],df['r/R']),df['CP'],(x_grid,y_grid),method='nearest')

fig = go.Figure(go.Surface(x=x_grid,y=y_grid,z=z_grid,showlegend=False, colorscale='blues'))

fig.update_layout(scene = dict(
                    xaxis_title='x/c',
                    yaxis_title='r/R',
                    zaxis_title='CP'),
                    title='CP along blade span')

fig.show()
