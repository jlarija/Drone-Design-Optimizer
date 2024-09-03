import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Required data for the propeller weight (that defines the loads)
# TODO add to propeller code the torque as a reading and figure what that torque actually is
"""Assumption: you are calculating the weight of the propeller that is the best combination already - so the file is selected as such"""


class Stresses:
    """Calculates the stresses and strains in the propeller arm"""

    def __init__(self, thrust_upper: float = 0, thrust_lower: float = 0, thrust_single: float = 0,
                 prop_weight: float = 0, motor_weight: float = 0, torque: float = 0,
                 # Loads
                 E_modulus: float = 0, sigma_yield: float = 0, mat_density: float = 0, shear_strength: float = 0,
                 G_rigidity: float = 0,
                 prop_radius: float = 0, motor_dim: float = 0, safety_factor: float = 1.5):
        self.thrust_upper = thrust_upper
        self.thrust_lower = thrust_lower
        self.thrust_single = thrust_single
        self.prop_weight = prop_weight
        self.motor_weight = motor_weight
        self.torque = torque
        self.E_modulus = E_modulus
        self.sigma_yield = sigma_yield
        self.mat_density = mat_density
        self.shear_strength = shear_strength
        self.G_rigidity = G_rigidity
        self.prop_radius = prop_radius
        self.motor_dim = motor_dim
        self.safety_factor = safety_factor

    def vertical_arm_sizing(self):  # Independent of configuration since we take upper propeller thrust anyways

        global mass, sigmatension, buck

        L_vertical = self.prop_radius
        cross_section = self.motor_dim * 1.25  # For clearance, air, heating and whatnot
        d_min_inner = cross_section  # [m] Random starting point for iteration
        d_min_outer = 0.1  # [m] -> starting value / it hopefully gets smaller
        F_max = self.thrust_upper - self.prop_weight  # This is the highest force and doesnt matter if single or corotating
        decrement = 0.002

        while d_min_outer > d_min_inner:

            area = 0.25 * np.pi * d_min_outer ** 2 - 0.25 * np.pi * d_min_inner ** 2
            mass = area * L_vertical * self.mat_density
            Ixx = np.pi / 64 * (d_min_outer ** 4 - d_min_inner ** 4)
            sigmatension = F_max / area
            sigmabend = (d_min_outer / 2) * (F_max * 2) * L_vertical / (4 * Ixx)
            K = 2
            Pcrit = np.pi * self.E_modulus * Ixx / ((K * L_vertical) ** 2)

            sigma_allowable_tension = self.sigma_yield * self.safety_factor
            sigma_allowable_bending = self.sigma_yield * self.safety_factor

            if abs(sigmatension) < sigma_allowable_tension and F_max < Pcrit and abs(
                    sigmabend) < sigma_allowable_bending:
                d_min_outer = d_min_outer - decrement

            else:
                return d_min_inner, d_min_outer, mass

        return d_min_inner, d_min_outer, mass, "outside of while"  # This return is more in the case that the while stops so it's for me to have a bit of troubleshooting

    def horizontal_arm_sizing(self, configuration):  # Configuration expects either coaxial or single as input

        global param0, param1, param2  # Required since they are inside a if loop, but have to be accessed later

        d_min_outer = 0.1  # [m] # Todo are there constraints on minimum inner diameter?
        d_min_inner = 0.07
        L_horizontal = 1.25 * self.prop_radius
        decrement = 0.002

        while d_min_outer > d_min_inner:

            area = 0.25 * np.pi * d_min_outer ** 2 - 0.25 * np.pi * d_min_inner ** 2
            mass = area * L_horizontal * self.mat_density
            Ixx = np.pi / 64 * (d_min_outer ** 4 - d_min_inner ** 4)

            # This part will only be valid for coaxial propellers because it takes the two thrusts.
            if str(configuration) == 'Coaxial' or str(configuration) == 'coaxial':
                param0 = self.thrust_upper
                param1 = self.thrust_lower
                param2 = 2


            elif str(configuration) == 'Single' or str(configuration) == 'single':
                param0 = self.thrust_single
                param1 = 0
                param2 = 1

            Az = param0 + param1 - self.prop_weight - self.motor_weight
            Mxa = Az * 0.5 * self.vertical_arm_sizing()[1]
            Mza = self.torque * param2
            Mxb = Mxa - Az * L_horizontal
            Mzb = Mza
            K = 2
            r = np.sqrt(Ixx / area)
            sigma_buck = np.pi ** 2 * self.E_modulus / ((K * L_horizontal / r) ** 2)
            Pcrit = np.pi * self.E_modulus * Ixx / ((K * L_horizontal) ** 2)  # [N] Critical buckling force

            # In normal flight conditions
            sigma1 = Mxb * (d_min_outer / 2) / Ixx
            sigma2 = Mzb * (d_min_outer / 2) / Ixx

            # In the case of maneuvres up to 90 deg (more of a safety factor, but then thrust will be inclined)
            alpha = np.radians(90)
            Wpropmot_buck = np.cos(alpha) * (self.prop_weight + self.motor_weight)
            Wpropmot_bend = np.sin(alpha) * (self.prop_weight + self.motor_weight)
            sigma3 = (Wpropmot_bend * L_horizontal) * (d_min_outer / 2) / Ixx
            Wpropmot_ten = Wpropmot_buck
            sigma4 = Wpropmot_ten / area
            sigma5 = ((self.prop_weight + self.motor_weight) * L_horizontal) * (d_min_outer / 2) / Ixx
            max_stress = np.max([sigma1, sigma2, sigma3, sigma4, sigma5])

            if max_stress < (self.sigma_yield * self.safety_factor) and Az < Pcrit and max_stress < (
                    sigma_buck / self.safety_factor):
                d_min_outer = d_min_outer - decrement
            else:
                return d_min_outer, d_min_inner, mass, L_horizontal

        else:
            return "Re-read required input for configuration parameter. Either Single or Coaxial"


