import numpy as np
import pandas as pd

class AeroData:
    def __init__(self, df):
        self.df = df

    def cl_0(self):
        return min(self.df['CL'], key=lambda x: abs(x - 0), default=0)  # find closest value to 0

    def cl_alpha(self):
        return (self.df['CL'][30] - self.df['CL'][28]) / (np.deg2rad(self.df['alpha'][30] - self.df['alpha'][28]))  # UNIT: 1/deg

    def cl_alpha_stall(self):
        return (self.df['CL'][65] - self.df['CL'][60]) / (np.deg2rad(self.df['alpha'][65] - self.df['alpha'][60]))  # UNIT: 1/deg

    def cl_max_min(self):
        return np.min(self.df['CL']), np.max(self.df['CL'])

    def cl_increment_stall(self):
        stall = self.df['CL'][self.df['CL'] == np.min(self.df['CL'])].index
        idx = int(stall[0]) - 1
        cl_before = self.df['CL'][idx]
        return cl_before

    def cd_min(self):
        min_index = self.df['CD'][self.df['CD'] == np.min(self.df['CD'])].index
        idx = int(min_index[0])
        return np.min(self.df['CD']), self.df['CL'][idx]

    def dcd_cl2(self):
        cl2 = self.df['CL'] ** 2
        return (self.df['CD'][30] - self.df['CD'][26]) / (cl2[30] - cl2[26])

def read_airfoil(file):
    df = pd.read_fwf(file, skiprows=11, index_col=False, names= ['alpha','CL','CD','CDp','CM','Top_Xtr','Bot_Xtr'])
    return df

#just me needing the aero data
df = read_airfoil('naca_4412.txt')
airfoil_class = AeroData(df)
print("Requested aero data:"
      "CL_0 =", airfoil_class.cl_0(), '\n',
      "CL_alpha", airfoil_class.cl_alpha(), '\n',
      "CL_alpha_stall", airfoil_class.cl_alpha_stall(), "\n",
      'CL_max, CL_min', airfoil_class.cl_max_min()[0],airfoil_class.cl_max_min()[1], '\n',
      'cl_incr_stall', airfoil_class.cl_increment_stall(), '\n',
      'CD_min', airfoil_class.cd_min()[0], 'Correspondind CL:', airfoil_class.cd_min()[1], '\n',
      'DcdDcl2', airfoil_class.dcd_cl2())
