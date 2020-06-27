# Key points 
- **Homing the arm first whenever you connect and control it - using G28 command**
- Currently - **AccelStepper library** is used for controlling the motor
- Both two motors move in **constant speed**
- **Gear ration is 3.1**(63(Printed**AccelStepper library** Gear)/20 (Pulley Gear))
- **Nema 200 stepper** motor and **1/32 micro step** mode with driver drv3385 is used.
- **Micro step mode** can be adjust by removing jumpers,which are placed below the stepper driver (The purple one on the board)
- **Ball bearing model** used in the robot (6002z ,608z)
- **Calibration excel, and mapping diagram for RAMPS 1.4 is provided in the Scara Folder**
- Recommend : **Using Visual Code** and **Arduino Extension of Visual Code** is easier in navigating code instead of **Arduino ide**
# File function
- Command is processed in main.ino
- Movement control and kinematic model is processed in scara_move.ino
- parameter is set in configuration file
  
# Setup
- Setting the followed parameter in Configuration.h (the defaut valued is already set in the file)
  - stepper motor unit : (steps per rev * stepping mode of motor)/360) * Gear ratio
  - homing angle 
  - rotation angle (For calibration)
  - Pin number
  - Arm length for each segment

# Command
1. Using **Pronterface sofware** or **Serial terminal in Arduino IDE** on computer to connect with the board by **USB port** 
2. Command for control
   1. G28 : Homing
   2. G0X_Y_ : moving the arm to the cartersain coordinate (X > 0 ; Y > 60 is recommended)
   3. G10 X_Y_ : rotate arm segment a certain degree in (X: outer arm segment , Y: inner arm segment). Positive direction is **counter-clockwise**
   4. G15,G16 : Homing only inner or outer arm segment
3. Other command is commented in **main.ino** file in **process_command()** function

# Calibration
- Read the **Calibration.pdf** in the Scara arm folder
- The **calibration excel file** in the Scara arm folder is already set up with formular for calibration each arm segment
- For the whole arm calibration 
  - Because data is measured mannually, you should lightly adjust the calibrate result (Ex 1.95 rotation degree +- 1 degree ) and test it be 