#
# Thrust, Weight to be  imported from LARES_Crotor and battery file.py
# Here are functions
def calculate_weight_oneblade(file, fileloc, radius, density):
    file_best_prop_upper = ''.join([fileloc, file, '.txt'])

    data_upper_rotor = pd.read_fwf(str(file_best_prop_upper), skiprows=31, index_col=False,
                                   names=['row index', 'r/R', 'c/R', 'beta(deg)', 'CL', 'CD', 'Rex10^3', 'Mach',
                                          'efficiency', 'effp', 'na.u/U'])

    # Retrieve only the relevant sections: the radial sections of the prop and the chord length at said stations
    r_R = data_upper_rotor['r/R']
    c_R = data_upper_rotor['c/R']
    r_upper = radius
    c = c_R * r_upper

    # remove the first element and add a 1 at the end for the subtraction, so to have the little elements required for the weights
    rem_firstel = r_R[1:]
    add = pd.Series(1)
    add_lastel = rem_firstel.append(add, ignore_index=True)  # array with a one in the end and no first element

    elements_width_minusfirst = add_lastel - r_R  # I have manually checked the result and it makes sense, mathematically it is correct
    array_elements = elements_width_minusfirst.to_numpy()
    elements_width = np.insert(array_elements, 0, r_R[0])  # Final numpy array of elements
    r_R = r_R.to_numpy()
    volumes = []

    for i in range(0, len(r_R)):
        if float(r_R[i]) < 0.11 or float(r_R[i]) > 0.9:
            r_wortmann = 0.126 / 2 * float(c[i])
            area0 = np.pi * r_wortmann ** 2 * 0.5 + 0.5 * r_wortmann / 2 * (c[i] - r_wortmann / 2)
            volume0 = area0 * elements_width[i]
            volumes.append(volume0)
        elif 0.11 < float(r_R[i]) < 0.90:
            r_goe225 = 0.128 / 2 * float(c[i])
            area1 = np.pi * r_goe225 ** 2 * 0.5 + 0.5 * r_goe225 / 2 * (c[i] - r_goe225 / 2)
            volume1 = area1 * elements_width[i]
            volumes.append(volume1)

    total_volume = np.sum(volumes)
    total_weight = total_volume * density

    return total_weight


