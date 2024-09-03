import numpy as np
import pandas as pd

def read_file(file):
    '''Why not using read_fwf? because python would return nan'''

    r_R = []
    c_R = []
    beta = []

    file_1 = open(file, 'r')
    lines = file_1.readlines()
    del lines[:3]
    for line in lines:
        split_lines = line.split()
        r_R.append(np.round(float(split_lines[0]),2))
        c_R.append(np.round(float(split_lines[1]), 2))
        beta.append(np.round(float(split_lines[2]), 2))

    df_data = {'r/R': np.asarray(r_R), 'chord': np.asarray(c_R), 'beta': np.asarray(beta)}
    df = pd.DataFrame(data=df_data, columns = ['r/R', 'chord', 'beta'])
    return df

def df_operations(df, savefile_name):

    df['c/R'] = df['chord']*(10**(-3)) / (df['r/R']*29*0.0254)
    del df['chord']

    final_data = {'r/R': df['r/R'], 'c/R': df['c/R'], 'beta': df['beta']}
    final_df = pd.DataFrame(data=final_data, columns = ['r/R', 'c/R', 'beta'])

    final_df = final_df.round(2)

    with open(savefile_name, 'w') as f:
        df_asstring =  final_df.to_string(header = True, index = False)
        f.write(df_asstring)
        f.close()

    return final_df

if __name__ == '__main__':
    file = 'T-Motor 29'

    savefile = 'TMotor29_final.txt'

    read_data = read_file(file)
    rewrite_file = df_operations(read_data, savefile)