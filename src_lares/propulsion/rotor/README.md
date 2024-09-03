# Rotor Sizing

This is an explanation file for the code that sizes the propellers (*LARES_CRotorPropellersSizing.py*) of the LARES DSE
Drone project. The code is general enough to be used for any other drone sizing, however LARES'design is what it was
mostly based on in its writing.

##### Requirements for the code to run

- An installation of CRotor, the extension of XRotor for coaxial propellers. It is already available in the git branch,
  so it only needs to be downloaded together with the script (documentation in the form of .txt is also included in the
  doc folder of CRotor!). In case it doesn't work, or to see where it comes from, it is also available
  at: http://www.esotec.org/sw/crotor.html. The code is written specifically for the Windows version of CRotor so it
  won't run on XRotor. The installation **must** be in the **same working directory**. If this is not done, this part of
  the code won't run and then CRotor won't be opened at all:

```python
 ps = subprocess.Popen(''.join([str(fileloc),'\\Crotor\\CRotor755es13_win32\\bin\\xrotor.exe']), shell=True,stdin=subprocess.PIPE, text=True)
```

When it's opened successfully you will see the CRotor start page in the terminal where the code runs.

Just ignore the Fortran runtime error when running the program because it's a given of the *ps.subprocess.communicate*
function, but it still works fine - it's just warning that the file is closed at the end (hence why the communicate
function is so long - file has to stay open).

#### The code itself

###### Class Propellers:

Firstly, the class *Propellers* contains functions that run CRotor based on the given inputs. The idea is to make it as
general as possible, which means that it needs to be valid also for a non coaxial set (as will be the case for Hive).
Luckily CRotor can also run as XRotor (while the opposite is more annoying to do) so I simply defined two functions
within the class:

- *do_coaxialrotor(self):* function shall be called in the case of co-rotating coaxial propellers, as was LARES. The
  function toggles the corotating option of CRotor, and inputs the coaxial, front and aft values of self. With regards
  to the inputs, the self function shows the kind of inputs the program is designed for. When inputting the list values,
  each should match the setting one wants to run: so say the aim is to run a propeller with r_front = 0.12, r_aft =
  0.14, RPM = 2000 and another with r_front = 0.15, r_aft = 0.18 and RPM = 5000, the inputs look like:

  ```
  r_front = [0.12,0.15] #[m]
  r_aft   = [0.14,0.18] #[m]
  RPM_coaxial = [2000,5000]
  ```

  so each i^th element of each list is run together in the code. An example of inputs is at the bottom of the code,
  under *name == main.*

- *do_singlerotor(self)*: this function is for the case of a single propeller per arm. It also allows to compare the
  thrust generated between coaxial and single, by for example plotting them in a graph.

A bit about the functions, since knowing what they do can help understand CRotor as well as follow the process I have
used: in both cases, the first thing that needs to be done in CRotor is define the geometry of the blade (else it will
simply take a nominal case, but I am unsure what that is). This is done through the AERO command, and the sequence of
seemingly random numbers are simply the data of the two airfoils (if you run CRotor from terminal you will see what they
stand for, it's really clear, but it's long to type). The data that are loaded for now are those of the WORTMANN FX and
the GOE225 airfoils. These were chosen during DSE, and I have kept the choice as is (more rationale on how the choice
was made is in the DSE final report).

So, if the aim is to run CRotor and get the results saved, it is necessary to input parameters in the class propellers,
and run either the single or coaxial function. The files will then be automatically saved into the current working
directory.

In the case that one or more iterations do not converge, it is not an issue, because each new iteration restarts with
CRotor from scratch. The file with the corresponding iteration will just not exist, as there is nothing to save for a
non converged iteration. This is taken care in the next class.

###### Class Data_analysis

Here the .txt files output by CRotor are read and their data is stored in an array. The functions in this class are able
to recognise whether the file that is being read is a Single or Coaxial rotor, and store the data as consequence.

- Firstly, the function *generate_files_names(self)* simply generates three lists, for front, aft (of coaxial) and
  single rotor files. It scans through the files present in the current working directory and, if the file exists, adds
  it to the list for it to be read later. If the file does not exist, the iteration must not have converged, and thus
  the search for that file stops. This function should be run **before** the *read_data* function. It basically
  generates the inputs for the second function, and prevents it reading a file that does not exist.
- *read_data(self,filetab)*: this function takes the input of the class + an additional input: filetab. This input is
  the result of the *generate_files_names(self)* function, which is why it is important to first run this function. As
  the output of *generate_files_names(self)* consists of 3 tabs in total (one for front coaxial, rear coaxial, and
  single rotor file names) it is important to give the input to *read_data()* in the form of filetab[0] or filetab[1]
  etc depending on which file is to read. The list of files to be read is passed to the read_data() function, so that
  the relevant data can be saved and graphed if necessary (for now RPM, Thrust, Power and Radius, but all are read so
  adding a return parameter can give more values, as long as they are in the .txt).

Now the code has been tested for a bunch of situations, but of course there are always things that I may have missed and
that are only found when working on another machine, so feel free to let me know if there's something that should be
changed!

As per what values should be inputs, well, that's being researched ;)

The two .txt files are example files. Delete them if running the code completely, or just use a read function if the aim
is to read them. 