def circle_line_segment_intersection(circle_center, circle_radius, pt1, pt2, full_line=True, tangent_tol=1e-9):
    """ Find the points at which a circle intersects a line-segment.  This can happen at 0, 1, or 2 points.

    :param circle_center: The (x, y) location of the circle center
    :param circle_radius: The radius of the circle
    :param pt1: The (x, y) location of the first point of the segment
    :param pt2: The (x, y) location of the second point of the segment
    :param full_line: True to find intersections along full line - not just in the segment.  False will just return intersections within the segment.
    :param tangent_tol: Numerical tolerance at which we decide the intersections are close enough to consider it a tangent
    :return Sequence[Tuple[float, float]]: A list of length 0, 1, or 2, where each element is a point at which the circle intercepts a line segment.

    Note: We follow: http://mathworld.wolfram.com/Circle-LineIntersection.html
    """

    (p1x, p1y), (p2x, p2y), (cx, cy) = pt1, pt2, circle_center
    (x1, y1), (x2, y2) = (p1x - cx, p1y - cy), (p2x - cx, p2y - cy)
    dx, dy = (x2 - x1), (y2 - y1)
    dr = (dx ** 2 + dy ** 2) ** .5
    big_d = x1 * y2 - x2 * y1
    discriminant = circle_radius ** 2 * dr ** 2 - big_d ** 2

    if discriminant < 0:  # No intersection between circle and line
        return []
    else:  # There may be 0, 1, or 2 intersections with the segment
        intersections = [
            (cx + (big_d * dy + sign * (-1 if dy < 0 else 1) * dx * discriminant ** .5) / dr ** 2,
             cy + (-big_d * dx + sign * abs(dy) * discriminant ** .5) / dr ** 2)
            for sign in ((1, -1) if dy < 0 else (-1, 1))]  # This makes sure the order along the segment is correct
        if not full_line:  # If only considering the segment, filter out intersections that do not fall within the segment
            fraction_along_segment = [(xi - p1x) / dx if abs(dx) > abs(dy) else (yi - p1y) / dy for xi, yi in
                                      intersections]
            intersections = [pt for pt, frac in zip(intersections, fraction_along_segment) if 0 <= frac <= 1]
        if len(intersections) == 2 and abs(
                discriminant) <= tangent_tol:  # If line is tangent to circle, return just one point (as both intersections have same location)
            return [intersections[0]]
        else:
            return intersections


