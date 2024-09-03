"""
Author: @jlarija
This code serves for the complete powertrain sizing, based on the selection of motors that was already done.
"""
import os

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit

sns.set_style('dark')

pd.set_option('mode.chained_assignment', None)

analyse_data = True

'''Mission overview'''


class SizingPower:
    """This produces the plot with the mission time and estimate of power expenditure over
    mission time. Time is in minutes (but doesn't matter too much depends on the data you want)"""

    def __init__(self, T_W=[], time=[]):
        self.T_W = T_W
        self.time = time

    def plot_power_expenditure(self):
        plt.vlines(time[0], self.T_W[0], self.T_W[1], color='cyan')
        plt.hlines(self.T_W[0], 0, self.time[0], color='cyan')
        plt.vlines(self.time[1], self.T_W[1], self.T_W[2], color='cyan')
        plt.hlines(self.T_W[1], self.time[0], self.time[1], color='cyan')
        plt.vlines(self.time[2], self.T_W[2], self.T_W[3], color='cyan')
        plt.hlines(self.T_W[2], self.time[1], self.time[2], color='cyan')
        plt.hlines(self.T_W[3], self.time[2], self.time[3], color='cyan')
        plt.ylabel('T/W ratio')
        plt.xlabel('Duration')

        return plt.show()


T_W = [1.4, 1.2, 2, 0.9]

tot_flight_time = 15
time_percentage = [0.25, 0.75, 0.755, 1]
time = []
for element in time_percentage:
    time.append(element * tot_flight_time)

avg_power_expenditure = SizingPower(T_W, time)
weight_prelim = 14.64  # kg #Motor data of the power through the mission:
T_W = np.asarray(T_W)
T_req = (weight_prelim * 9.81 * T_W / 4) / 1.6
T_req_g = T_req * 100  # convert newtons to grams


