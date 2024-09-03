"""
Author: @jlarija
This part of the code first converts the .DAT files into .CSV and then reads and organises the data into a dictionary.
The first functions are used for this conversion, so if the files already converted into CSV have been downloaded from
GitHub, there is no need to run them. I had to since I made the conversion.
A bit about the files: each file is a different propeller named as radius x pitch [in] and it contains a range of RPMs,
for which the velocity, CT, CP, adv. ratio, torque, thrust and power are available.
"""

import csv
import os
import pickle
import shutil

import numpy as np


def get_RPM_ranges():
    """This function reads the RPM ranges for each of the propeller files, in order to determine the range of
    data to analyse. """

    prop_name = []
    R1 = []
    R2 = []

    directory = os.getcwd()
    file_to_read = open(''.join([str(directory), '\PER2_RPMRANGE.DAT']))
    lines = file_to_read.readlines()
    file_to_read.close()

    for line in lines:
        if len(line.strip()) > 0:
            columns_0 = line.split(" ")

            columns_1 = list(filter(None, columns_0))

            for i in range(len(columns_1)):
                columns_1[i] = columns_1[i].strip()

            prop_name.append(columns_1[0])
            R1.append(columns_1[1])
            R2.append(columns_1[2])

    R1 = np.asarray(R1)
    R2 = np.asarray(R2)

    return prop_name, R1, R2


def save_files_to_Excel():
    """DAT files are hard to read with pandas due to inconsistent spacing. Converting all of them to an EXCEL format
    and saving them to a different directory (for better organisation) is what this function does. """

    dir_ = '\\'.join([os.getcwd(), 'PERFILES2'])

    for file in os.listdir(dir_):

        file_to_read = '\\'.join([os.getcwd(), 'PERFILES2', str(file)])  # already has .dat in it
        datContent = [i.strip().split() for i in open(file_to_read).readlines()]

        # print("Currently at file", file_to_read)
        # write it as a new CSV file

        filename_ascsv = '\\'.join([str(os.getcwd()), 'CSV_of_PERFILES2', str(file).replace('.dat', '.csv')])

        with open(filename_ascsv, "w") as f:
            writer = csv.writer(f)
            writer.writerows(datContent)

        final_csv_name = str(filename_ascsv).replace('.csv', 'final.csv')

        if os.path.isfile(final_csv_name):  # if file already exists it will not write
            continue
        else:
            with open(filename_ascsv) as in_file:
                with open(final_csv_name, 'w') as out_file:
                    writer = csv.writer(out_file)
                    for row in csv.reader(in_file):
                        if any(field.strip() for field in row):
                            writer.writerow(row)

    return 'Files have been converted to Excel'


def move_files_to_directory():
    """It was annoying to have a duplicate of every CSV (since there is the "final" with consistent spacing
    and the original one) so I moved them to a different directory. Only run if that's what you have to do, but probably
    unnecessary if files in CSV are downloaded from Git."""

    original_directory = '\\'.join([os.getcwd(), 'CSV_of_PERFILES2'])
    target_directory = '\\'.join([os.getcwd(), 'Intermediate_PERFILES'])
    files_to_move = []
    for file in os.listdir(original_directory):

        if 'final' in str(file):
            continue

        else:
            files_to_move.append(str(file))

    for element in files_to_move:

        path_to_move = '\\'.join([str(os.getcwd()), 'CSV_of_PERFILES2', element])

        if os.path.isfile(element):
            continue

        else:
            shutil.move(path_to_move, target_directory)

    return 'Selected files were moved'


def check_name(prop_lists, filename):
    start = 0
    stop_first = 4
    if len(filename) > stop_first:
        file_1 = filename[0: start:] + filename[stop_first + 1::]

    name_to_check = file_1[:-9:]

    indx = [i for i in enumerate(prop_lists) if name_to_check in i][0][
        0]  # now this gives the index in the filelist to get the right rpm range
    return indx


