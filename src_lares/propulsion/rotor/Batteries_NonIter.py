"""
Author: @jlarija

This code is meant to graph all of the propeller data for the final propeller. Changing the name of the file that has to
be loaded will load a different propeller. Since the data of the selected propeller are used as input for the sizing of
motor, ESC and batteries (in this order) the complete power system is sized in here.
"""

import pickle

import numpy as np
from matplotlib import pyplot as plt

from APC_propellers import APCPropellers_RPM_Size as datasaver

# Load APC dictionary
load_all_prop = open('complete_prop_dict', 'rb')
all_prop = pickle.load(load_all_prop)
load_all_prop.close()

# Only keep the relevant propeller
selected_val = all_prop['1225x375']
all_prop.clear()
final_prop = selected_val

final_prop_at4ms = {}


# Now only select the velocity for the value

def temporary_vel_sizing(input_propellerdict, v_sizing, final_dict):
    for inside_key in input_propellerdict.keys():

        final_dict[str(inside_key)] = {}

        closest_velocity = min(input_propellerdict[str(inside_key)]['v'],
                               key=lambda x: abs(x - v_sizing),
                               default=0)  # Find the closest velocity to the sizing velocity among the data set

        if abs(closest_velocity - v_sizing) < 0.5:

            get_index = np.where(
                input_propellerdict[str(inside_key)]['v'] == closest_velocity)

            actual_index = get_index[0]  # np.where returns an array

            corr_thrust = input_propellerdict[str(inside_key)]['T'][actual_index]
            corr_power = input_propellerdict[str(inside_key)]['P'][actual_index]
            corr_torque = input_propellerdict[str(inside_key)]['M'][actual_index]

            # Define dictionary structure with subkeys: outside key = propeller name, inside key = RPM

            final_dict[str(inside_key)]['T'] = corr_thrust
            final_dict[str(inside_key)]['P'] = corr_power
            final_dict[str(inside_key)]['M'] = corr_torque
            final_dict[str(inside_key)]['v'] = closest_velocity

        else:
            continue

    final_dict = {k: v for k, v in final_dict.items() if v}

    return final_dict


vel_4ms = temporary_vel_sizing(v_sizing=4, input_propellerdict=final_prop, final_dict=final_prop_at4ms)

# remove empty ones
final_prop_at4ms = {k: v for k, v in final_prop_at4ms.items() if v}

# Now make plots of thrust vs RPM at 4 m/s approx
fig, ax = plt.subplots(1, 1)

index = 0
T_tab = []
RPM_tab = []

# Plot the RPM vs thrust at required speed

for key in final_prop_at4ms.keys():
    RPM = int(key[4:])
    RPM_tab.append(RPM)
    T_tab.append(float(final_prop_at4ms[key]['T']))
ax.plot(T_tab, RPM_tab, color='#00A6D6', label='Thrust vs RPM', marker="^")
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.88, box.height])
ax.axvspan(23.52, 45, color='#beafd0', label='Single \n Config. \n Thrust \n Required', alpha=0.25)
ax.legend(ncol=1, loc='center left', bbox_to_anchor=(0.9, 0.9))
ax.grid()
ax.set_xlim(0, 45)
ax.set_xlabel("Thrust [N]")
ax.set_ylabel("RPM")
ax.set_title('Thrust APC @ v = 4 [m/s] per RPM', loc='left')

plt.show()

saving_location = 'C:\\Users\\jlari\\Desktop\\Drones Design Resources\\Documentation on design choices\\Pictures for documentation'
save_figure = datasaver.Plotting()
fig_name = '\\12.25x3.75_4ms'
saving_name = ''.join([saving_location, fig_name, '.pdf'])
savefig = save_figure.save_plot(saving_name, fig)

"""----MOTOR SIZING----"""


class Motor:

    def __init__(self, P_req):
        self.P_req = P_req
        pass

    def sizing_param_motors(self):
        P_sizing = self.P_req / 0.65
        return


"""----BATTERY----"""
DoD = 0.80
t_phase = 20 * 60  # 20 mins
Preq = 520  # W (at most?)
eta_b = 0.95
N = 8

I_peak = 61.65  # A
t_needed = 15  # s
V = 22.2  # V

energy_supplied = I_peak * V * N  # W

Qb = (t_phase * Preq * 0.5 * N * 1000) / (3600 * V * DoD * eta_b)
print("Batteries total capacity required at least", Qb)

Nbatteries = 2

print("Battery capacity per battery, at least", Qb / Nbatteries)

Battery_capacity = float(input("Chosen battery capacity?"))
Battery_energy = V * (Battery_capacity / 1000) * 3600

req_Crating = (energy_supplied * 3600) / Battery_energy

print("CRating", req_Crating)

use_motor = ((t_needed * energy_supplied) / Battery_energy) * 100
print('Usage of battery capacity for peak:', use_motor, '%')

batt_weight = float(input("Battery weight:"))

print("System weight:", batt_weight * Nbatteries)
