# Drone-Design-Optimizer
This project focuses on the iterative design optimization of two drones, developed in cooperation with TurboAir and produced with the support of TU Delft DEMO. The drones were optimized based on specific initial requirements and were tested in real-world scenarios, including a collaboration with Dutch firefighters.

## Project Overview

The project aimed to design drones optimized for the highest thrust-to-weight (T/W) ratio, tailored to meet specific payload and configuration requirements. The process involved selecting the best combination of components—such as batteries, motors, ESCs, and propellers—from an existing database.

### Key Features

1. **Custom T/W Optimizer with SciPy:**
   - I developed a custom optimization routine using Python’s SciPy library. The optimizer was designed to maximize the thrust-to-weight ratio of the drone by systematically exploring available component combinations.

2. **Integration of Fortran-Based Programs:**
   - To enhance the optimization process, I incorporated Fortran-based programs, such as CRotor, directly within the optimizer. This allowed for precise calculations of rotor performance, leveraging the computational efficiency of Fortran while maintaining the flexibility of Python.

3. **High-Performance Computing (HPC) for Final Calculations:**
   - The final calculation of thrust parameters for the rotor was conducted on a High-Performance Computing (HPC) cluster at TU Delft. This setup enabled efficient handling of the complex calculations involved, running directly from the terminal on the TU Delft system.

### Input Parameters

The optimization process begins with the following initial inputs:

- **Desired Payload Weight:** The target weight the drone needs to carry.
- **Dimensional Constraints:** Any specific size or dimensional restrictions for the drone.
- **Configuration:** The type of drone configuration (e.g., quadcopter, octa-copter, coaxial).

### Process Workflow

1. **Initial Input:** Users provide the desired payload weight, any dimensional constraints, and the preferred drone configuration.
2. **Component Selection:** The code automatically selects the optimal battery, motor, ESC, and propeller combination from a pre-defined database to achieve the highest T/W ratio.
3. **Optimization:** The custom SciPy-based optimizer iteratively refines the component selection, incorporating Fortran-based performance calculations.
4. **Final Computation:** Thrust parameters are finalized using the HPC cluster, ensuring the drone design meets the required specifications.
5. **Production:** The optimized drone design is produced, in cooperation with TU Delft DEMO.

### Results

The first optimized drone was successfully produced and tested in collaboration with Dutch firefighters. Below is a render of the final drone design:

The TurboAir project page can be found at: [TurboAir Project Page](https://www.tudelft.nl/lr/tu-delft-advanced-air-mobility-ta2m/projects/drones-turbo-air)

A render of the first drone:
![image](https://github.com/user-attachments/assets/e5471e1e-8821-48c3-a4dd-11afd7699342)

A render of the second drone:
![image](https://github.com/user-attachments/assets/f3f3b70f-b6b8-44b2-95ce-1a394cccb3d0)

