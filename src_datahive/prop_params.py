"""
Author: @jlarija
This part of the code only reads and stores the data of the propeller files, which ideally should all be in one
directory.
"""
import os
import csv
import sys
import pickle
import numpy as np

class ReadData:

    def __init__(self, RPM):

        self.RPM  = RPM


    def get_apc_prop(self): #old files
        with open('complete_prop_dict', 'rb') as pickle_file:
            dict = pickle.load(pickle_file)
            return dict

    def filter_propellers_varyTFixRPM(self, all_props):
        prop_samples = ['10x10E', '12x115', '13x45MR', '14x6', '15x13', '16x11', '17x18', '18x10']
        new_props = {}

        for name in prop_samples:
            new_props[str(name)] = all_props[str(name)]

        return new_props

    def filter_propellers_varyDiameter(self, all_props):
        prop_samples = ['10x10', '11x10', '12x10', '13x10', '14x10', '15x10', '16x10', '17x10', '18x10']
        new_props = {}

        for name in prop_samples:
            new_props[str(name)] = all_props[str(name)]

        return new_props

    def varyTFixRPM(self):

        filtered_props = {}

        input_props = self.filter_propellers_varyTFixRPM(self.get_apc_prop())

        for propname_key in input_props.keys():
            filtered_props[str(propname_key)] = {}

            for rpm_key in input_props[str(propname_key)].keys():
                if rpm_key == ' '.join(['RPM', str(self.RPM)]):

                    filtered_props[str(propname_key)] = {}
                    filtered_props[str(propname_key)] = input_props[str(propname_key)][str(rpm_key)]


        #now choose a range of thrusts for the analysis (especially cause if you use T[0] you divide by 0

            filtered_props[str(propname_key)]['T'] = \
                filtered_props[str(propname_key)]['T'][5:15]
            filtered_props[str(propname_key)]['v'] = \
                filtered_props[str(propname_key)]['v'][5:15]
            filtered_props[str(propname_key)]['P'] = \
                filtered_props[str(propname_key)]['P'][5:15]

            # the torque is not needed
            del filtered_props[str(propname_key)]['M']


        return filtered_props, print('Selected RPM is', self.RPM)

    def varyDiameter(self):

        filtered_props = {}
        vtab = []
        ttab = []
        ptab = []

        input_props = self.filter_propellers_varyDiameter(self.get_apc_prop())

        for propname_key in input_props.keys():
            filtered_props[str(propname_key)] = {}

            for rpm_key in input_props[str(propname_key)].keys():
                if rpm_key == ' '.join(['RPM', str(self.RPM)]):
                    filtered_props[str(propname_key)] = {}
                    filtered_props[str(propname_key)] = input_props[str(propname_key)][str(rpm_key)]


            index = [15] # take the half field since you cant select a thrust due to the change in dimensions.
            #having the same pitch should take care of the fact that only the diameter is being increased

            t = filtered_props[str(propname_key)]['T'][index]
            p = filtered_props[str(propname_key)]['P'][index]
            v = filtered_props[str(propname_key)]['v'][index]

            ttab.append(t)
            ptab.append(p)
            vtab.append(v)


        return ttab, ptab, vtab


if __name__ == "__main__":

    prop_data = ReadData(5000)

    #load dictionary
    _varyT = prop_data.varyTFixRPM()

    #load all propellers
    all_props = prop_data.varyDiameter(10)