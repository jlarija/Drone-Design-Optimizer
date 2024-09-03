from matplotlib import pyplot as plt
import pandas as pd
import seaborn as sns

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

class ModifyGeometry:

    def __init__(self, R, og_file):
        self.R = R
        self.og_file = og_file

    def og_geometry(self):
        df = pd.read_fwf(self.og_file, skiprows=1, index_col=False, names=['r/R', 'c/R', 'beta'])

        c_halves = df['c/R'] / 2
        c_value = c_halves * self.R
        r_value = df['r/R'] * self.R

        d_pos = {'Chord [in]': c_value, 'Radius [in]': r_value}
        df_positives = pd.DataFrame(data=d_pos, columns=['Chord [in]', 'Radius [in]'])

        d_neg = {'-c/2': -c_value, 'r/R': r_value}
        df_negatives = pd.DataFrame(data=d_neg, columns=['-c/2', 'r/R'])
        return df_positives, df_negatives, df

    def modified_geometry(self, r_start, c_incr):
        """
        r_start    : r/R coordinate to begin increasing the chord
        c_incr    : desired increase in chord at r/R = 1
        R        : radius of the propeller [in]
        """
        init_geom = self.og_geometry()[0]

        c = init_geom['Chord [in]']
        radius = init_geom['Radius [in]']

        d_pos_new = {'Chord [in]': c, 'Radius [in]': radius}
        d_neg_new = {'Chord [in]': -c, 'Radius [in]': radius}

        df_pos_new = pd.DataFrame(data=d_pos_new, columns=['Chord [in]', 'Radius [in]'])
        df_neg_new = pd.DataFrame(data=d_neg_new, columns=['Chord [in]', 'Radius [in]'])

        # increase is done by defining a line y = mx + c such that @ start, y = 0, @ r/R = 1 y = R_val
        m = c_incr / (df_pos_new['Radius [in]'].iloc[-1] - r_start)

        c_fact = c_incr * r_start / (df_pos_new['Radius [in]'].iloc[-1] - r_start)

        for i in range(len(radius)):
            if radius[i] > r_start:
                df_pos_new.loc[i, 'Chord [in]'] = c[i] + m*radius[i] - c_fact

                df_neg_new.loc[i, 'Chord [in]'] = -c[i] - m*radius[i] + c_fact

        # for writing in the txt file, the coordinates have to be converted back to their original format

        c_R = df_pos_new['Chord [in]'] * (2 / self.R)
        r_R = df_pos_new['Radius [in]'] / self.R
        beta = self.og_geometry()[2]['beta'] #keep beta the same as before as no other knowledge for now

        data_writetofile = {'r/R': r_R, 'c/R': c_R, 'beta': beta}
        df_writetofile = pd.DataFrame(data=data_writetofile, columns = ['r/R', 'c/R', 'beta'])

        filename = ''.join(['mod_prop/', 'modified_chord', self.og_file[8:16], '.txt'])

        with open(filename, 'w') as f:
            df_as_string = df_writetofile.to_string(header=True, index=False)
            f.write(df_as_string)
            f.close()

        return df_pos_new, df_neg_new, df_writetofile, filename

    def plot_geometry(self, r_start, c_incr):

        #only one modification at a time possible for now

        fig, ax = plt.subplots()
        sns.lineplot(x='Radius [in]', y='Chord [in]', data=self.og_geometry()[0], color='black', label='Original')
        sns.lineplot(x='r/R', y='-c/2', data=self.og_geometry()[1], color='black')
        sns.lineplot(x='Radius [in]', y='Chord [in]', data=self.modified_geometry(r_start, c_incr)[0], color='red',
                     label='Modified', ls='dashed')
        sns.lineplot(x='Radius [in]', y='Chord [in]', data=self.modified_geometry(r_start, c_incr)[1], color='red',
                     ls='dashed')
        ax.grid(ls=':')
        plt.legend()

        return plt.draw()


if __name__ == '__main__':
    new_rotor = ModifyGeometry(22/2, 'og_prop/APC17x12.txt')
    new_prop = new_rotor.modified_geometry(4,0.25)[2]
    save_file = new_prop.to_string(header=True, index=False)

    with open('final_prop_geom.txt', 'w') as f:
        f.write(save_file)
        f.close()