def store_data_in_dictionary(final_files_directory):
    """Finally, this function reads the final CSV files and stores the data in a dictionary"""

    for file in os.listdir(final_files_directory):

        # initialise index to pair RPM ranges
        csvfilearray = []  # re-initialise array for a new file. It should be fine since it makes another key in the dictionary and the other ones should be kept as the name changes
        filename = '\\'.join([str(final_files_directory), str(file)])
        csvfile = open(filename, 'r')  # open the file

        for row in csv.reader(csvfile):  # take a row and append it to the tab
            csvfilearray.append(row)

        rows = [x for x in csvfilearray if x != []]  # for every row delete the empty rows (because the csv file is)
        rows = [x for x in rows if x != ['', '', '', '', '', '', '', '', '', '', '', '', '', '']]
        csvfile.close()

        index_for_RPM = check_name(get_RPM_ranges()[0], file)  # same index to be used for RPM

        all_propellers[str(get_RPM_ranges()[0][index_for_RPM])] = {}

        R1 = get_RPM_ranges()[1][index_for_RPM]
        R2 = get_RPM_ranges()[2][index_for_RPM]

        ranger = range(int(R1), int(R2), 1000)  # Range adapted depending on file. In steps of 1000

        if str(rows[2][0]) == 'DEFINITIONS:':
            a = 8
        else:
            a = 13

        for n in range(len(ranger)):  # for each RPM value #this is a loop that goes inside the file

            rpm_row_indeces = a + n * 33  # should be the same for every file, checked

            velocity = []  # if you empty it each time it can be fine if it's in the same loop. it does not empty the dictionary
            power = []
            thrust = []
            torque = []

            # issue is with m
            m = int(rpm_row_indeces) + 3  # so initially 11, 8+33+3 etc etc

            for k in range(0, 30):

                if m < len(rows) and len(rows[m]) > 7:  # some files have a NaN so then the math below cannot be done

                    velocity.append(rows[m][0])
                    power.append(rows[m][5])
                    torque.append(rows[m][6])
                    thrust.append(rows[m][7])

                    m += 1

                else:

                    m += 1

            # now you appended everything so you can convert it

            velocity = np.round(np.asarray(velocity, dtype=float) * 0.44704, 2)
            power = np.round(np.asarray(power, dtype=float) * 745.7, 2)
            torque = np.round(np.asarray(torque, dtype=float) * 0.11, 2)
            thrust = np.round(np.asarray(thrust, dtype=float) * 4.44822, 2)

            rpm_count = ranger[0] + n * 1000  # whatever the beginning of the range is, this is the first value

            prop_name = get_RPM_ranges()[0][int(index_for_RPM)]

            all_propellers[str(prop_name)][' '.join(['RPM', str(rpm_count)])] = {}
            all_propellers[str(prop_name)][' '.join(['RPM', str(rpm_count)])]['v'] = velocity
            all_propellers[str(prop_name)][' '.join(['RPM', str(rpm_count)])]['P'] = power
            all_propellers[str(prop_name)][' '.join(['RPM', str(rpm_count)])]['T'] = thrust
            all_propellers[str(prop_name)][' '.join(['RPM', str(rpm_count)])]['M'] = torque

        print('Analysed file', file)

    return 'Done! Total files analysed: ', len(all_propellers)


def get_propellers_atvelocity(v_sizing, input_propellerdict, final_dict):
    for outside_keys in input_propellerdict.keys():  # iterate through propeller names that got into dictionary

        final_dict[str(outside_keys)] = {}  # Must create the dictionaries as well

        for inside_key in input_propellerdict[
            str(outside_keys)].keys():  # Iterate through all RPMs of the propellers

            final_dict[str(outside_keys)][
                str(inside_key)] = {}  # Must create the dictionaries as well (will make it empty tho)

            # ValueError: min() arg is an empty sequence: basically if you pass an empty sequence it won't work. so if all_propellers[str(outside_keys)][str(inside_key)]['v'] = []. Some are empty cause they were NaN in the dat file

            closest_velocity = min(input_propellerdict[str(outside_keys)][str(inside_key)]['v'],
                                   key=lambda x: abs(x - v_sizing),
                                   default=0)  # Find the closest velocity to the sizing velocity among the data set

            if abs(closest_velocity - v_sizing) < 0.5:

                get_index = np.where(
                    input_propellerdict[str(outside_keys)][str(inside_key)]['v'] == closest_velocity)

                actual_index = get_index[0]  # np.where returns an array

                corr_thrust = input_propellerdict[str(outside_keys)][str(inside_key)]['T'][actual_index]
                corr_power = input_propellerdict[str(outside_keys)][str(inside_key)]['P'][actual_index]
                corr_torque = input_propellerdict[str(outside_keys)][str(inside_key)]['M'][actual_index]

                # Define dictionary structure with subkeys: outside key = propeller name, inside key = RPM

                final_dict[str(outside_keys)][str(inside_key)]['T'] = corr_thrust
                final_dict[str(outside_keys)][str(inside_key)]['P'] = corr_power
                final_dict[str(outside_keys)][str(inside_key)]['M'] = corr_torque
                final_dict[str(outside_keys)][str(inside_key)]['v'] = closest_velocity

            else:
                continue

    final_dict = {k: v for k, v in final_dict.items() if v}

    return final_dict


if __name__ == '__main__':
    # Directories, data and empty dicts
    final_files_directory = '//'.join([os.getcwd(), 'CSV_of_PERFILES2'])

    all_propellers = {}  # Initial dictionary where APC propeller data are saved
    filtered_propellers = {}  # Dictionary for the propeller at 4 m/s

    v_sizing = 2  # m/s

    index = 0

    data = store_data_in_dictionary(
        final_files_directory)  # load the dictionary by reading the CSV. This fills the all_propellers

    final_propellers = get_propellers_atvelocity(v_sizing, all_propellers, filtered_propellers)

    # NB: No need to activate this if you download the data.pkl file from git already

    # Save the 2 m/s propellers, filtered:
    save_file = open('data_2.pkl', 'wb')
    pickle.dump(filtered_propellers, save_file)
    save_file.close()

    # Save all propellers

    save_all_prop = open('complete_prop_dict.pkl', 'wb')
    pickle.dump(all_propellers, save_all_prop)
    save_all_prop.close()
