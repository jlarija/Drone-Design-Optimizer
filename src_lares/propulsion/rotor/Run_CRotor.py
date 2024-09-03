import os
import subprocess

import numpy as np
import pandas as pd


# from LARES_preliminarysizing.py import T_req - #TODO figure out input across multiple directories

class Propellers:
    """ Run CRotor based on the inputs"""

    # Basically like passing inputs to a function
    def __init__(self, r_front: list = [0], r_aft: list = [0], blades_front: list = [0], blades_aft: list = [0],
                 P_rot: list = [0], RPM_coaxial: list = [0], speed: float = 0, fileloc: str = 'N/A',
                 blades_single: list = [0], r_single: list = [0], RPM_single: list = [0], P_single: list = [0],
                 lift_coeff: list = [0]):
        self.r_front = r_front
        self.r_aft = r_aft
        self.blades_front = blades_front
        self.blades_aft = blades_aft
        self.P_rot = P_rot
        self.RPM_coaxial = RPM_coaxial
        self.speed = speed
        self.blades_single = blades_single
        self.r_single = r_single
        self.RPM_single = RPM_single
        self.P_single = P_single
        self.lift_coeff = lift_coeff
        self.fileloc = fileloc

    # Give a description of the inputs
    def __str__(self):
        return f" upper rotor radius \n{self.r_front}| lower rotor radius \n{self.r_aft} | Blades of upper rotor \n{self.blades_front} |  Blades of lower rotor \n{self.blades_aft}" \
               f" Power of coaxial set \n{self.P_rot} | RPM coaxial set \n{self.RPM_coaxial}| Speed \n{self.speed} |" \
               f" # blades single rotor \n{self.blades_single} | Radius single rotor \n{self.blades_single} | RPM of single rotor \n{self.RPM_single} |" \
               f" Power of single rotor \n{self.P_single} | Blade section lift coefficient \n{self.lift_coeff} | CRotor output directory location \n{self.fileloc} "

    def do_coaxialrotor(self):

        i = 0  # Iteration count for the bigger loop (top radius)

        for j in range(0, len(self.r_front)):
            # hub and wake radiuses:
            r_hub = np.divide(self.r_front[i], 15)
            r_wake = np.divide(r_hub, 2)

            # Open program CRotor
            ps = subprocess.Popen(''.join([str(self.fileloc), '\\Crotor\\CRotor755es13_win32\\bin\\xrotor.exe']),
                                  shell=True, stdin=subprocess.PIPE,
                                  text=True)  # Open CRotor for first iteration, from pc location

            # Pass the inputs to CRotor. Each string separated by a comma is a new input, can be passed together, as when the communicate is closed, the program is closed too
            ps.communicate(os.linesep.join(
                ['AERO', 'EDIT', '1', '-0.5', '2', '7.9595', '4', '1.4316', '5', '-0.52', '7', '0.0277', '8', '-0.3455',
                 '10', '50000', '11', '0', '12', '-0.2131', '13', '0.61', '\n'  # Load data of Wortmann FX airfoil
                                                                          'NEW', '0.10',
                 'NEW', '2', '0.11',
                 'EDIT', '3', '1', '-6.5', '2', '5.55769', '4', '1.8415', '5', '-0.0067', '7', '0.01413', '8', '0.0131',
                 '10', '200000', '12', '-0.0541', '13', '0.5862', '\n'  # Load data of GOE225
                                                                  'NEW', '3', '0.90',  # Creates section 3
                 'NEW', '1', '0.91', '\n'
                                     'CROT', 'INPU',
                 str(self.P_rot[i]), str(self.RPM_coaxial[i]), str(self.speed),
                 # Initial input parameter: total power for 2 rotors, RPM 2 rotors, flight speed
                 'VCLR',  # Used to clean slipstream
                 'DFWD', 'Forward Rotor', str(self.blades_front[i]), str(self.r_front[i]), str(r_hub), str(r_wake),
                 # Data for forward rotor: name, No. blades, tip radius, hub radius, hub wake displacement body radius
                 'DFWD', '\n'  # This is a suggestion from the manual, to rerun forward rotor to let it optimise itself
                         'DAFT', 'Aft Rotor', str(self.blades_aft[i]), str(self.r_aft[i]), str(r_hub), str(r_wake),
                 # Data for aft rotor (same order as front)
                 ' '.join(['RPM', str(self.RPM_coaxial[i])]), ' '.join(['POWE', str(self.P_rot[i])]),
                 # To converge run a rpm and then a power sim, so to have the final
                 'FWD', ' '.join(['WRIT', ''.join(['Coaxial_Forward_Rotor_Iteration_Number', str(i), '.txt'])]),
                 # Runs the forward rotor and saves its output
                 'AFT', ' '.join(['WRIT', ''.join(['Coaxial_Rear_Rotor_Iteration_Number', str(i), '.txt'])])
                 # Runs and writes the aft rotor
                 ]))
            i += 1

        return print("Coaxial Rotor Done")

    def do_singlerotor(self):

        for i in range(0, len(self.r_single)):
            r_hub = np.divide(self.r_single[i], 7.5)
            r_wake = np.divide(r_hub, 2)

            ps = subprocess.Popen(''.join([str(self.fileloc), '\\Crotor\\CRotor755es13_win32\\bin\\xrotor.exe']),
                                  shell=True, stdin=subprocess.PIPE, text=True)
            ps.communicate(os.linesep.join(
                ['AERO', 'EDIT', '1', '-0.5', '2', '7.9595', '4', '1.4316', '5', '-0.52', '7', '0.0277', '8', '-0.3455',
                 '10', '50000', '12', '-0.2131', '\n'  # Load data of Wortmann FX airfoil
                                                 'NEW', '0.10',
                 'NEW', '2', '0.11',
                 'EDIT', '3', '1', '-6.5', '2', '5.55769', '4', '1.8415', '5', '-0.0067', '7', '0.01413', '8', '0.0131',
                 '10', '200000', '12', '-0.0541', '\n'  # Load data of GOE225
                                                  'NEW', '3', '0.90',  # Creates section 3
                 'NEW', '1', '0.91', '\n'
                 # 'DUCT', '1',  
                                     'DESI', 'INPU', str(self.blades_single[i]), str(self.r_single[i]), str(r_hub),
                 str(r_wake), str(self.speed), '0', str(self.RPM_single[i]), '0', str(self.P_single[i]),
                 str(self.lift_coeff[i]), '\n', '\n'
                                                'OPER',
                 ' '.join(['WRIT', ''.join(['Single_rotor_for_radius_', str(self.r_single[i]), '.txt'])])
                 ]))

            i += 1