class MotorData():
    """ Contains the data for all of the motors that are in the database (easier to store on Python
    than in the Excel) """

    def __init__(self):
        pass

    def fitting(self, x, a, b):
        return a * x ** 2 + b * x

    def polyfit(self, function, motor_thrust, motor_power):
        a, b = curve_fit(function, motor_thrust, motor_power)[0]
        return a, b

    def calculate_avg_power(self, a, b, t_req, time):
        P_req = self.fitting(t_req, a, b)
        P_average = (P_req[0] * time[0] + P_req[1] * (time[1] - time[0]) + P_req[2] * (time[2] - time[1])
                     + P_req[3] * (time[3] - time[2])) / (time[3])
        return P_average

    def U7_KV420(self):
        thrust = [1940, 2880, 3530, 4080, 4560]
        power = [250, 455, 635, 823, 993]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def U7_KV490(self):
        thrust = [2260, 3450, 4020, 4790, 5070]
        power = [350, 638, 870, 1113, 1325]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def MN505S_KV380(self):
        thrust = [1071, 1160, 1287, 1414, 1545, 1676, 1843, 1985, 2084, 2216, 2347, 2806, 3091, 3456, 3818, 4606, 5444]
        power = [127, 141, 158, 177, 196, 216, 242, 270, 293, 320, 348, 439, 504, 587, 685, 901, 1163]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV300_APC14x7_LONGSHAFT(self):
        thrust = [1086, 1375, 1796, 2183, 2633, 2989, 3536, 4146, 4686, 5432, 6283]
        power = [151.51, 201.78, 287.44, 388.82, 497.36, 595.23, 754.68, 993.34, 1181.17, 1729.89, 2323.39]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV300_APC15x8_LONGSHAFT(self):
        thrust = [1434, 1779, 2342, 2982, 3484, 4010, 4569, 5080, 5694, 6751, 7787]
        power = [193.7, 253.89, 375.21, 513.33, 667.08, 816.06, 981.04, 1355.63, 1689.88, 2412, 3117.41]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV230_APC16X8(self):
        thrust = [1087, 1341, 1744, 2139, 2513, 2906, 3366, 3903, 4407, 5293, 6395]
        power = [127.58, 165.46, 229.88, 302.67, 302.67, 468.76, 579.1, 720.88, 865.54, 1215.78, 1674.45]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV450_APC17X10(self):
        thrust = [1632, 1873, 2182, 2671, 3124, 3610, 4039, 4486, 5113, 6091, 6534]
        power = [212.83, 256.58, 315.17, 414.61, 510, 627, 747.18, 882.51, 1061.39, 1390.48, 1571.68]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV450_APC18X8(self):
        thrust = [1778, 2016, 2356, 2830, 3374, 3824, 4355, 4908, 5409, 6471, 7017]
        power = [212.8, 252.32, 314.41, 404.33, 511.02, 615.93, 735, 879.75, 1026.98, 1346.9, 1540.06]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def AT4130_KV300_APC18X8(self):
        thrust = [1246, 1573, 2061, 2542, 3027, 3438, 4019, 4601, 5145, 6224, 7231]
        power = [122.11, 165.57, 249.2, 333.59, 428.57, 512.67, 642.57, 796.16, 945.54, 1269.83, 1617.91]
        a, b = self.polyfit(self.fitting, thrust, power)
        avg_mission_power = self.calculate_avg_power(a, b, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), a, b, avg_mission_power

    def COBRA_4120_MAS14X7X3(self):
        # warnings.warn("SELECTED MOTOR COBRA_4120 CANNOT PRODUCE 2 T/W")
        thrust = [4215, 3141.65, 2692.84, 2019.63]
        power = [0.00004 * t ** 2 + 0.0605 * t for t in thrust]
        avg_mission_power = self.calculate_avg_power(0.00004, 0.0605, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), avg_mission_power

    def COBRA_4120_APC15X6E(self):
        # warnings.warn("SELECTED MOTOR COBRA_4120 CANNOT PRODUCE 2 T/W")
        thrust = [4154, 3141.65, 2692.84, 2019.63]
        power = [0.00004 * t ** 2 + 0.0605 * t for t in thrust]
        avg_mission_power = self.calculate_avg_power(0.00004, 0.0605, T_req_g, time)
        return np.asarray(thrust), np.asarray(power), avg_mission_power

    def motor_fitting_plots(self):
        plt.scatter(self.U7_KV420()[0], self.U7_KV420()[1], color='red', label='U7_KV420', marker='.')
        plt.plot(self.U7_KV420()[0],
                 self.fitting(np.asarray(self.U7_KV420()[0]),
                              self.polyfit(self.fitting, self.U7_KV420()[0], self.U7_KV420()[1])[0],
                              self.polyfit(self.fitting, self.U7_KV420()[0], self.U7_KV420()[1])[1]), color='red')

        plt.scatter(self.MN505S_KV380()[0], self.MN505S_KV380()[1], color='blue', label='MN505S_KV380', marker='^')
        plt.plot(self.MN505S_KV380()[0],
                 self.fitting(np.asarray(self.MN505S_KV380()[0]),
                              self.polyfit(self.fitting, self.MN505S_KV380()[0], self.MN505S_KV380()[1])[0],
                              self.polyfit(self.fitting, self.MN505S_KV380()[0], self.MN505S_KV380()[1])[1]),
                 color='blue')

        plt.scatter(self.AT4130_KV230_APC16X8()[0], self.AT4130_KV230_APC16X8()[1], color='orange',
                    label='AT4130_KV230_APC16X8', marker='1')
        plt.plot(self.AT4130_KV230_APC16X8()[0],
                 self.fitting(np.asarray(self.AT4130_KV230_APC16X8()[0]),
                              self.polyfit(self.fitting, self.AT4130_KV230_APC16X8()[0],
                                           self.AT4130_KV230_APC16X8()[1])[0],
                              self.polyfit(self.fitting, self.AT4130_KV230_APC16X8()[0],
                                           self.AT4130_KV230_APC16X8()[1])[1]), color='orange')

        plt.scatter(self.AT4130_KV300_APC14x7_LONGSHAFT()[0], self.AT4130_KV300_APC14x7_LONGSHAFT()[1],
                    color='green', label='AT4130_KV300_APC14x7_LONGSHAFT', marker='*')
        plt.plot(self.AT4130_KV300_APC14x7_LONGSHAFT()[0],
                 self.fitting(np.asarray(self.AT4130_KV300_APC14x7_LONGSHAFT()[0]),
                              self.polyfit(self.fitting, self.AT4130_KV300_APC14x7_LONGSHAFT()[0],
                                           self.AT4130_KV300_APC14x7_LONGSHAFT()[1])[0],
                              self.polyfit(self.fitting, self.AT4130_KV300_APC14x7_LONGSHAFT()[0],
                                           self.AT4130_KV300_APC14x7_LONGSHAFT()[1])[1]),
                 color='green')

        plt.xlabel('Thrust [g]')
        plt.ylabel('Power [W]')
        plt.legend()
        plt.title('Thrust vs Power for some selected motors')
        return plt.show()


