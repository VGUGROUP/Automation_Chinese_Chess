# FOR ARM CONTROL
import sys
import serial
import serial.tools.list_ports
import time
import pandas as pd
import re
#####################################################
#               PREDEFINED VARIABLES                #
#####################################################
# Read csv file
csv_path = "src\\ChessBoard_Data.csv"
df = pd.read_csv(csv_path, index_col=0)
# Arduino COM number
port = ''
ports = list(serial.tools.list_ports.comports())
for p in ports:
    print(p)
    if 'Arduino' in p.description:
        port = p[0]
# Arduino port number
baud = 115200
# dead piece position and Boundary for graveyard:
dead_pos =['50','50']
graveyard_min_x = 50
graveyard_min_y = 50
graveyard = [['-89', '10'], ['-131','10'],['-173','10'],
             ['-89','-32'],['-131','-32'],['-173','-32'],
             ['-89','-74'],['-131','-74'],['-173','-74'],
             ['-89','-116'],['-131','-116'],['-173','-116'],
             ['-89','-158'],['-131','-158'],['-173','-158']]

# Camera Origin pos
cam_origin = ['0','275']
class ArmControl:
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
            # # Test received variables############################
            # print ("check: ", self.check)
            # print('Pre pos ini: {},{}'.format(self.prepos_ini[0], self.prepos_ini[1]))
            # print('Pre pos end: {},{}'.format(self.prepos_end[0], self.prepos_end[1]))
            # print('Pos: {},{}'.format(self.pos[0], self.pos[1]))
            # print("Endgame condition: ",self.endgame)
            # #####################################################


    #####################################################
    #                   MISC FUNCTIONS                  #
    #####################################################
    def ReadButton(self):
        print ("read button now: ")
        #####################################################
        #           READ Done playing FROM BUTTON           #
        #####################################################
        # The loop in CheckDoneplaying will freeze the program until the sig is match
        clientmessage = self.CheckDonePlaying()
        print ("In Arm_Control send: ", clientmessage)
        # Send Doneplaying msg to server to run camera and alpha beta
        print("Awaiting server response...")
        return clientmessage

    def RunSCARA(self, old_pos, new_pos, check_capture):
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
        print('G0 X{}Y{}\r\n'.format(position[0], position[1]))
        code = 'G0 X{}Y{}\r\n'.format(position[0], position[1])
        self.ser.write(code.encode('ascii'))

    def ChessGrabDrop(self):
        self.MoveServo()
        self.CheckDoneStatus()
        self.Magnet()
        self.CheckDoneStatus()
        self.MoveServo()
        self.CheckDoneStatus()
        time.sleep(0.5)

    def MoveServo(self):
        print("Move Servo")
        code = 'G5' + '\r\n'
        self.ser.write(code.encode('ascii'))

    def Magnet(self):
        print("Magnet")
        code = 'G6' + '\r\n'
        self.ser.write(code.encode('ascii'))

    def ReturnHome(self):
        print("Return Home")
        code = 'G28' + '\r\n'
        self.ser.write(code.encode('ascii'))
        self.CheckDoneStatus()
        # code = 'G10 X-50' + '\r\n'
        # self.ser.write(code.encode('ascii'))
        # self.CheckDoneStatus()

    def CheckDoneStatus(self):
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
        print("CHECK Done playing STATUS")
        breakstatus = False
        while breakstatus == False:
            out = self.ser.readline()
            out_d = out.decode()
            print('Receiving...'+out_d)
            # out_d = input()
            if out_d == 'Done playing\r\n':
                print("Done playing")
                breakstatus = True
                return out_d
                break
# if __name__ == "__main__":
#     ArmControl()