class Data_analysis:
    """Analysis of the data from CRotor and XRotor """

    def __init__(self, fileloc: str = 'N/A', r_front: list = [0], r_aft: list = [0], r_single: list = [0]):
        self.r_front = r_front
        self.r_aft = r_aft
        self.r_single = r_single
        self.fileloc = fileloc

    def generate_files_names(self):

        """Generates the file names (files themselves are generated by CRotor, this tells the program what to read)"""

        i = 0
        l = 0

        Upper_Rotors_Files = []
        Lower_Rotors_Files = []
        Single_Rotors_Files = []

        for j in range(0, len(self.r_front)):

            file1 = ''.join([self.fileloc, '\Coaxial_Forward_Rotor_Iteration_Number', str(i), '.txt'])
            file2 = ''.join([self.fileloc, '\Coaxial_Rear_Rotor_Iteration_Number', str(i), '.txt'])

            if os.path.isfile(file1):
                Upper_Rotors_Files.append(file1)
            if os.path.isfile(file2):
                Lower_Rotors_Files.append(file2)
            else:
                continue
            i += 1

        for k in range(0, len(self.r_single)):
            file = ''.join([self.fileloc, '\Single_rotor_for_radius_', str(self.r_single[l]), '.txt'])
            if os.path.isfile(file):
                Single_Rotors_Files.append(file)
            else:
                continue

            l += 1

        return Upper_Rotors_Files, Lower_Rotors_Files, Single_Rotors_Files

    def read_data(self, filetab):
        """ Reads the files"""

        global thrust, power, radius, rpm

        thrust_tab = []
        power_tab = []
        radius_tab = []
        rpm_tab = []

        for i in range(0, len(filetab)):

            if 'Coaxial' in str(filetab[i]):
                row_radialsections = 31
                row_thrust = 19
                row_radius = 18
                row_rpm = 20

            elif 'Single' in str(filetab[i]):
                row_radialsections = 17
                row_thrust = 5
                row_radius = 4
                row_rpm = 6

            else:
                return 'Invalid Filename'

            if os.path.isfile(str(filetab[i])):  # equivalent to a if==true statement

                # Obtain data per radial section (in case we need it)
                data = pd.read_fwf(str(filetab[i]), skiprows=row_radialsections, index_col=False,
                                   names=['row index', 'r/R', 'c/R', 'beta(deg)', 'CL', 'CD', 'Rex10^3', 'Mach',
                                          'efficiency', 'effp', 'na.u/U'])

                # This second read function isolates the row in the txt file specifying thrust and power
                thrust_value = pd.read_fwf(str(filetab[i]), skiprows=row_thrust, skipfooter=41, index_col=False)
                radius_value = pd.read_fwf(str(filetab[i]), skiprows=row_radius, skipfooter=42, index_col=False)
                rpm_value = pd.read_fwf(str(filetab[i]), skiprows=row_rpm, skipfooter=40, index_col=False)

                for col in thrust_value.columns:  # obtain actual values
                    values = col.split()
                    thrust = float(values[2])
                    power = float(values[5])

                for colu in radius_value.columns:
                    index = colu.split()
                    radius = float(index[6])

                for cavallo in rpm_value.columns:
                    things = cavallo.split()
                    rpm = float(things[8])

                thrust_tab.append(thrust)
                power_tab.append(power)
                radius_tab.append(radius)
                rpm_tab.append(rpm)

            else:
                return 'File does not exist, iteration of these values must not have converged'

        return np.asarray(thrust_tab), np.asarray(power_tab), np.asarray(radius_tab), np.asarray(rpm_tab), data[
            'beta(deg)']  # I like arrays more for graphing


