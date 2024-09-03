"""
(Co)Authors: @jlarija (re-organisation) and @minerva (found the paper + wrote it initially)

This is the starting point for the LARES design. Based on the weight of the payload, the fixed elements (such as batteries)
and the expected configuration, it calculates the maximum take off weight and the thrust required. On the sizing thrust,
the assumption is made that the T/W ratio is equal to 1.4. This is the correspondent of 65% throttle, which puts less
loads on the system compared to a sizing T/W ratio of 2. However, at 100% throttle (that is only to be sustained
at small intervals) T/W = 2.14. It also gives an initial estimate of current drawn from the battery and the mission time.

"""

import matplotlib.pyplot as plt
import numpy as np


class InitialEstimations:
    """Contains the functions used in the sizing of the drone."""

    def __init__(self, payloadweight, N_rotors, W_fixed_components, r_rot, V_nom, eta_b):
        self.W_PL = payloadweight
        self.N = N_rotors  # number of rotors
        self.W_fix = W_fixed_components
        self.r_rot = r_rot
        self.V_nom = V_nom
        self.eta_b = eta_b

    def preliminary_weight(self):
        """ Based on an iterative process, described in the reference paper, returns the MTOW"""

        global Wb_MTOW_0

        MTOW_1 = self.W_PL  # [g] Initial starting point of iteration
        MTOW_0 = self.W_PL / 0.4  # [g]
        k = 0  # [-] Iteration count

        while np.abs(1 - MTOW_1 / MTOW_0) > 0.0001:
            MTOW_1 = MTOW_0
            # Empty weight fraction
            We_MTOW_0 = 0.4666 * MTOW_0 ** (-0.02)
            # Battery weight fraction
            delta = 1  # Correction factor for battery weight fraction - might be useufl at later iterations
            Wb_MTOW_0 = 195.27 * MTOW_0 ** (-0.703) * delta
            MTOW_0 = (W_PL + W_fix) / (1 - We_MTOW_0 - Wb_MTOW_0)

            k += 1

        return np.round(MTOW_0, 2), Wb_MTOW_0

    def battery_estimate(self):
        """Just a simple and preliminary estimation of the required battery capacity."""

        Q_b = 0.008 * self.preliminary_weight()[0] * self.preliminary_weight()[1]  # # Battery capacity in [Ah] - LiPo

        return Q_b

    def propulsion(self):
        """Propulsion parameters for selected configuration"""

        G0 = 9.80665  # m/s^2
        T_req = self.preliminary_weight()[0] * G0 * 10 ** -3 / N  # [N] - Required thrust to sustain level flight

        A = np.pi * self.r_rot ** 2  # [m²] Rotor disk area

        kappa = 1.4  # [-] Allowance for excess thrust, which is the T/W.
        FM = 1 / 0.59  # [-] Figure of Merit, a measure of efficiency of the rotorcraft.
        P_req = kappa * FM * np.sqrt((T_req ** 3) / (2 * rho_fire * A))  # [W] Power required for one motor.

        T_act = FM ** (2 / 3) * T_req  # Required thrust accounting for losses
        P_max = P_req / 0.7  # [W] Maximum motor power required for efficiency purposes.

        A_draw = P_req / V_nom  # Current drawn

        t_avail = self.battery_estimate() / A_draw * DoD * eta_b * 3600  # Available flight time

        return T_act, P_max, t_avail, A_draw


def plots(r_rot, t_avail, P_max, A_draw):
    """ Makes the plots for the rotor"""

    plt.figure()
    plt.xlabel("Rotor radius [m]")
    plt.plot(r_rot, t_avail / 60, color="skyblue", label='Rotor radius vs Flight Time')
    plt.grid(axis='both')
    plt.legend()
    plt.ylabel("Time available [min]")
    plt.twinx()
    plt.plot(r_rot, A_draw, color="orange", label='Rotor radius vs Current Drawn')
    plt.ylabel("Current draw [A]")
    plt.legend()
    # plt.show()

    '''fig, axis = plt.subplots(1, 1)
    axis.plot(r_rot, P_max, color='black', label='Rotor radius vs Power required')
    axis.set_xlabel('Rotor Radius [m]')
    axis.set_ylabel('Power required [W]')
    axis.legend()'''

    return plt.show()


'''-----------------------RUNNING CODE -----------------------------'''

if __name__ == "__main__":
    # some constants
    RHO_SL = 1.225
    T_SL = 288.15
    P_SL = 101325
    G0 = 9.81
    R = 8.3145
    T_fire = 273.15 + 90  # [K]
    rho_fire = RHO_SL * 0.5  # [kg/m³] 50 % of real density
    W_PL = 4410  # [g] Payload weight
    N = 8  # [-] Amount of rotors
    r_rot = np.arange(0.08, 0.25, 0.01)  # [m] Rotor radius
    V_nom = 22.2  # [V] LiPo battery nominal voltage

    DoD = 0.80  # [-] Depth of Discharge
    eta_b = 0.95  # [-] Battery efficiency
    W_fix = 1000  # [g] Fixed weight (Payload fairing, sensors etc.)

    initial_LARES = InitialEstimations(W_PL, N, W_fix, r_rot, V_nom, eta_b)
    weight_LARES = initial_LARES.preliminary_weight()[0]  # g
    thrust_LARES = initial_LARES.propulsion()[0]

    print("With these data, the initial weight of LARES is", np.round(weight_LARES * 10 ** (-3), 2), "[Kg]")
    print("Required thrust per arm, assuming 8 arms:", np.round(thrust_LARES, 2), "[N]")
    plots = plots(r_rot, initial_LARES.propulsion()[1], initial_LARES.propulsion()[2], initial_LARES.propulsion()[3])