def battery_selection(target_capacity: float, motor_voltage: float, motor_power_65: float, motor_count: int):
    """

    Additional eplanation:
    Motor voltage has a margin of 15%, since the voltage of a LiPo cell varies between 3.7-4.2V,
    depending on the battery charge level. Since both the motor voltage as the battery voltage
    can be provided as a fully charged LiPo battery, the margin is taken both as upper and lower bound.
    """

    # Constants for battery sizing.
    battery_efficiency = 0.95
    DoD = 0.80

    # Load the files in a pandas dataframe.
    fileloc = os.getcwd()

    filename_batteries = ''.join([fileloc, '/electrical/Power_Sizing_Dataset_Batteries.csv'])
    batteries_df = pd.read_csv(filename_batteries)

    # Filter batteries based on the motor voltage requirement, with a 15% margin for charge levels.
    batteries_df = batteries_df[batteries_df["Voltage Output [V]"] > motor_voltage * (0.85)]
    batteries_df = batteries_df[batteries_df["Voltage Output [V]"] < motor_voltage * (1.15)]

    # Check for the minimum battery amount needed, and calculate the 'overcapacity'.
    battery_count_float = target_capacity / batteries_df["Capacity [mAh]"]
    # Rounding up the value to the nearest integer.
    battery_count_min = np.ceil(battery_count_float)
    # Calculate the excess in capacity due to rounding the battery count.
    battery_overcapacity = np.round(battery_count_min - battery_count_float, 2) * batteries_df["Capacity [mAh]"]

    # Weight of the total assembly, if there are multiple circuits, then the total is given.
    battery_assembly_weight = battery_count_min * batteries_df["Weight [+20 g]"]

    # The total capacity of all circuits is calculated.
    battery_assembly_capacity = battery_count_min * batteries_df["Capacity [mAh]"]

    # The energy density of the whole assembly is calculated here.
    assembly_energy_density = battery_assembly_capacity / battery_assembly_weight

    # The mission time of the whole assembly is counted here.
    mission_time = (battery_assembly_capacity * battery_efficiency * motor_voltage * DoD) / (
                motor_power_65 * (motor_count)) * 3.6 / 60

    # The burst current for one circuit is calculated here.
    burst_current = batteries_df["C-rate [-]"] * battery_assembly_capacity / 1000

    # Creating a new DataFrame with the newly calculated values for the battery assemblies.
    new_df = batteries_df["Capacity [mAh]"].to_frame()
    new_df = new_df.assign(battery_count=battery_count_min.values, assembly_capacity=battery_assembly_capacity.values,
                           overcapacity=battery_overcapacity.values, energy_density=assembly_energy_density.values,
                           mission_time=mission_time.values, assembly_weight=battery_assembly_weight.values,
                           C_rate=batteries_df["C-rate [-]"].values, burst_current_pc=burst_current.values)
    final_df = new_df.sort_values(by='assembly_weight')
    best_option = final_df.iloc[0]
    return best_option


def get_capacity(t_flight, P, N_rot, voltage):  # TODO YOU CAN ADD CAPACITY TO THE MOTOR CLASS TOO SINCE IT'S DEPENDENT
    C = (t_flight * 60 * P * N_rot * 1000) / (3600 * voltage * 0.80 * 0.95)
    return C