def do_we_fit_through_the_window_plot(D_mainbody8, L_mainbody8, mainbody_og, mainbody_iter, arm_og, arm_iter,
                                      prop_diam_og, prop_diam_iter, L_mainbody, D_mainbody, prop_diam_8blades):
    mainbody_og_circle = plt.Circle((0, 0), mainbody_og, color='b', fill=False, linestyle='dotted')

    intersection_point_mainbody_OG = circle_line_segment_intersection((0, 0), float(mainbody_og), (0, 0), (5, 5))
    print(intersection_point_mainbody_OG)
    intersection_point_mainbody_iter = circle_line_segment_intersection((0, 0), float(mainbody_iter), (0, 0), (5, 5))
    finalpoint_arm_OG = intersection_point_mainbody_OG[1] + arm_og * np.cos(np.radians(45))
    finalpoint_arm_iter = intersection_point_mainbody_iter[1] + arm_iter * np.cos(np.radians(45))

    spacing_factor = 1
    finalpoint_arm_8blades = intersection_point_mainbody_iter[1] + arm_iter * spacing_factor * np.cos(np.radians(45))

    fig, ax = plt.subplots()
    ax.add_patch(mainbody_og_circle)

    x = np.linspace(0, finalpoint_arm_OG[0], 20)
    x_iter = np.linspace(0, finalpoint_arm_iter[0], 20)
    x_8blades = np.linspace(0, finalpoint_arm_8blades[0], 20)

    ax.plot(x, x, color='b', linestyle='dotted', label='Original LARES')
    ax.plot(-x, -x, color='b', linestyle='dotted')
    ax.plot(-x, x, color='b', linestyle='dotted')
    ax.plot(x, -x, color='b', linestyle='dotted')

    ax.plot(x_iter, x_iter, color='r', label='Current iteration')
    ax.plot(-x_iter, -x_iter, color='r')
    ax.plot(-x_iter, x_iter, color='r')
    ax.plot(x_iter, -x_iter, color='r')

    fig2, ax2 = plt.subplots()
    ax2.plot(x_8blades, x_8blades, color='g', label='8 blades')
    ax2.plot(-x_8blades, -x_8blades, color='g')
    ax2.plot(-x_8blades, x_iter, color='g')
    ax2.plot(x_8blades, -x_8blades, color='g')
    '''ax2.hlines(0, -finalpoint_arm_8blades[0], +finalpoint_arm_8blades[0], color = 'g')
    ax2.vlines(0,-finalpoint_arm_8blades[0], +finalpoint_arm_8blades[0], color = 'g')'''

    propeller_circles_8blades = plt.Circle((finalpoint_arm_8blades[0], finalpoint_arm_8blades[0]), prop_diam_8blades,
                                           color='g',
                                           fill=False)
    propeller_circles1_8blades = plt.Circle((-finalpoint_arm_8blades[0], finalpoint_arm_8blades[0]), prop_diam_8blades,
                                            color='g',
                                            fill=False)
    propeller_circles2_8blades = plt.Circle((finalpoint_arm_8blades[0], -finalpoint_arm_8blades[0]), prop_diam_8blades,
                                            color='g',
                                            fill=False)
    propeller_circles3_8blades = plt.Circle((-finalpoint_arm_8blades[0], -finalpoint_arm_8blades[0]), prop_diam_8blades,
                                            color='g',
                                            fill=False)
    propeller_circles4_8blades = plt.Circle((0, finalpoint_arm_8blades[0]), prop_diam_8blades, color='g',
                                            fill=False)
    propeller_circles5_8blades = plt.Circle((-finalpoint_arm_8blades[0], 0), prop_diam_8blades, color='g',
                                            fill=False)
    propeller_circles6_8blades = plt.Circle((finalpoint_arm_8blades[0], 0), prop_diam_8blades, color='g',
                                            fill=False)
    propeller_circles7_8blades = plt.Circle((0, -finalpoint_arm_8blades[0]), prop_diam_8blades, color='g',
                                            fill=False)

    '''ax2.vlines(D_mainbody / 2, L_mainbody / 2, - L_mainbody / 2, color='r', label = 'Coaxial')
    ax2.vlines(-D_mainbody / 2, L_mainbody / 2, - L_mainbody / 2, color='r')
    ax2.hlines(L_mainbody / 2, D_mainbody / 2, - D_mainbody / 2, color='r')
    ax2.hlines(-L_mainbody / 2, D_mainbody / 2, - D_mainbody / 2, color='r')'''
    ax2.vlines(D_mainbody8 / 2, L_mainbody8 / 2, - L_mainbody8 / 2, color='g', )
    ax2.vlines(-D_mainbody8 / 2, L_mainbody8 / 2, - L_mainbody8 / 2, color='g')
    ax2.hlines(L_mainbody8 / 2, D_mainbody8 / 2, - D_mainbody8 / 2, color='g')
    ax2.hlines(-L_mainbody8 / 2, D_mainbody8 / 2, - D_mainbody8 / 2, color='g')

    ax2.add_patch(propeller_circles_8blades)
    ax2.add_patch(propeller_circles1_8blades)
    ax2.add_patch(propeller_circles2_8blades)
    ax2.add_patch(propeller_circles3_8blades)
    '''ax2.add_patch(propeller_circles4_8blades)
    ax2.add_patch(propeller_circles5_8blades)
    ax2.add_patch(propeller_circles6_8blades)
    ax2.add_patch(propeller_circles7_8blades)'''

    propeller_circles_OG = plt.Circle((finalpoint_arm_OG[0], finalpoint_arm_OG[0]), prop_diam_og, color='b', fill=False,
                                      linestyle='dotted')
    propeller_circles1_OG = plt.Circle((-finalpoint_arm_OG[0], finalpoint_arm_OG[0]), prop_diam_og, color='b',
                                       fill=False, linestyle='dotted')
    propeller_circles2_OG = plt.Circle((finalpoint_arm_OG[0], -finalpoint_arm_OG[0]), prop_diam_og, color='b',
                                       fill=False, linestyle='dotted')
    propeller_circles3_OG = plt.Circle((-finalpoint_arm_OG[0], -finalpoint_arm_OG[0]), prop_diam_og, color='b',
                                       fill=False, linestyle='dotted')

    propeller_circles_iter = plt.Circle((finalpoint_arm_iter[0], finalpoint_arm_iter[0]), prop_diam_iter, color='r',
                                        fill=False)
    propeller_circles1_iter = plt.Circle((-finalpoint_arm_iter[0], finalpoint_arm_iter[0]), prop_diam_iter, color='r',
                                         fill=False)
    propeller_circles2_iter = plt.Circle((finalpoint_arm_iter[0], -finalpoint_arm_iter[0]), prop_diam_iter, color='r',
                                         fill=False)
    propeller_circles3_iter = plt.Circle((-finalpoint_arm_iter[0], -finalpoint_arm_iter[0]), prop_diam_iter, color='r',
                                         fill=False)

    '''ax.add_patch(propeller_circles_OG)
    ax.add_patch(propeller_circles1_OG)
    ax.add_patch(propeller_circles2_OG)
    ax.add_patch(propeller_circles3_OG)'''

    '''ax2.add_patch(propeller_circles_iter)
    ax2.add_patch(propeller_circles1_iter)
    ax2.add_patch(propeller_circles2_iter)
    ax2.add_patch(propeller_circles3_iter)'''

    "Standard window size"
    ax2.hlines(0.8, -0.4, 0.4, color='m', linestyle='dotted', label='Window Size - 80 cm')

    ax.set_xlabel('Dimensions [m]')
    ax.set_ylabel('Dimensions [m]')
    ax.set_xlim((-1.25, 1.25))
    ax.set_ylim((-1.25, 1.25))
    ax.set_title('LARES Drone dimensions compared to a std. window size of 80 [cm]')
    ax.legend()

    ax2.set_xlabel('Dimensions [m]')
    ax2.set_ylabel('Dimensions [m]')
    ax2.set_xlim((-1.25, 1.25))
    ax2.set_ylim((-1.25, 1.25))
    ax2.set_title('LARES Drone dimensions compared to a std. window size of 80 [cm]')
    ax2.legend()

    return plt.show()


def save_plot(location_name, figure):
    save_figure = PdfPages(str(location_name))
    figure.savefig(save_figure, dpi=300, format='pdf', transparent=True)
    save_figure.close()

    return 'Figure saved'


if __name__ == '__main__':
    """LARES dimensions DSE in [m]"""
    mainbody_og = 0.22  # m of main body
    arm_og = 0.58
    prop_diam_og = 0.34

    """These 3 values are the only thing that is going to change once we have a design. It can also be imported from other files ofc"""
    prop_diam_iter = 0.17
    prop_diam_8blades = 0.17
    mainbody_iter = 0.33 / 2
    arm_iter = 1.4 * prop_diam_iter

    loc = 'C:\\Users\\jlari\\Desktop\\Drones Design Resources\\Documentation on design choices\\Pictures for documentation'
    fig_name = '\\Dimensions_8blades.pdf'
    saving_name = ''.join([loc, fig_name])

    dasplot = do_we_fit_through_the_window_plot(0.29, 0.33, mainbody_og, mainbody_iter, arm_og, arm_iter, prop_diam_og,
                                                prop_diam_iter, 0.5387, 0.4187, prop_diam_8blades)
    # saving = save_plot(loc,dasplot)
