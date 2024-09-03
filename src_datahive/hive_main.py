#!/usr/bin/env python
"""
Final main runcode for the propeller noise modifications
"""
import shutil
import errno

from chord_modi import *
from run_xrotor import *

plt.rcParams.update({
    "text.usetex": True,
    "font.family": "sans-serif",
    "font.sans-serif": ["Helvetica"]})

# Required inputs
init = input('Inputs: og prop file <space> og diameter[in] <space> radial point [in] to '
             'begin chord change <space> chord increase @ r/R = 1 <space> RPMseq <space>')

fileslist = init.split()
prop_file = ''.join(['og_prop/', str(fileslist[0])])
R = float(fileslist[1]) / 2
r_start = float(fileslist[2])
c_incr = float(fileslist[3])
rpm = fileslist[4]
aero_data = None

# STEP 1: modify the chord
mod = ModifyGeometry(R, prop_file)
new_prop = mod.modified_geometry(r_start, c_incr)  # returns ... (for the future to remember how to run something)
make_plot = mod.plot_geometry(r_start, c_incr)

savefile_1 = ''.join(
    ['og', str(fileslist[0][:-4]), 'RPM', str(rpm),'c_incr',str(c_incr),'at',str(r_start),'.txt'])  # .txt extension is added in the file already
savefile_2 = ''.join(['changed', str(fileslist[0][:-4]), 'RPM', str(rpm), 'c_incr',str(c_incr),'at',str(r_start), '.txt'])
print('Original & Modified files saved')

# STEP 2: use the files you made to run them to XRotor
print('Running XRotor...')
xrot_og = RunXrotor(prop_file, rpm, R, savefile_1)
xrot_mod = RunXrotor(new_prop[3], rpm, R, savefile_2)

run_og = xrot_og.run_xrotor()
run_mod = xrot_mod.run_xrotor()
working_dir = os.getcwd()


print('XRotor ran successfully')

# For each run of the program, make a new directory that saves results (so move XRotor files to here)
dir_name = ''.join(['xrotor_results/RUNwith', str(fileslist[0][:-4]), '_Rad_', str(R)])
path = os.path.join(working_dir, dir_name)

try:
    os.mkdir(path)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise
    pass

# Now move the XRotor files to the created directory
final_path = '/'.join([path, savefile_1])

try:
    shutil.move(savefile_1, path)
    shutil.move(savefile_2, path)
except FileNotFoundError as error:
    pass

fig_name = ''.join(['Chord_Graph_Cchange_RPM', str(c_incr), str(rpm), '.png'])
plt.savefig(str(fig_name), dpi=200)
print('Figure Saved')

try:
    shutil.move(fig_name, path)
except (FileNotFoundError, FileExistsError) as error:
    pass
print('Files moved')

plt.show()
