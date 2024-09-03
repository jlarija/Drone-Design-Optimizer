"""
Author: @jlarija
This code plots and skims the data obtained in the ReadFile.py for APC propellers. It loads the dictionary as obtained
in APCPropellers_Reader_VFilter.py, however if the repository is downloaded from git there is no need to run the first one as
everything already exists. The propeller data is made smaller by a certain criteria, such as max thrust produced, so that
only one point per propeller is present. This way the resultant graph is easier to interpret and a certain propeller
is easier to select.
"""

import pickle

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class DatabaseAnalysis:
    """This class includes all the functions used for the plotting of a specific subset of the APC propelles
    (e.g. by size, by thrust produced, by RPM...). The class input is simply the APC propellers initial dictionary,
    which can be loaded through the load function. """

    def __init__(self, prop_dict):
        self.prop_dict = prop_dict

    def get_max_thrust(self, init_dict, final_prop_dict):

        """This function is the original function that allows to get the graph at the maximum RPM """

        for outside_keys in init_dict.keys():  # iterate through propeller names that got into dictionary

            final_prop_dict[str(outside_keys)] = {}
            thrust_tab = []
            for inside_key in init_dict[str(outside_keys)].keys():  # ITERATE through RPMS

                # Now overwrite the thrust. Every time
                if init_dict[str(outside_keys)][str(inside_key)]:

                    thrust = init_dict[str(outside_keys)][str(inside_key)]['T']

                    thrust_tab.append(thrust)

                else:
                    continue

                selected_thrust = max(thrust_tab)

                get_index = np.where(init_dict[str(outside_keys)][str(inside_key)]['T'] == selected_thrust)[
                    0]
                power = init_dict[str(outside_keys)][str(inside_key)]['P'][get_index]

                final_prop_dict[str(outside_keys)]['T'] = selected_thrust
                final_prop_dict[str(outside_keys)]['P'] = power

        t_tab = [[] for z in range(len(acceptable_sizes))]
        p_tab = [[] for y in range(len(acceptable_sizes))]

        i = 0

        for item in acceptable_sizes:
            for prop in final_prop_dict.keys():

                current_label = self.get_label(prop)  # here you get 10,10,10,11

                if current_label == item:

                    t_tab[i].append(final_prop_dict[str(prop)]['T'])
                    p_tab[i].append(final_prop_dict[str(prop)]['P'])

                else:
                    continue

            i += 1

        return final_prop_dict, t_tab, p_tab

    def get_label(self, prop_name):
        """Must be here cause needed for small propellers, it just extracts the name"""
        label_ = ''.join([str(prop_name)[0], str(prop_name)[1]])
        if label_ == '87':
            label_ = '8x'
        if label_ == '52':
            label_ = '5x'
        if label_ == '92':
            label_ = '9x'
        return label_

    def get_propellers_smaller_than(self, prop_radiuses_to_select, small_prop_dict):

        """Input dictionaries must be empty dictionaries and must be created obviously"""

        # STEP 1: only select the propellers below a certain range

        for key in self.prop_dict.keys():  # Iterate through names

            prop_name = self.get_label(key)  # extract the label

            if prop_name in prop_radiuses_to_select:  # if it's any of the small propellers that you want
                small_prop_dict[str(key)] = {}
                for rpm, value in self.prop_dict[str(key)].items():
                    if value:
                        small_prop_dict[str(key)][str(rpm)] = {}

                        small_prop_dict[str(key)][str(rpm)]['T'] = self.prop_dict[str(key)][str(rpm)]['T']
                        small_prop_dict[str(key)][str(rpm)]['P'] = self.prop_dict[str(key)][str(rpm)]['P']

        return small_prop_dict

    def select_RPM(self, input_dict, RPM_dict, selected_RPM, alternative_RPM1, alternative_RPM2):

        for propeller in input_dict.keys():

            RPM_dict[str(propeller)] = {}

            try:
                RPM = selected_RPM
                RPM_dict[str(propeller)]['T'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['T']
                RPM_dict[str(propeller)]['P'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['P']

            except KeyError:

                try:
                    RPM = alternative_RPM1
                    RPM_dict[str(propeller)]['T'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['T']
                    RPM_dict[str(propeller)]['P'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['P']

                except KeyError:
                    RPM = alternative_RPM2
                    RPM_dict[str(propeller)]['T'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['T']
                    RPM_dict[str(propeller)]['P'] = input_dict[propeller][' '.join(['RPM', str(RPM)])]['P']

        t_tab = [[] for z in range(len(acceptable_sizes))]
        p_tab = [[] for y in range(len(acceptable_sizes))]

        i = 0

        for item in acceptable_sizes:
            for prop in input_dict.keys():

                current_label = self.get_label(prop)  # here you get 10,10,10,11

                if current_label == item:

                    t_tab[i].append(RPM_dict[str(prop)]['T'])
                    p_tab[i].append(RPM_dict[str(prop)]['P'])

                else:
                    continue

            i += 1

        return RPM_dict, t_tab, p_tab

    def select_65thrust(self, input_dict, final_dict):

        for propeller in input_dict.keys():

            final_dict[str(propeller)] = {}
            # among the available RPMs you want to select a middle / upper range. So:
            # 1 check which RPMs exist for each (and are non empty)
            # 2 select the 4
            RPM_tabs = []  # a place to append RPMs
            RPM_values = []
            for rpm in input_dict[str(propeller)].keys():

                if input_dict[propeller][rpm]:  # there should be no more empty ones but it's an extra check!
                    RPM_tabs.append(rpm)  # now it should give you a list of RPMs

            for value in RPM_tabs:
                number = value[4:]
                RPM_values.append(int(number))

            selected_RPM = RPM_values[-6]  # TODO MAKE IT EASIER TO FIND WHERE TO CHANGE
            final_dict[str(propeller)]['T'] = input_dict[propeller][' '.join(['RPM', str(selected_RPM)])]['T']
            final_dict[str(propeller)]['P'] = input_dict[propeller][' '.join(['RPM', str(selected_RPM)])]['P']

        thrust_tab = [[] for z in range(len(acceptable_sizes))]
        power_tab = [[] for y in range(len(acceptable_sizes))]

        counter = 0

        for val in acceptable_sizes:
            for curr_prop in final_dict.keys():

                this_label = self.get_label(curr_prop)

                if this_label == val:
                    thrust_tab[counter].append(final_dict[str(curr_prop)]['T'])
                    power_tab[counter].append(final_dict[str(curr_prop)]['P'])
                else:
                    continue

            counter += 1

        return final_dict, thrust_tab, power_tab

    def get_propellers_atvelocity(self, v_sizing, input_propellerdict, final_dict):

        for outside_keys in input_propellerdict.keys():  # iterate through propeller names that got into dictionary

            final_dict[str(outside_keys)] = {}  # Must create the dictionaries as well

            for inside_key in input_propellerdict[str(outside_keys)].keys():

                final_dict[str(outside_keys)][
                    str(inside_key)] = {}  # Must create the dictionaries as well (will make it empty tho)

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


class Plotting:

    def __init__(self):
        pass

    def make_plot(self, xlim, P_lim, T_single, t_tab, p_tab):
        """Add colors if necessary if you want to plot more data!"""

        color_list_complete = ['#bcd025', '#000000', '#ef8114', '#b01b81', '#f7d019', '#482776', '#3cbfbe', '#c3312f',
                               '#611089']

        color_list = color_list_complete[:len(p_tab)]  # only select as many colors as points you are plotting

        fig, ax = plt.subplots(1, 1)

        index = 0

        for i in range(0, len(color_list)):  # Make the plot for each label

            ax.scatter(t_tab[index], p_tab[index], label=acceptable_sizes[index],
                       color=color_list[index])  # check that index stays the same cause it wont

            index += 1

        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.88, box.height])
        ax.axvspan(T_single, xlim, color='#beafd0', label='Single \n Config. \n Thrust \n Required', alpha=0.25)
        ax.legend(ncol=1, loc='center left', bbox_to_anchor=(1, 0.5))
        ax.grid()
        ax.set_xlim(20, xlim)
        ax.set_ylim(0, P_lim)
        ax.set_xlabel("Thrust [N]")
        ax.set_ylabel("Power [W]")
        ax.set_title('Thrust given by APC propellers for v = 4 [m/s] @ optimum RPMs', loc='left')

        return plt.show(), fig

    def save_plot(self, location_name, figure):
        save_figure = PdfPages(str(location_name))
        figure.savefig(save_figure, dpi=300, format='pdf', transparent=True)
        save_figure.close()

        return 'Figure saved'


def load_prop_dictionary():
    open_file = open('data.pkl', 'rb')
    APC_propellers = pickle.load(open_file)
    open_file.close()
    return APC_propellers


def inches_to_meters(inc):
    """Because I keep forgetting the conversion factor and I am tired of googling it"""

    return inc * 0.0254


'''-----------------------RUNNING CODE -----------------------------'''

if __name__ == '__main__':
    APC_dictionary = load_prop_dictionary()
    acceptable_sizes = ['14']

    small_propeller_dict = {}
    rpms = {}
    smoothing = DatabaseAnalysis(APC_dictionary)
    small_prop = smoothing.get_propellers_smaller_than(acceptable_sizes, small_propeller_dict)
    final_props = smoothing.select_65thrust(small_prop, rpms)
    print(rpms['14x7'])
    graphs = Plotting()
    plot = graphs.make_plot(80, 2000, 31.4, final_props[1], final_props[2])[0]

    figure = graphs.make_plot(90, 2000, 31.4, final_props[1], final_props[2])[1]

    # saving_location = 'C:\\Users\\jlari\\Desktop\\Drones Design Resources\\Documentation on design choices\\Pictures for documentation'
    # fig_name = '\\APCProp_4ms_RPM[-6]'
    # saving_name = ''.join([saving_location,fig_name,'.pdf'])
    # savefigure = graphs.save_plot(saving_name, figure)

    print('12 inches is a diameter of', np.round(inches_to_meters(12), 3), 'm')
    print('11 inches is a diameter of', np.round(inches_to_meters(11), 3), 'm')
    print('10 inches is a diameter of', np.round(inches_to_meters(10), 3), 'm')
