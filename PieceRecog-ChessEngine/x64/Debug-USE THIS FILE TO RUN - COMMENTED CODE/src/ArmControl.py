# FOR ARM CONTROL
import serial
import serial.tools.list_ports
import time
import pandas as pd
import re
#####################################################
#               PREDEFINED VARIABLES                #
#####################################################
# ChessBoard_Data
csv_path = "src\\ChessBoard_Data.csv"
df = pd.read_csv(csv_path, index_col=0)

# Arduino Baudrate
baud = 115200

# Detect Arduino port automatically
port = ''
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    if 'Arduino' in p.description:
        port = p[0]


class ArmControl:
    """
    This class handles communication with the Arduino via serial connection.
    There are two main functions: RunSCARA and ReadButton

    <> Parameters
    --------------
    :param old_pos: The current position of the chess piece
    :param new_pos: The position that the piece will be placed
    :param check_capture: Flag to check whether the new_pos has an opponent piece or not

    <> Serial functions (send and receive message in byte form)
    -------------------
    ser.write(str.encode('ascii'))
    ser.readline().decode()
    """
    def __init__(self):

        #####################################################
        #                   SETUP ARDUINO                   #
        #####################################################
        # Open Serial Connection between Arduino and Python
        self.ser = serial.Serial(port, baud, timeout=1)

        # Check if the serial port is opened and available
        if self.ser.isOpen():
            print(self.ser.name + ' is open...')

        # Wait for arduino to setup
        while 1:
            print ("Readinggg")
            out = self.ser.readline()
            out_d = out.decode()
            print('Receiving...' + out_d)
            if (out_d == ''):
                break
        print("Set arm to home")
        self.ReturnHome()
        self.CheckDoneStatus()
        print("Return HOME")
        self.count = 0
        self.graveyard = df.loc['Row_1', 'Col_9'].split(',')
        self.graveyard[0] = str(int(self.graveyard[0]) - 55)
        initialgraveyard_row = self.graveyard[1]



    #####################################################
    #                   MAIN FUNCTIONS                  #
    #####################################################
    def ReadButton(self):
        """
        This function freeze the system and wait for the button to be pressed by the player
        "Done playing" string to the program

        :return: clientmessage (Doneplaying string)
        """
        print ("read button now: ")
        # The loop in CheckDoneplaying will freeze the program until the signal is match
        clientmessage = self.CheckDonePlaying()
        print ("In Arm_Control send: ", clientmessage)
        # Send Doneplaying msg to server to run camera and alpha beta
        print("Awaiting server response...")
        return clientmessage

    def RunSCARA(self, old_pos, new_pos, check_capture):
        """
        This function is a combination of functions:
            + MoveChess()
            + CheckDoneStatus()
            + ChessGrabDrop()
            + ReturnHome()
        Basing on the check_capture variable, the function is divided into 2 cases.

        <> G-code representation
        ------------------------
        G5: Move Servo up or down based on a Boolean in Arduino code
        G6: Set the solenoid in the tool ON or OFF
        G28: Move the SCARA arm to its home position. This step is required after every RunSCARA command
        G0 X<pos>Y<pos>: Move the SCARA arm to position (x,y).(Ex: G0 X50Y40)
        """
        print("Set arm to home")
        self.ReturnHome()
        self.CheckDoneStatus()
        print("Information passed: Old pos: {}, New pos: {}, check capture: {}".
               format(old_pos, new_pos, check_capture))
        self.old_pos = df.loc['Row_{}'.format(old_pos[0]),
                     'Col_{}'.format(old_pos[1])].split(',')
        self.pos = df.loc['Row_{}'.format(new_pos[0]),
                     'Col_{}'.format(new_pos[1])].split(',')
        #####################################################
        #                   CONTROL ARM                     #
        #####################################################
        # Check condition:
        if check_capture == False:
            print("Check = True")
            self.MoveChess(self.old_pos)
            self.CheckDoneStatus()
            print("Moved to previous position")
            self.ChessGrabDrop()
            print("Take piece")
            self.MoveChess(self.pos)
            self.CheckDoneStatus()
            print("Moved to new position")
            self.ChessGrabDrop()
            print("Release Piece")
            self.ReturnHome()
            self.CheckDoneStatus()
            print("Return HOME")
        if check_capture == True:
            print("Check = False")
            # Get to the position where the piece was captured
            # Setup place in graveyard
            self.count += 1
            self.graveyard[1] = str(int(self.graveyard[1]) + 42)

            # When the chess piece exceeds 10 piece in a column,
            # the initial row is reset to reset the process
            if self.count == 10:
                self.graveyard[0] = str(int(self.graveyard[0]) - 55)
                self.count = 0
                self.graveyard[1] = initialgraveyard_row

            self.MoveChess(self.pos)
            self.CheckDoneStatus()
            # Pick up the piece
            self.ChessGrabDrop()
            # Put it to graveyard area
            self.MoveChess(self.graveyard)
            self.count += 1
            # Put piece down
            self.ChessGrabDrop()
            # Move arm to the position to pick up
            self.MoveChess(self.old_pos)
            self.CheckDoneStatus()
            # Pickup the piece
            self.ChessGrabDrop()
            # Put the piece at its new position
            self.MoveChess(self.pos)
            self.CheckDoneStatus()
            # Put piece down
            self.ChessGrabDrop()
            print("Moved to new position")
            self.ReturnHome()
            self.CheckDoneStatus()
            print("Return HOME")

    def MoveChess(self, position):
        """
        This function moves SCARA arm based on input position
        
        :param position: The position you want the SCARA arm to move to ( tuple form)
        """
        print('G0 X{}Y{}\r\n'.format(position[0], position[1]))
        code = 'G0 X{}Y{}\r\n'.format(position[0], position[1])
        self.ser.write(code.encode('ascii'))

    def ChessGrabDrop(self):
        """
        This function is a combination of functions:
            + MoveServo()
            + CheckDoneStatus()
            + Magnet()
        It represent 2 cycles based on the solenoid Boolean inside Arduino code:
            + Moving the servo down -> turn on magnet to grab the chess piece -> moving the servo up
            + Moving the servo down -> turn off magnet to drop the chess piece -> moving the servo up
        """
        self.MoveServo()
        self.CheckDoneStatus()
        self.Magnet()
        self.CheckDoneStatus()
        self.MoveServo()
        self.CheckDoneStatus()
        time.sleep(0.5)

    def MoveServo(self):
        """
        This function move the servo based on the servo Boolean inside Arduino code
        """
        print("Move Servo")
        code = 'G5' + '\r\n'
        self.ser.write(code.encode('ascii'))

    def Magnet(self):
        """
        This function turn the solenoid on or off based on the solenoid Boolean inside Arduino code
        """
        print("Magnet")
        code = 'G6' + '\r\n'
        self.ser.write(code.encode('ascii'))

    def ReturnHome(self):
        """
        This function move the SCARA arm to its home location
        """
        print("Return Home")
        code = 'G28' + '\r\n'
        self.ser.write(code.encode('ascii'))
        self.CheckDoneStatus()

    def CheckDoneStatus(self):
        """
        This function puts the system in freeze and wait for the "Done" signal sent from the Arduino
        """
        print("CHECK DONE STATUS")
        breakstatus = False
        while breakstatus == False:
            out = self.ser.readline()
            out_d = out.decode()
            print('Receiving...' + out_d)
            if out_d == 'Done\r\n':
                time.sleep(0.5)
                # if out_d=='':
                print("TASK DONE")
                breakstatus = True
                break
    def CheckDonePlaying(self):
        """
        This function puts the system in freeze and wait for the "Done playing" signal sent from the Arduino
        """
        print("CHECK Done playing STATUS")
        breakstatus = False
        while breakstatus == False:
            out = self.ser.readline()
            out_d = out.decode()
            print('Receiving...'+out_d)
            if out_d == 'Done playing\r\n':
                print("Done playing")
                breakstatus = True
                return out_d
                break
