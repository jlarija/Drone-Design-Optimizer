import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Motor():
    """This class is used for the basic parameters of the UAV's motors."""

    def __init__(self, model: str, power: float, voltage: float, peakcurrent: float, KV: float, weight: float):
        self.model = model
        self.power = power
        self.voltage = voltage
        self.peakcurrent = peakcurrent
        self.KV = KV
        self.weight = weight

    def __str__(self):
        return (
            f" Model: {self.model} \n Power: {self.power} \n Voltage: {self.voltage} \n Peak current: {self.peakcurrent} \n KV: {self.KV} \n Weight: {self.weight}")


class ESC():
    """This class is used for the basic parameters of the UAV's ESCs."""

    def __init__(self, model: str, voltage: float, peakcurrent: float, contcurrent: float, weight: float):
        self.model = model
        self.voltage = voltage
        self.peakcurrent = peakcurrent
        self.contcurrent = contcurrent
        self.weight = weight

    def __str__(self):
        return (
            f" Model: {self.model} \n Voltage: {self.voltage} \n Peak Current: {self.peakcurrent} \n Continuous Current: {self.contcurrent} \n Weight: {self.weight}")


class Battery():
    """This class is used for the basic parameters of the UAV's Batteries."""

    def __init__(self, model: str, voltage: float, peakcurrent: float, contcurrent: float, weight: float,
                 capacity: float):
        self.model = model
        self.voltage = voltage
        self.peakcurrent = peakcurrent
        self.contcurrent = contcurrent
        self.weight = weight
        self.capacity = capacity

    def __str__(self):
        return (
            f" Model: {self.model} \n Voltage: {self.voltage} \n Peak Current: {self.peakcurrent} \n Continuous Current: {self.contcurrent} \n Weight: {self.weight} \n Capacity {self.capacity}")


