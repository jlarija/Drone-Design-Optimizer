import numpy as np
import pandas as pd


# first read the coordinates from the file

def get_propeller_geometry(APC_prop_txt, R):
    """Input file with chord pitch etc """

    airfoil_data = open(APC_prop_txt)
    lines = airfoil_data.readlines()
    airfoil_data.close()

    columns = []
    r_R = []
    c_R = []
    pitch = []
    sweep = []
    twist = []  # NOT SURE WHICH ONE I NEED IF PITCH OR TWIST
    zhigh = []

    for line in lines:
        if len(line.strip()) > 0:
            columns_0 = line.split(" ")

            columns_1 = list(filter(None, columns_0))

            for i in range(len(columns_1)):
                columns_1[i] = columns_1[i].strip()

            columns.append(columns_1)

    final_cols = columns[23:59]

    for m in range(len(final_cols)):
        r_R.append(float(final_cols[m][0]))
        c_R.append(float(final_cols[m][1]))
        pitch.append(float(final_cols[m][2]))
        sweep.append(float(final_cols[m][5]))
        twist.append(float(final_cols[m][7]))
        zhigh.append(float(final_cols[m][10]))

    # convert to arrays and multiply to SI units
    r_R = np.array(r_R) / R  # * 0.0254 * 10 ** (3)  # using mm so it's CATIA real size
    c_R = np.array(c_R) / R  # * 0.0254 * 10 ** (3)
    sweep = np.array(sweep)  # * 0.0254 * 10 ** (3)
    zhigh = np.array(zhigh)  # * 0.0254 * 10 ** (3)

    return r_R, c_R, pitch, sweep, zhigh, twist


r_R, c_R, pitch, sweep, zhigh, twist = get_propeller_geometry('15X8-PERF.PE1', 7.5)
r_R = np.round(r_R, 2)
data_df = {'r/R': r_R, 'c/R': c_R, 'pitch': pitch, 'sweep': sweep, 'zhigh': zhigh, 'twist': twist}
df = pd.DataFrame(data=data_df)

write_data = False
# write data in a document
if write_data:
    with open('apc_geometry.txt', 'w') as f:
        df_asstring = df.to_string(header=True, index=False)
        f.writelines(df_asstring)
        f.close()

# Now make a final file with the propeller data
write_final = True
xrotor_data = pd.read_fwf('changedAPC17x12RPM2500c_incr0.3at4.0.txt', skiprows=17, index_col=False,
                          names=['i', 'r/R', 'c/R', 'beta', 'CL', 'CD', ' REx10^3', 'Mach', 'effi', 'effp', 'na.u/U'])
del xrotor_data['i']

if write_final:
    data_apc = pd.read_fwf('apc_geometry.txt', index_col=False, skiprows=1,
                           names=['r/R', 'c/R', 'pitch', 'sweep', 'zhigh', 'twist'])

    final_apc = data_apc.filter(['sweep', 'zhigh'], axis=1)
    final_apc.reset_index(drop=True, inplace=True)
    xrotor_df = xrotor_data.filter(['r/R', 'c/R', 'beta'], axis=1)
    xrotor_df.reset_index(drop=True, inplace=True)
    final_df = xrotor_df.join(final_apc)

    final_filename = 'prop_cad_f.txt'
    with open('catia_geom.txt', 'w') as file:
        df_string = final_df.to_string(header=True, index=False)
        file.writelines(df_string)
        file.close()

