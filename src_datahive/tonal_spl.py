"""A basic code for aeroacoustics comparisons of propeller noise"""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})


from prop_params import ReadData

class ConvertUnits:
    """Freedom units suck, but that's what's in the formula"""

    def __init__(self):
        pass

    def m_to_ft(self, val):
        return val / 0.3048

    def in_to_ft(self, val):
        return 0.0833333 * val

    def mph_to_fts(self, val):
        return val * 1.46667

    def to_fts(self, val):
        return val * 1/0.3048

    def to_pounds(self, val):
        return val / 4.44822

    def to_hpw(self, val):
        return val / 745.7

class IndependentVariables:

    def __init__(self):
        pass

    def mode_number(self):
        return 1

    def blade_n(self):
        blades = 2
        return blades

    def r_distance(self):
        x_dist = 0
        y_dist = 5
        return x_dist, y_dist

    def cos_theta(self):
        return 1

    def z_eff(self):
        return 0.8

    @property
    def speed_sound(self):
        return 308.63 * 0.3048 #ft/s

class DependentVariables:

    def __init__(self,  chord, diameter, velocity, RPM):
        """User parameters"""

        self.x         = 0
        self.y         = 20
        self.c         = IndependentVariables().speed_sound
        self.B         = 2
        self.cos_theta = IndependentVariables().cos_theta()


        #Variables from files

        self.d   = diameter
        self.ch  = chord #the chord can only be found for the propellers that I have more data of
        self.v   = velocity
        self.RPM = RPM

    def flight_mach(self):
        return self.v / self.c

    def tip_mach(self):
        return self.RPM * (self.d/2) / self.c

    def psi(self):
        z = np.sqrt((self.x**2 + self.y**2)) / (self.d/2)
        m_r = self.flight_mach()**2 + self.tip_mach()**2 * z**2
        x = np.divide((1*self.B*self.tip_mach()* (self.ch/self.d)), (m_r * (1 - self.flight_mach() * self.cos_theta)))
        psi = np.sin(x)/x
        return psi

    def get_thrust_differences(self, input_thrust):

        # compute the differences of each thrust

        thrust_diff = {}


        for prop in input_thrust.keys():
            thrust_diff[prop] = {}
            t_tab = []

            for i in range(len(input_thrust[prop]['T'])):

                #take care of the out of bounds
                if i+1 < len(input_thrust[prop]['T']):
                    t_diff = np.round(input_thrust[prop]['T'][i+1] - input_thrust[prop]['T'][i], 4)
                    t_tab.append(t_diff)

                else:
                    break

            thrust_diff[prop] = t_tab

        return thrust_diff

    def power(self):

        ## read file of APC and get the power -> this should either be a read function, or an
        ## import function from somewhere else that reads the thrust (eg old lares code)
        return 200, 310

def spl_variable_thrust(cos_theta, z, Mt, c0, Mx1, Mx2, T_1, T_2, W_1, W_2, psi_1, psi_2):
    numerator = 1/(1- Mx1*cos_theta) * (cos_theta / (1- Mx1*cos_theta)*T_1 - 550/(z**2 * Mt**2 * c0)* W_1) * psi_1
    denominator = 1/(1- Mx2*cos_theta) * (cos_theta / (1- Mx2*cos_theta)*T_2 - 550/(z**2 * Mt**2 * c0)* W_2) * psi_2
    delta_spl = 20*np.log10(numerator / denominator)
    return delta_spl

def blade_passing_frequency(RPM, B):
    bpf = B * RPM / 60
    return bpf

def diameter_change_plot():
    fig, ax = plt.subplots()

    colors = ['#4477AA', '#EE6677', '#228833', '#CCBB44', '#66CCEE', '#AA3377', '#BBBBBB', '#000000']
    index = 0

    for i in range(len(t_diff)):
        _label = diameter_list
        ax = sns.lineplot(x=t_diff[index], y=spl_diff[index], label=diameter_list[index], marker='^',
                          color=colors[index])
        ax.set(xlabel='Change in Thrust [Lbf]', ylabel='Change in SPL [dB]',
               title='Correlation between Sound Power Level and Thrust for increasing diameter w fixed pitch')
        plt.legend(loc='upper right')
        index += 1

    ax.grid()
    plt.tight_layout()

    return plt.show()

def bpf_plot(rpm, B):
    bpf = blade_passing_frequency(rpm, B)
    sns.set(style='white')
    plt.style.use("classic")

    #plot part
    fig, ax = plt.subplots()
    colour = '#6ebbd5'

    ax = sns.lineplot(x=rpm, y=bpf, label='RPM vs BPF', marker = '^', color = 'black')
    ax.axhspan(500,550, label='Above Measured Frequency', facecolor='#82d7c6', alpha=0.5)
    ax.set(xlabel='RPM [1/min]', ylabel='Blade Passing Frequency [Hz]')
    ax.set_ylim(0,550)
    plt.legend(loc='lower right')

    return plt.show()

if __name__ == "__main__":

    # units to convert
    converter = ConvertUnits()
    indep_var = IndependentVariables()

    # import propeller data
    get_props = ReadData(RPM=5000)
    prop_params = get_props.varyDiameter()
    diameter_list = np.asarray([10,11,12,13,14,15,16,17,18])

    spl_diff = {}

    # thrust_diff = DependentVariables(1,1,1,5000).get_thrust_differences(prop_data) #thrust difference is computed correctly - it's for plotting

    for element in prop_params[0]: #for propeller in dict
        v = np.round(converter.mph_to_fts(np.asarray(prop_params[2])),2)
        P = prop_params[1] #p is already in horsepower hp
        T = prop_params[0] #T is already in pounds lbs

        spl_tab = []  # just an empty tab to append the spl values for each propeller

        for index in range(len(v)):


            if index + 1 < len(v):
                datapoint_1 = DependentVariables(1,diameter_list[index],v[index],5000) #for every velocity in the dictionary
                datapoint_2 = DependentVariables(1,diameter_list[index+1],v[index+1],5000) #for every velocity in the dictionary

                #compute SPL diff
                spl_change = spl_variable_thrust(indep_var.cos_theta(), indep_var.z_eff(), datapoint_1.tip_mach(),
                                                 indep_var.speed_sound,
                                                 datapoint_1.flight_mach(), datapoint_1.flight_mach(), T[index],
                                                 T[index+1], P[index], P[index+1],datapoint_1.psi(),datapoint_2.psi())
                spl_tab.append(spl_change)

            else:
                break

        spl_diff = spl_tab

    t_diff = []

    # calculate thrust differences
    for i in range(len(prop_params[0]) -1):
        diff = prop_params[0][i+1] - prop_params[0][i]
        t_diff.append(diff)

    # blade passing frequency plot
    rpm= np.arange(0,12000,1000)
    B = 2

    plot = bpf_plot(rpm,B)