def Power_Sizing_Cat(Preq: float, t_phase: float, N: int, DoD=0.80, eta_b=0.95):
    """
    This function gives a basic sizing of the power system. Currently it is limited to the Motor and ESC sizing.
    The function also returns the approximated loaded KV values with the 65% of the maximum power of the motor.

    Battery sizing is not yet fully implemented, pending iterations between the motors and CRotor.
    
    Inputs:
    Preq        :float  [W] The power required by the motors.
    t_phase     :float  [s] The desired mission time.
    N           :int    [-] The amount of motors used by the UAV.
    DoD = 0.80  :float  [-] The Depth of Discharge of the batteries.
    eta_b = 0.95:float  [-] The Battery efficiency (Average efficiency of LiPo battery cells).
    
    Outputs:
    Motor1      :object [-] The properties of the selected motor as a class "Motor".  
    ESC1        :object [-] The properties of the selected ESC as a class "ESC". 
    AL_KV       :ndarray[-] A numpy array containing the approximated KV values at 55% of no-load KV values of the motor catalogue.
    Pmax_65     :ndarray[-] A numpy array containing the power at 65% of the maximum power of the motor catalogue.
    """

    S_LiPo = 3.7  # [V]

    # Load the files in a pandas dataframe.
    fileloc = os.getcwd()
    filename_Motors = ''.join([fileloc, '\Power_Sizing_Dataset_Motors.csv'])
    PS_data_Motors = pd.read_csv(filename_Motors)

    filename_ESC = ''.join([fileloc, '\Power_Sizing_Dataset_ESCs.csv'])
    PS_data_ESC = pd.read_csv(filename_ESC)

    filename_Batteries = ''.join([fileloc, '\Power_Sizing_Dataset_Batteries.csv'])
    PS_data_Batteries = pd.read_csv(filename_Batteries)

    # Function to read the voltage strings from the files.
    def V_nom_str_reader(V_nom_str):
        """
        Function to read the rated voltage numbers, typically presented as XX-XXS.
        Takes a voltage rating, and detects the integers in it.
        Returns the values in a numpy array as integers, or as float.
        """
        if '-' in V_nom_str:
            V_nom_str = V_nom_str[:-1]

            V_nom_S = V_nom_str.split('-')
        else:
            V_nom_S = V_nom_str[:-1]

        # Convert string array to integer array
        V_nom_S = np.array(V_nom_S).astype(int)

        return V_nom_S

    """MOTOR SELECTION"""
    # Find the closest value for the maximum power of a motor, around the 65% throttle value.
    Pmax = np.abs(PS_data_Motors["Max Power [W]"] - (Preq / 0.65))
    Pmax = Pmax.to_frame()

    # Find the row in the pandas dataframe which corresponds to the closest value.
    Mot_index = np.argmin(Pmax)
    Mot_select = PS_data_Motors.loc[Mot_index]

    # Check for the voltage range, for ESC and battery selection.
    V_nom_S = V_nom_str_reader(str(Mot_select[5]))

    Motor1 = Motor(Mot_select[1], Mot_select[3], V_nom_S * S_LiPo, Mot_select[4], Mot_select[2], Mot_select[6])

    "ESC SELECTION"
    ESC_feasible_V_nom = []
    V_sum = []

    for k in range(len(PS_data_ESC) - 1):
        if (np.max(V_nom_str_reader(PS_data_ESC.loc[k][4])) >= np.max(V_nom_S)):
            if type(V_nom_str_reader(PS_data_ESC.loc[k][4]) * S_LiPo - Motor1.voltage) == type(np.array(0)):
                if all(i >= 0 for i in
                       (np.array(V_nom_str_reader(PS_data_ESC.loc[k][4])) * S_LiPo - Motor1.voltage)) == True:
                    ESC_feasible_V_nom.append(PS_data_ESC.loc[k])
                    V_sum.append(V_nom_str_reader(PS_data_ESC.loc[k][4]) * S_LiPo - Motor1.voltage)
            elif type(V_nom_str_reader(PS_data_ESC.loc[k][4]) * S_LiPo - Motor1.voltage) != type(np.array(0)):
                if V_nom_str_reader(PS_data_ESC.loc[k][4]) * S_LiPo - Motor1.voltage >= 0:
                    ESC_feasible_V_nom.append(PS_data_ESC.loc[k])
                    V_sum.append(V_nom_str_reader(PS_data_ESC.loc[k][4]) * S_LiPo - Motor1.voltage)

    ESC_feasible = pd.DataFrame(ESC_feasible_V_nom)
    ESC_feasible['V Sum'] = np.round(np.matrix(V_sum).sum(axis=1), 2)

    # Find the closest value for the peak current of the ESC.

    A_peak_ESC = ESC_feasible[ESC_feasible["Peak Current [A]"] - (Motor1.peakcurrent) > 0]
    min_rows = A_peak_ESC[A_peak_ESC["Peak Current [A]"] == A_peak_ESC["Peak Current [A]"].min()]
    # Then find the minimum weight in case multiple ESCs fullfil criterion.
    ESC_select = min_rows[min_rows["V Sum"] == min_rows["V Sum"].min()]

    ESC_test = ESC_select.to_numpy()
    ESC1 = ESC(ESC_test[0][1], ESC_test[0][4], ESC_test[0][3], ESC_test[0][2], ESC_test[0][5])

    "BATTERY SELECTION"

    # Current draw at maximum power
    Volt_feasible = Motor1.voltage[Preq / Motor1.voltage < ESC1.peakcurrent]
    Volt_feasible = np.min(Volt_feasible)

    # Battery capacity is not yet returned, will be implemented pending iteration with CRotor.
    Qb = (t_phase * Preq * 0.5 * N * 1000) / (3600 * Volt_feasible * DoD * eta_b)

    if __name__ == "__main__":

        V_nom_NL = []
        for x in range(len(PS_data_Motors['Rated Voltage [*S]'])):
            V_nom_elem = V_nom_str_reader(PS_data_Motors['Rated Voltage [*S]'].iloc[x])
            V_nom_NL.append(np.max(V_nom_elem))
        AL_KV = PS_data_Motors['KV [RPM/V]'].to_numpy() * V_nom_NL * 0.55  # Value of KV Fraction
        Pmax_65 = PS_data_Motors['Max Power [W]'].to_numpy() * 0.65
        plt.figure()
        plt.scatter(AL_KV, Pmax_65, color="skyblue")
        plt.xlabel('Loaded RPM Approximation [RPM]')
        plt.ylabel('Power Required (65%) [W]')
        plt.grid()
        plt.show()

    return Motor1, ESC1, AL_KV, Pmax_65


"Code test section"
if __name__ == "__main__":
    Preq = 400  # [W]
    DoD = 0.8  # [-] Depth of Discharge
    eta_b = 0.95  # [-] LiPo Battery Efficiency
    N = 4  # [-] Amount of motors considered
    t_phase = 20*60  # [s]

    Motor1, ESC1, AL_KV, Pmax_65 = Power_Sizing_Cat(Preq, t_phase, N)
    print(Motor1)
    print()
    print(ESC1)
    print()
    print(AL_KV)
    print()
    print(Pmax_65)