def calculate_phi(velocity, RPM, r,
                  beta):  # For which angle phi represents, check documentation. It's just a velocity triangle

    phi = np.arctan(velocity / (RPM * r * np.pi / 30))
    alpha = beta - phi

    return alpha, phi


"""----------------- RUNNING CODE --------------------- """
if __name__ == "__main__":
    fileloc = os.getcwd()

    # Dummy inputs for coaxial rotors
    r_front = [0.17]  # [m]
    r_aft = [0.18]  # [m]
    RPM_coaxial = [11000]
    blades_front = [4]
    blades_aft = [4]
    speed = 0.4  # m/s - For indoor use, a speed of 4 m/s is more than reasonable
    Power_2rot = [1400]  # W
    blades_single = [4]
    r_single = [0.15]
    RPM_single = [11000]
    P_single = [650]
    lift_coeff = [0.5]

    T_req = 65.1  # N
    T_req_single = 32.5  # N
    case1 = Propellers(r_front, r_aft, blades_front, blades_aft, Power_2rot, RPM_coaxial, speed, fileloc, blades_single,
                       r_single, RPM_single, P_single, lift_coeff)
    rotor = case1.do_coaxialrotor()
    # rotor_single = case1.do_singlerotor()
    data = Data_analysis(fileloc, r_front, r_aft, r_single)
    file_names = data.generate_files_names()
    result = np.sum(data.read_data(file_names[0])[0][0] + data.read_data(file_names[1])[0][
        0])  # Keep this notation. 0 reads the first iteration, 1 the second etc
    print("Total obtained thrust by coaxial propellers", result, '[N]')
    # print("Difference from requirement for a T/W of 1.4: ", np.round(T_req - result, 2), '[N]')
