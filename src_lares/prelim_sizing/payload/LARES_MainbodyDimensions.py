"""
Author: @jlarija
Main considerations: the coolant is a sphere with a radius of 9cm (so a total length of 18) but it will only be appended at the bottom! Which means that the
dimensions of the sides are only dependent on the fire masks and batteries buffer. This leaves some room for having bigger propellers, because we really
need them.
"""

import numpy as np


class Payload:
    """This class serves to calculate the amount of fire masks, and whenever thats going to be possible, of coolant, that can be brought onboard
    based on the dimensions of the main body.
    Inputs:
    Number of face masks stacked vertically (n_vertical)
    Number of face masks stacked horizontally (n_horizontal)
    (for later) weight + volume of coolant.
    Everything in SI Units"""

    def __init__(self):
        pass

    def fire_masks_volume(self, n_vertical, n_horizontal):
        """Data reported here comes from DSE report, which in turn is taken from bol.com for a firemask"""
        horiz_dimension = n_horizontal * 0.14  # [m]
        vert_dimension = n_vertical * 0.08
        depth = 0.16  # Standard depth
        weight = 0.482 * (n_vertical + n_horizontal)  # g
        return horiz_dimension, vert_dimension, depth, weight

    def coolant_volume(self, rad):
        radius = rad
        weight = 2.001  # kg
        return radius, weight

    def battery_dimensions(self):  # Eventually add in the battery dimensions
        pass


class Material:
    """Everything in SI units"""

    def __init__(self, duct_height, duct_radius, duct_thickness, MB_height, MB_width, MB_platethickness, MB_depth,
                 Nducts):
        self.duct_height = duct_height
        self.duct_radius = duct_radius
        self.MB_height = MB_height
        self.MB_width = MB_width
        self.duct_thickness = duct_thickness
        self.MB_platethickness = MB_platethickness
        self.MB_depth = MB_depth
        self.Nducts = Nducts

    def aluminium(self):
        density = 2710  # kg/m^3
        duct_weight = (self.duct_radius ** 2 - (
                    self.duct_radius - self.duct_thickness) ** 2) * self.duct_height * density * np.pi * self.Nducts
        MB_weight = self.MB_platethickness * self.MB_height * self.MB_width * density * 4 + self.MB_depth * self.MB_width * self.MB_platethickness * 2 * density

        return duct_weight + MB_weight

    def carbon_fiber(self):
        density = 1750  # kg/m^3
        duct_weight = (self.duct_radius ** 2 - (
                    self.duct_radius - self.duct_thickness) ** 2) * self.duct_height * density * np.pi * self.Nducts
        MB_weight = self.MB_platethickness * self.MB_height * self.MB_width * density * 4 + self.MB_depth * self.MB_width * self.MB_platethickness * 2 * density

        return duct_weight + MB_weight


"""-------RUNNING CODE----------"""

if __name__ == '__main__':
    battery_estimation = 0.05  # Extra buffer to account for stuff that may not be in my payload estimation as well as required  insulation (if any)
    mainbody_dimensions = Payload()
    total_horiz_measure = mainbody_dimensions.fire_masks_volume(3, 2)[0] + battery_estimation
    total_vertical_measure = mainbody_dimensions.fire_masks_volume(3, 2)[1] + battery_estimation
    total_depth = mainbody_dimensions.fire_masks_volume(3, 2)[2] + mainbody_dimensions.coolant_volume(9 * 10 ** (-2))[
        0] + battery_estimation
    payload_weight = mainbody_dimensions.fire_masks_volume(3, 2)[3] + \
                     mainbody_dimensions.coolant_volume(7.8 * 10 ** (-2))[1]
    print("Main Body Dimensions:", total_horiz_measure, "[m] x", total_vertical_measure, "[m] x", total_depth,
          "[m] (horizxvertxdepth)")
    print("Weight of Payload", payload_weight, "kg")

    drone = Material(duct_height=0.15, duct_radius=0.1725, duct_thickness=0.001, MB_height=0.33, MB_width=0.33,
                     MB_platethickness=0.002, MB_depth=0.290, Nducts=4)
    option_1_alu = drone.aluminium()
    option_2_cf = drone.carbon_fiber()

    print()

    print("Aluminium mainframe+ducts:", np.round(option_1_alu, 2), "[KG]")
    print("Carbon Fiber mainframe+ducts:", np.round(option_2_cf, 2), "[KG]")
    print()

    drone_2 = Material(duct_height=0.15, duct_radius=1.02, duct_thickness=0.001, MB_height=0.33, MB_width=0.33,
                       MB_platethickness=0.002, MB_depth=0.290, Nducts=1)
    option_3_alu = drone_2.aluminium()
    option_4_cf = drone_2.carbon_fiber()

    print("Aluminium mainframe+1duct:", np.round(option_3_alu, 2), "[KG]")
    print("Carbon Fiber mainframe+1duct:", np.round(option_4_cf, 2), "[KG]")
