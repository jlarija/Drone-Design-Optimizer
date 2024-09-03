"""Author: @jlarija
The code is meant to calculate all the inputs parameters for CRotor, as well as some  quantities that can be useful for sizing a rotor. These are:
- the critical Mach number which is important for the aerodynamics input parameters;
- A plot of the rotor radius versus the required Power for a certain Thrust. This can help not inputting random values of power and radius if we know what kind of thrust we want to achieve. Of course it's simplistic as RPM matters too!
- An approximation of the flow angle phi to determine whether the blade is at too high angle (whereby stall happens).
 """

import numpy as np
from matplotlib import pyplot as plt


def calculate_mcrit(gamma, cpmin, airfoiltype):
    """
    Calculates critical Mach number. No compressibility is taken into account yet because XRotor also applies compressibility corrections.
    Theory behind the calculation is from Fundamental of Aerodynamics by Anderson. Inputs:
    gamma       : air ratio (cp/cv)
    cpmin       : minimum pressure coefficient on the suction side at an angle of attack of zero, for low speeds.
    airfoiltype : just for naming purposes, represents which airfoil is being used.
    """

    m_crit = np.linspace(0.2, 0.9, 30)
    cp_cr = (((1 + ((gamma - 1) / 2) * m_crit ** 2) / (1 + ((gamma - 1) / 2))) ** (gamma / (gamma - 1)) - 1) * (
            2 / (gamma * m_crit ** 2))
    cp = cpmin / np.sqrt(1 - m_crit ** 2)
    plt.plot(m_crit, cp_cr, label='Cp,cr = f(M,cr)', color='#00A6D6', marker='d')
    plt.plot(m_crit, cp, label='Cp,0 corrected', color='#82d7c6', marker='^')
    plt.legend()
    plt.ylabel('$C_p$')
    plt.xlabel('$M_{cr}$')
    plt.title(' '.join(['Determination of Critical Mach Number for', str(airfoiltype)]))
    plt.grid()
    plt.gca().invert_yaxis()
    intersection = np.argwhere(np.diff(np.sign(cp_cr - cp))).flatten()
    return plt.show(), print('Critical Mach from the graph for', str(airfoiltype), m_crit[intersection + 1])


def calculate_phi(v, RPM, r):
    """
    Calculates the angle of the flow wrt the rotor. An optimum angle should be betweem 10 and 40 degrees. Else chances are it will stall.
    See documentation for more information. Inputs:
    v   : freestream velocity
    RPM : rotor's RPM
    r   : rotor's radius
    """

    phi = np.arctan(v / (RPM * r * np.pi / 30))

    return np.rad2deg(phi)


"""----------------- RUNNING CODE --------------------- """

if __name__ == "__main__":
    """ 1: Give the critical numbers and show the graph where the calculation comes from """

    GOE225_M_crit = calculate_mcrit(1.4, -1.1575, 'GOE225')[1]
    WORTMANN_M_crit = calculate_mcrit(1.4, -1.0453, 'WORTMANN')[1]

    """ 2: Plot of rotor area versus power for the required thrust """

    T_req = 65.1  # [N]

    r = np.linspace(0.05, 0.27, 20)  # [ m ]
    A = np.pi * r ** 2
    rho = 1.225
    P = T_req ** (3 / 2) / (np.sqrt(2 * rho * A))

    plt.plot(r, P, color='#00A6D6', marker='d')
    plt.ylabel('$P [W]$')
    plt.xlabel('r [m]')
    plt.title(''.join(['Rotor Radius and Ideal Required Power for T = ', str(T_req), ' [N]']))
    plt.grid()
    plt.show()

    """ 3: Give the angle phi for input values of velocity and RPM"""

    # Acceptable values will obviously depend on the portion of the blade that you are at. But such low
    # values, like 1 deg, help explain why the blade stalls so much at the root when you input strong RPMs!

    velocity = 4  # m/s
    RPM = np.arange(300, 12000, 5)
    r = 0.15

    phi = calculate_phi(velocity, RPM, r)
    plt.plot(RPM, phi, color='#007188', label='phi vs RPM')
    plt.fill_between(RPM, 10, 30, color='#99d28c', label='Acceptable values')
    plt.ylabel('$\phi$ [deg]')
    plt.xlabel('RPM')
    plt.title('Angle $\phi$ as a function of RPM for v = 4 [m/s]')
    plt.grid()
    plt.legend()
    plt.show()
