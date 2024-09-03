import matplotlib.pyplot as plt

from Generate_Blade_CADCoords import CoordinatesOperations

import pandas as pd
import numpy as np
import csv

#plot the airfoil and add the extra thickness in the front for catia
airfoil = 'CLARKY.csv'
get_coords = CoordinatesOperations(airfoil)
x , z = get_coords.read_coord_from_file()

# plot airfoil to see
fig, ax = plt.subplots()
# dont mind the line in the middle it's because it joins back
ax.plot(x, z, label = 'Clark Y Normal', color = '#6ebbd5')
plt.xlim(-0.2,1.2)
plt.ylim(-0.2,0.2)
plt.show()


