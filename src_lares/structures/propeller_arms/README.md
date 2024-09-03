# LARES_PropellerArms.py

This README is a work in progress but for now the only thing that is there to know is: the code is largely based on the
previous DSE sizing code, with some minor adjustments to make it better and more adaptable. It will be done very soon :)

**YES the image will be changed and visible** :)

**TODO: get torque from CRotor and figure out what the torque actually is**

This README aims to explain what the propeller arms script does.

The first step is to calculate the loads that the propeller arm experiences. Taking a look at the two FBDs below, these
can be easily determined (for terms vertical/horizontal the DSE report is extensive enough):

![image-20211001103156451](C:\Users\jlari\AppData\Roaming\Typora\typora-user-images\image-20211001103156451.png)

Firstly, as all the loads need to be calculated, the weight of the propeller is determined. This is done through the
function *calculate_weight_oneblade()* which takes the data from the files where the propeller is saved and calculates
the total weight of one blade. As the file output from CRotor/XRotor gives the properties of the blade per section, the
idea behind calculating the weight is as follows:

For each element, the radial section and the chord are given. This allows for calculating the area of the airfoil at a
specific point. Knowing which airfoil is used where means the t/c ratio is easily found at each section. Since a drawing
explains it better, in the image below is the method I have used for estimating the weight of one blade:

![Image-1](C:\Users\jlari\Downloads\Image-1.jpg)

Note: in the code, r_wortmann is *already* half the thickness!

This being an estimation means that it is not completely precise. Firstly, both Wortmann and GOE225 airfoils are much "
leaner" compared to a circle and a triangle joined together. However, although there are for sure software that
calculate the precise area, this approximation will lead to an overestimation of the weight rather than an
underestimation (simply because I am considering an airfoil with more area than the real, rather than less). For this
reason I believe this overestimation can be considered as a safety factor.

The function returns the weight of one blade (so total propeller is times number of blades) and as input asks the file
where the blade weight has to be calculated, as well as the total radius. These can both be found from the
LARES_CRotorPropellerSizing.py file, so the only requirement is knowing which file to calculate the weight for. If it's
multiple, the function can be run multiple times. For now I assumed we will run the weight of only a selected amount of
propellers, but if I see that there's too many I can modify the function to do them all at once.

The other two required loads, the thrust and the weight of the motor (I am assuming the battery is stored in the main
body) are imported from the respective files.

Motor dimensions should be in [m]
