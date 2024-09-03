# -*- coding: utf-8 -*-
"""
Created on Tue Sep 21 14:13:39 2021

@author: kiransripathy
"""

import matplotlib.pyplot as plt

import header as head

# Fire suppressant object declaration
water = head.Fire_Suppressant("Water", 1000, 0.59, 373.2, 4.19e3, 2.0267e3, 2260e3)
novec_1230 = head.Fire_Suppressant("Novec 1230", 1600, 13.6, 322.2, 1.103e3, 0.891e3, 88e3)
fe_25 = head.Fire_Suppressant("FE-25", 1530, 4.983, 224.86, 1.37e3, 0.809e3, 164.4e3)
fm_200 = head.Fire_Suppressant("FM-200", 1460, 7.1461, 256.66, 1.1816e3, 0.81327e3, 131.77e3)

# Room object declaration.
room1 = head.Room("Room-1", 5, head.np.arange(1, 6), 2.5, 343, 323)  # Array for room width input
room2 = head.Room("Room-2", 5, 2, 2.5, head.np.arange(333, 483, 10), 323)  # Array for initial room temp input
room3 = head.Room("Room-3", 5, 2, 2.5, 343, head.np.arange(323, 343, 2))  # Array for desired room temp input

# Plotting fluid volume vs area
fig1, ax1 = plt.subplots()
ax1.plot(room1.volume() / room1.height, water.required_volume(room1) * 1e3, 'r-',
         label=water.name + " initial_temp = 15 [C]")
ax1.plot(room1.volume() / room1.height, novec_1230.required_volume(room1) * 1e3, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax1.plot(room1.volume() / room1.height, fe_25.required_volume(room1) * 1e3, 'b-',
         label=fe_25.name + " initial_temp = -48 [C]")
ax1.plot(room1.volume() / room1.height, fm_200.required_volume(room1) * 1e3, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax1.set(xlabel="Room Area [m^2]", ylabel="Suppressant Volume [litre]",
        title="Room temperature 70 [C], Target temperature 50 [C]")
ax1.legend()
plt.grid()
plt.show()

# plotting fluid mass vs area
fig2, ax2 = plt.subplots()
ax2.plot(room1.volume() / room1.height, water.required_volume(room1) * water.density_liquid, 'r-',
         label=water.name + " initial_temp = 15 [C]")
ax2.plot(room1.volume() / room1.height, novec_1230.required_volume(room1) * novec_1230.density_liquid, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax2.plot(room1.volume() / room1.height, fe_25.required_volume(room1) * fe_25.density_liquid, 'b-',
         label=fe_25.name + " initial_temp = -48 [C]")
ax2.plot(room1.volume() / room1.height, fm_200.required_volume(room1) * fm_200.density_liquid, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax2.set(xlabel="Room Area [m^2]", ylabel="Suppressant mass [kg]",
        title="Room temperature 70 [C], Target temperature 50 [C]")
ax2.legend()
plt.grid()
plt.show()

# Plotting fluid volume vs room_temp
fig3, ax3 = plt.subplots()
ax3.plot(room2.room_temp - 273, water.required_volume(room2) * 1e3, 'r-', label=water.name + " initial_temp = 15 [C]")
ax3.plot(room2.room_temp - 273, novec_1230.required_volume(room2) * 1e3, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax3.plot(room2.room_temp - 273, fe_25.required_volume(room2) * 1e3, 'b-', label=fe_25.name + " initial_temp = -48 [C]")
ax3.plot(room2.room_temp - 273, fm_200.required_volume(room2) * 1e3, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax3.set(xlabel="Target Temperature [C]", ylabel="Suppressant Volume [litre]",
        title="Room area 10 [m^2], Target temperature 50 [C]")
ax3.legend()
plt.grid()
plt.show()

# Plotting fluid mass vs room_temp
fig4, ax4 = plt.subplots()
ax4.plot(room2.room_temp - 273, water.required_volume(room2) * water.density_liquid, 'r-',
         label=water.name + " initial_temp = 15 [C]")
ax4.plot(room2.room_temp - 273, novec_1230.required_volume(room2) * novec_1230.density_liquid, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax4.plot(room2.room_temp - 273, fe_25.required_volume(room2) * fe_25.density_liquid, 'b-',
         label=fe_25.name + " initial_temp = -48 [C]")
ax4.plot(room2.room_temp - 273, fm_200.required_volume(room2) * fm_200.density_liquid, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax4.set(xlabel="Target Temperature [C]", ylabel="Suppressant mass [kg]",
        title="Room area 10 [m^2], Target temperature 50 [C]")
ax4.legend()
plt.grid()
plt.show()

# Plotting fluid volume vs target_temp
fig5, ax5 = plt.subplots()
ax5.plot(room3.target_temp - 273, water.required_volume(room3) * 1e3, 'r-', label=water.name + " initial_temp = 15 [C]")
ax5.plot(room3.target_temp - 273, novec_1230.required_volume(room3) * 1e3, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax5.plot(room3.target_temp - 273, fe_25.required_volume(room3) * 1e3, 'b-',
         label=fe_25.name + " initial_temp = -48 [C]")
ax5.plot(room3.target_temp - 273, fm_200.required_volume(room3) * 1e3, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax5.set(xlabel="Room Temperature [C]", ylabel="Suppressant Volume [litre]",
        title="Room area 10 [m^2], Room temperature 150 [C]")
ax5.legend()
plt.grid()
plt.show()

# Plotting fluid mass vs room_temp
fig6, ax6 = plt.subplots()
ax6.plot(room3.target_temp - 273, water.required_volume(room3) * water.density_liquid, 'r-',
         label=water.name + " initial_temp = 15 [C]")
ax6.plot(room3.target_temp - 273, novec_1230.required_volume(room3) * novec_1230.density_liquid, 'g-',
         label=novec_1230.name + " initial_temp = 15 [C]")
ax6.plot(room3.target_temp - 273, fe_25.required_volume(room3) * fe_25.density_liquid, 'b-',
         label=fe_25.name + " initial_temp = -48 [C]")
ax6.plot(room3.target_temp - 273, fm_200.required_volume(room3) * fm_200.density_liquid, 'k-',
         label=fm_200.name + " initial_temp = -16 [C]")
ax6.set(xlabel="Room Temperature [C]", ylabel="Suppressant mass [kg]",
        title="Room area 10 [m^2], Room temperature 70 [C]")
ax6.legend()
plt.grid()
plt.show()
