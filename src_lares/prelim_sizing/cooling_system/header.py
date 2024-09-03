# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 11:41:31 2021

@author: kiransripathy
"""

import numpy as np

import constants as const


class Fire_Suppressant:
    '''This is a class for modelling the payload requirement of fire suppressant.
    
    Declaration format: Fire_Suppressant(name, density_liquid, density_gas, boiling_point at 1 atm,
    specific_heat_liquid, specific_heat_gas, latent_heat)'''

    def __init__(self, name: str = "N/A", density_liquid: float = 0, density_gas: float = 0, boiling_point: float = 0,
                 specific_heat_liquid: float = 0, specific_heat_gas: float = 0, latent_heat: float = 0):

        self.name = name  # []
        self.density_liquid = density_liquid  # [kg/m^3]
        self.density_gas = density_gas  # [kg/m^3]
        self.boiling_point = boiling_point  # [K]
        self.specific_heat_liquid = specific_heat_liquid  # [J/(kg K)]
        self.specific_heat_gas = specific_heat_gas  # [J/(kg K)]
        self.latent_heat = latent_heat  # [J/kg]
        self.fluid_volume = 0  # [m^3]

        if self.boiling_point > const.T_SL:
            self.storage_temp = const.T_SL

        else:
            self.storage_temp = boiling_point

    def required_volume(self, Room_obj):

        # Heat energy to cool room to target_temp
        room_heat = Room_obj.air_density() * Room_obj.volume() * const.CP_AIR * (
                    Room_obj.room_temp - Room_obj.target_temp)

        # if target_temp is of fundamental data type
        if isinstance(Room_obj.target_temp, (int, float)):

            if Room_obj.target_temp < self.boiling_point:
                self.fluid_volume = room_heat / (self.density_liquid * self.specific_heat_liquid * (
                            Room_obj.target_temp - self.storage_temp))

            else:
                self.fluid_volume = room_heat / (self.density_liquid * (
                            self.specific_heat_liquid * (self.boiling_point - self.storage_temp) +
                            self.latent_heat + self.specific_heat_gas * (Room_obj.target_temp - self.boiling_point)))

            return self.fluid_volume

        # if target_temp is of derived data type (numpy array)
        else:

            fluid_volume_array = np.zeros(len(Room_obj.target_temp))

            for i in range(len(Room_obj.target_temp)):

                if Room_obj.target_temp[i] < self.boiling_point:
                    fluid_volume_array[i] = room_heat[i] / (self.density_liquid * self.specific_heat_liquid * (
                                Room_obj.target_temp[i] - self.storage_temp))

                else:
                    fluid_volume_array[i] = room_heat[i] / (self.density_liquid * (
                                self.specific_heat_liquid * (self.boiling_point - self.storage_temp) +
                                self.latent_heat + self.specific_heat_gas * (
                                            Room_obj.target_temp[i] - self.boiling_point)))

            return fluid_volume_array


class Room:
    '''This is a class for specifying the geometric and thermal properties of an enclosed space.
    
    Declaration format: Room(name, length, width, height, initial_room_temperature, desired_room_temperature)'''

    def __init__(self, name: str = "N/A", length: float = 0, breadth: float = 0, height: float = 0,
                 room_temp: float = 0, target_temp: float = 0):
        self.name = name  # []
        self.length = length  # [m]
        self.breadth = breadth  # [m]
        self.height = height  # [m]
        self.room_temp = room_temp  # [K]
        self.target_temp = target_temp  # [K]

    def volume(self):
        return self.length * self.breadth * self.height  # [m^3]

    def air_density(self):
        return const.P_SL / (const.R * self.room_temp)  # [kg/m^3]