if analyse_data == True:
    motors = MotorData()

    avg_powers = [motors.U7_KV420()[4], motors.U7_KV490()[4], motors.MN505S_KV380()[4],
                  motors.COBRA_4120_MAS14X7X3()[2], motors.AT4130_KV300_APC14x7_LONGSHAFT()[4],
                  motors.AT4130_KV300_APC15x8_LONGSHAFT()[4], motors.COBRA_4120_APC15X6E()[2],
                  motors.AT4130_KV230_APC16X8()[4], motors.AT4130_KV450_APC17X10()[4],
                  motors.AT4130_KV450_APC18X8()[4], motors.AT4130_KV300_APC18X8()[4], 400]

    # Read the motor data + some data skimming: eliminate COBRA for now cause can't produce 2 T/W and AT 3520 we dont have data
    motor_df = pd.read_csv('Motor_Propeller_Comb.csv')
    motor_df = motor_df[motor_df["Max Current drawn [A]"].notna()]
    motor_df['Average Power Expenditure'] = 0  # create new column in dataframe to save data somewhere
    motor_df['Total Capacity Required [mAh]'] = 0
    motor_df["Best battery weight"] = 0
    motor_df["Battery capacity"] = 0
    motor_df["Number of Batteries"] = 0
    motor_df["Overall Weight [kg]"] = 0
    motor_df = motor_df.reset_index(drop=True)

    """To be deleted maybe"""
    voltage = motor_df['Voltage [V]']
    batteryconfig = motor_df['Battery config']
    motor_current = motor_df['Max Current [A]']
    fileloc = os.getcwd()
    count = 0

    for power in avg_powers:
        capacity = get_capacity(time[-1], np.ceil(power), 8, motor_df['Voltage [V]'][count])
        motor_df['Average Power Expenditure'][count] = np.ceil(power)
        motor_df['Total Capacity Required [mAh]'][count] = np.round(capacity, 0)

        count += 1

    for index, row in motor_df.iterrows():
        current_voltage = row['Voltage [V]']

        best_option = battery_selection(row['Total Capacity Required [mAh]'], current_voltage,
                                        row['Average Power Expenditure'],
                                        8)

        motor_df["Best battery weight"][index] = best_option["assembly_weight"]
        motor_df["Number of Batteries"][index] = best_option["battery_count"]
        motor_df["Battery capacity"][index] = best_option['assembly_capacity']

        total_weight = best_option["assembly_weight"] + motor_df["Weight of one [g]"][index] * 8
        motor_df["Overall Weight [kg]"][index] = total_weight

    # finally, save the dataframe to CSV
    # motor_df.to_csv(''.join(['Motor_Data_', str(tot_flight_time), 'min.csv']))

weights = []


def read_csv(title):
    return pd.read_csv(title)


'''
for file in os.listdir():
    if 'min' in str(file):
        data = read_csv(str(file))
        lightest = data.sort_values(by='Overall Weight [kg]')
        save_lightest = lightest.iloc[0]
        weights.append(save_lightest['Overall Weight [kg]'])


times = np.asarray([20,17,16,15,14,13,12,11,10])

weights = np.asarray(weights)* 10 ** (-3)
weights = np.flip(np.sort(weights))

#just plotting times against weights

class Pretty_Plots():

    """A class because I was tired of remaking the same plots over and over again so now I can save
    the settings. These are mostly for pandas or numpy plotting"""

    def __init__(self):
        pass


    def scatter_xy_pastelpalette(self, dataframe, x_data, y_data,xlabel,title):

        ax = sns.scatterplot(data=dataframe, x=x_data,y=y_data, hue=str(y_data), palette ='pastel',legend=False)
        plt.grid()
        ax.set(xlabel = str(xlabel), ylabel=None ,title=title)
        plt.tight_layout()

        return plt.show()

    def lineplot(self, x,y, xlabel, ylabel, title ):

        plt.tight_layout
        plt.plot(x,y,color = '#DDA0DD', marker = 'o')
        plt.title(title)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.yticks(y)
        plt.grid()

        return plt.show()

#data = Pretty_Plots()

#plot = data.lineplot(weights, times,'Weight [kg]', ' Flight Time [min]', title='Required Battery Weight per Flight Time')
#plot_1 = data.scatter_xy_pastelpalette(data_for_plot.sort_values(by='Overall Weight [kg]'),x_data=x_data, y_data='Motor + Prop Name',
#                                     xlabel='Config. Weight [kg]',title='Mission Time: 20 [min]')

#plot_2 = data.scatter_xy_pastelpalette(data_for_plot_2.sort_values(by='Overall Weight [kg]'),x_data=x_data_2, y_data='Motor + Prop Name',
                                    # xlabel='Config. Weight [kg]',title='Mission Time: 17 [min]')

'''
