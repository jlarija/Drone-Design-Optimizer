import os
import subprocess
import pandas as pd


class RunXrotor:

    def __init__(self, runfile, rpm, radius, savefilename):
        if os.name == 'nt':
            self.path = r'C:\Users\jlari\Documents\GitHub\DSE-LARES-HIVE-Resources\src_lares\propulsion\rotor\CRotor' \
                        r'\CRotor755es13_win32\bin\xrotor.exe'
        else:
            self.path = '/home/jlarija/Desktop/Xrotor/bin/xrotor'
        self.runfile = runfile
        self.rpm = rpm
        self.radius = radius
        self.savename = savefilename

    def input_tostring(self):
        df = pd.read_fwf(self.runfile, skiprows=1, index_col=False, names=['r/R', 'c/R', 'beta'])
        n_stations = len(df)
        print(n_stations)
        df['Press Enter'] = '\n'  # add enter sign after every line

        df_as_string = df.to_string(header=False, index=False)

        return df_as_string, str(n_stations)

    def run_xrotor(self):
        ps = subprocess.Popen(self.path, shell=True, stdin=subprocess.PIPE,
                              text=True)

        ps.communicate(os.linesep.join(['ARBI', '2', '1',
                                        str(self.radius * 0.0254),
                                        '0.032385', self.input_tostring()[1], self.input_tostring()[0], 'n', 'OPER',
                                        'RPM', str(self.rpm), 'WRIT', str(self.savename), 'SAVE latest_rotor'
                                        ]))
        return 'Analysis Terminated.'
