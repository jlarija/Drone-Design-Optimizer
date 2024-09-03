"""
Author: @jlarija
This code serves to write the coordinates of the airfoil of the propeller to a form that can be directly
imported into CATIA as the final blade. Having dowloaded the coordinates of the relevant airfoil (in this
case, CLARK Y) then the code transforms the coordinate with the twist, pitch and y displacement to fill
each blade's section. The results are written to a CSV file to be imported to CATIA.
"""

import csv
import os

import pandas as pd
import numpy as np


class CoordinatesOperations:

    def __init__(self, file):

        """Input the csv file for which you want to read the airfoil coordinates"""

        self.file = file

    def read_coord_from_file(self):
        """Read CSV file coordinates and split into x,y,z tabs. Airfoil is in zx plane in CATIA."""

        # required tabs
        rows = []
        xcoord = []
        zcoord = []

        airfoil = open(self.file, 'r')

        # Read all the rows
        for row in csv.reader(airfoil):
            rows.append(row)

        # Split coordinates

        for n in range(len(rows)):
            try:
                xcoord.append(float(rows[n][0]))
                zcoord.append(float(rows[n][1]))

            except ValueError:
                xcoord.append(0)

        xcoord = list(filter(None, xcoord))
        zcoord = list(filter(None, zcoord))
        xcoord.insert(0,
                      0)  # only for x cause for some reason the first vlaue ends up being "0?' otherwise #pythonthings
        xcoord.insert(61, 0)
        zcoord.insert(0, 0)  # first coordinate
        zcoord.insert(61, 0)
        xcoord = np.array(xcoord)
        zcoord = np.array(zcoord)

        return xcoord, zcoord

    def get_propeller_geometry(self, APC_prop_txt):
        """Input file with chord pitch etc """

        airfoil_data = open(APC_prop_txt)
        lines = airfoil_data.readlines()
        airfoil_data.close()

        columns = []
        radial_station = []
        chord = []
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

        final_cols = columns[20:53]

        # separate the ones you need (and convert to SI units)
        tablist = [radial_station, chord, pitch, sweep, twist, zhigh]

        for m in range(len(final_cols)):
            radial_station.append(float(final_cols[m][0]))
            chord.append(float(final_cols[m][1]))
            pitch.append(float(final_cols[m][2]))
            sweep.append(float(final_cols[m][5]))
            twist.append(float(final_cols[m][7]))
            zhigh.append(float(final_cols[m][10]))

        # convert to arrays and multiply to SI units
        radial_station = np.array(radial_station) * 0.0254 * 10 ** (3)  # using mm so it's CATIA real size
        chord = np.array(chord) * 0.0254 * 10 ** (3)
        sweep = np.array(sweep) * 0.0254 * 10 ** (3)
        zhigh = np.array(zhigh) * 0.0254 * 10 ** (3)

        return radial_station, chord, pitch, sweep, zhigh, twist

    def transform_coord(self, file):
        ycoord = []
        xcoord, zcoord = self.read_coord_from_file()

        airfoil_stations = {}

        df =  pd.read_fwf(file, skiprows = 1, index_col=False, names=['r/R', 'c/R', 'beta', 'sweep', 'zhigh'])
        radial_station, chord, sweep, zhigh, twist = df['r/R'], df['c/R'], df['sweep'], df['zhigh'], df['beta']

        for station in radial_station:
            airfoil_stations[" - ".join(['station', str(np.round(station, 4))])] = {}
            airfoil_stations[" - ".join(['station', str(np.round(station, 4))])]['x'] = {}
            airfoil_stations[" - ".join(['station', str(np.round(station, 4))])]['y'] = {}
            airfoil_stations[" - ".join(['station', str(np.round(station, 4))])]['z'] = {}

        # airfoil 1 is just the airfoil times the chord
        keylist = list(airfoil_stations.keys())

        for j in range(len(keylist)):
            airfoil_stations[str(keylist[j])]['x'] = (xcoord * chord[j]) / np.cos(np.deg2rad(twist[j])) + sweep[j]
            airfoil_stations[str(keylist[j])]['y'] = np.full(len(xcoord), radial_station[j], dtype=float)
            airfoil_stations[str(keylist[j])]['z'] = (zcoord * chord[j]) / np.cos(np.deg2rad(twist[j])) + (
                        zhigh[j] - np.max(zcoord))

        return airfoil_stations

    def join_files(self, directory):

        columns = []

        for file in os.listdir(directory):
            x  =[]
            y = []
            z = []

            current_file = open(file, 'r')
            lines = current_file.readlines()
            current_file.close()
            for line in lines:
                if len(line.strip()) > 0:
                    columns_0 = line.split(" ")

                    columns_1 = list(filter(None, columns_0))

                    for i in range(len(columns_1)):
                        columns_1[i] = columns_1[i].strip()

                    columns.append(columns_1)

            for i in range(len(columns)):
                x.append(columns[0])
                y.append(columns[1])
                z.append(columns[2])

        #now you need to create one file and then input the commands of the curves before opening the
        #next file and doing the

        return

if __name__ == '__main__':

    file = 'CLARKY.csv'
    airfoil = CoordinatesOperations(file)
    x, z = airfoil.read_coord_from_file()

    airfoil_sections = airfoil.transform_coord('catia_geom.txt')

    # now open the file for writing the coordinates
    field_names = list(airfoil_sections.keys())

    rows_to_write = []
    command_1 = ['StartLoft']
    command_2 = ['StartCurve']
    command_3 = ['EndCurve']
    command_4 = ['EndLoft']
    command_5 = ['End']

    with open('prop_1.csv', 'w', encoding='UTF8', newline='') as final_file:
        writer = csv.writer(final_file)  # if by chance you have the file open then python denies you permission
        writer.writerow(command_1)
        writer.writerow(command_2)
        for key in field_names:

            rows_to_write = []  # empty it each time and add onto what you aleady have
            x_write = airfoil_sections[str(key)]['x']
            y_write = airfoil_sections[str(key)]['y']
            z_write = airfoil_sections[str(key)]['z']

            for i in range(len(x_write)):
                rows_to_write.append([x_write[i], y_write[i], z_write[i]])

            # now for ease of spline building you want to reverse the second half of x only (z shold be fine)

            writer.writerows(rows_to_write)

            writer.writerow(command_3)
            writer.writerow(command_2)

        writer.writerow(command_4)
        writer.writerow(command_5)

    directory = r'C:\Users\jlari\Documents\GitHub\DSE-LARES-HIVE-Resources\src_lares\propulsion\rotor\CRotor' \
                r'\CRotor755es13_win32\bin\01 cad_blades'