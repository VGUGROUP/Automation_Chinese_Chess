
#include "Configuration.h"
#include "Arduino.h" //Needed for Ramps 1.4
#include "fastio.h"
#include "math.h"

#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>
extern "C" void __cxa_pure_virtual();
// Servo object

Servo piece_graber;
// Servo State and Magnet State
bool isDown = false;
bool Grab = false;

// PlayerDone button
bool isPlayerDone = false;

//Implemented Codes
//-------------------
// G0  -> G1
// G1  - Coordinated Movement X Y Z E
// G28 - Home all Axis

//Stepper Movement Variables

char axis_codes[NUM_AXIS] = {'X', 'Y', 'Z', 'E'};
char polar_codes[NUM_AXIS] = {'X', 'Y', 'Z', 'E'};

float destination_polar[NUM_AXIS] = {0, 0, 0, 0}; //Holds the X Y Z cartesian coordinates of the current position of the tool head
float start_cart[NUM_AXIS] = {0, 0, 0, 0};        //Holds the X Y Z cartesian coordinates of the current position of the tool head
float current_cart[NUM_AXIS] = {0, 0, 0, 0};      //Holds the predicted X Y Z cartesian coordinates of the tool head at any point in time
float destination_cart[NUM_AXIS] = {0, 0, 0, 0};  //Holds the X Y Z cartesian coordinates of the destination position of the tool head

float start_degree[NUM_AXIS] = {0, 0, 0, 0};       //Holds the start position for the SCARA MOVE in stepper steps (4th value not yet used)
float move_degree[NUM_AXIS] = {0, 0, 0, 0};        //Holds the predicted X Y Z SCARA coordinates of the tool head at any point in time
float destination_degree[NUM_AXIS] = {0, 0, 0, 0}; //Holds the finish position for the SCARA MOVE in stepper steps (4th value not yet used)

long gcode_N, gcode_LastN;
bool relative_mode = false; //Determines Absolute or Relative Coordinates
bool has_homed = true;      //Whether the robot has been homed. No moves allowed until it has
int endstopstate;           //used when checking endstops

// comm variables
#define MAX_CMD_SIZE 96
#define BUFSIZE 8
char cmdbuffer[BUFSIZE][MAX_CMD_SIZE];
//bool fromsd[BUFSIZE];
int bufindr = 0;
int bufindw = 0;
int buflen = 0;
int i = 0;
char serial_char;
int serial_count = 0;
boolean comment_mode = false;
char *strchr_pointer; // just a pointer to find chars in the cmd string like X, Y, Z, E, etc

volatile bool endstopX = false;
volatile bool endstopY = false;

AccelStepper stepperX(AccelStepper::DRIVER, X_STEP_PIN, X_DIR_PIN);
AccelStepper stepperY(AccelStepper::DRIVER, Y_STEP_PIN, Y_DIR_PIN);
MultiStepper steppers;

int angleRotatedX = 0;
int angleRotatedY = 0;

void setup()
{
  //TEST ENDSTOP ON X-AXIS FOREARM
  attachInterrupt(digitalPinToInterrupt(X_MIN_PIN), endstop_X, CHANGE);
  attachInterrupt(digitalPinToInterrupt(Y_MIN_PIN), endstop_Y, CHANGE);
  attachInterrupt(digitalPinToInterrupt(PlayerButton), playerButton, FALLING);

  //-------------------------------
  stepperX.setMaxSpeed(800);
  stepperY.setMaxSpeed(800);

  stepperX.setSpeed(450);
  stepperY.setSpeed(450);

  stepperX.setAcceleration(800);
  stepperY.setAcceleration(800);

  steppers.addStepper(stepperX);
  steppers.addStepper(stepperY);

  Serial.begin(BAUDRATE);
  Serial.println("start");

  if (is_X_endstopped() == false)
  {
    ForearmHoming();
  }

  if (is_Y_endstopped() == false)
  {
    ArmHoming();
  }
  ForeArmHoming_back();
  ArmHoming_back();
  Scara_to_Cartersian(Y_AXIS_HOME_ANGLE, X_AXIS_HOME_ANGLE);
  Cartesian_to_Scara(start_cart[0], start_cart[1]);

  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);
  Report_Info();
  
 

  // Set servo pin
  piece_graber.attach(SERVO_PIN);
  // Set magnet pin
  SET_OUTPUT(MAGNET_PIN);
  //Initialize Dir Pins
  SET_OUTPUT(X_DIR_PIN);
  SET_OUTPUT(Y_DIR_PIN);

  //Initialize Enable Pins - steppers default to disabled.
  SET_OUTPUT(X_ENABLE_PIN);
  WRITE(X_ENABLE_PIN, LOW);
  SET_OUTPUT(Y_ENABLE_PIN);
  WRITE(Y_ENABLE_PIN, LOW);


  //endstops and pullup resistors

  SET_INPUT(X_MIN_PIN);
  WRITE(X_MIN_PIN, HIGH);
  SET_INPUT(Y_MIN_PIN);
  WRITE(Y_MIN_PIN, HIGH);


  SET_INPUT(X_MIN_PIN);
  SET_INPUT(Y_MIN_PIN);

  //Initialize Step Pins
  SET_OUTPUT(X_STEP_PIN);
  SET_OUTPUT(Y_STEP_PIN);
  Report_Info();
}

void loop()
{
  if (buflen < 3)
    get_command();

  if (buflen)
  {

    process_commands();

    buflen = (buflen - 1);
    bufindr = (bufindr + 1) % BUFSIZE;
  }
}

inline void get_command()
{
  while (Serial.available() > 0 && buflen < BUFSIZE)
  {
    serial_char = Serial.read();
    if (serial_char == '\n' || serial_char == '\r' || serial_char == ':' || serial_char == ';' || serial_count >= (MAX_CMD_SIZE - 1))
    {
      if (!serial_count)
        return;                             //if empty line
      cmdbuffer[bufindw][serial_count] = 0; //terminate string
      if (!comment_mode)
      {
        //    fromsd[bufindw] = false;
        if (strstr(cmdbuffer[bufindw], "N") != NULL)
        {
          strchr_pointer = strchr(cmdbuffer[bufindw], 'N');
          gcode_N = (strtol(&cmdbuffer[bufindw][strchr_pointer - cmdbuffer[bufindw] + 1], NULL, 10));
          if (gcode_N != gcode_LastN + 1 && (strstr(cmdbuffer[bufindw], "M110") == NULL))
          {
            Serial.print("Serial Error: Line Number is not Last Line Number+1, Last Line:");
            Serial.println(gcode_LastN);
            //Serial.println(gcode_N);
            FlushSerialRequestResend();
            serial_count = 0;
            return;
          }

          if (strstr(cmdbuffer[bufindw], "*") != NULL)
          {
            byte checksum = 0;
            byte count = 0;
            while (cmdbuffer[bufindw][count] != '*')
              checksum = checksum ^ cmdbuffer[bufindw][count++];
            strchr_pointer = strchr(cmdbuffer[bufindw], '*');

            if ((int)(strtod(&cmdbuffer[bufindw][strchr_pointer - cmdbuffer[bufindw] + 1], NULL)) != checksum)
            {
              Serial.print("Error: checksum mismatch, Last Line:");
              Serial.println(gcode_LastN);
              FlushSerialRequestResend();
              serial_count = 0;
              return;
            }
            //if no errors, continue parsing
          }
          else
          {
            Serial.print("Error: No Checksum with line number, Last Line:");
            Serial.println(gcode_LastN);
            FlushSerialRequestResend();
            serial_count = 0;
            return;
          }

          gcode_LastN = gcode_N;
          //if no errors, continue parsing
        }
        else // if we don't receive 'N' but still see '*'
        {
          if ((strstr(cmdbuffer[bufindw], "*") != NULL))
          {
            Serial.print("Error: No Line Number with checksum, Last Line:");
            Serial.println(gcode_LastN);
            serial_count = 0;
            return;
          }
        }
        if ((strstr(cmdbuffer[bufindw], "G") != NULL))
        {
          strchr_pointer = strchr(cmdbuffer[bufindw], 'G');
          switch ((int)((strtod(&cmdbuffer[bufindw][strchr_pointer - cmdbuffer[bufindw] + 1], NULL))))
          {
          case 0:
          case 1:

            // Serial.println("ok");
            break;
          default:
            break;
          }
        }
        bufindw = (bufindw + 1) % BUFSIZE;
        buflen += 1;
      }
      comment_mode = false; //for new command
      serial_count = 0;     //clear buffer
    }
    else
    {
      if (serial_char == ';')
        comment_mode = true;
      if (!comment_mode)
        cmdbuffer[bufindw][serial_count++] = serial_char;
    }
  }
}

inline float code_value()
{
  return (strtod(&cmdbuffer[bufindr][strchr_pointer - cmdbuffer[bufindr] + 1], NULL));
}
inline long code_value_long()
{
  return (strtol(&cmdbuffer[bufindr][strchr_pointer - cmdbuffer[bufindr] + 1], NULL, 10));
}
inline bool code_seen(char code_string[])
{
  return (strstr(cmdbuffer[bufindr], code_string) != NULL); //Return True if the string was found
}

inline bool code_seen(char code)
{
  strchr_pointer = strchr(cmdbuffer[bufindr], code);
  return (strchr_pointer != NULL); //Return True if a character was found
}

inline void process_commands()
{
  unsigned long codenum; //throw away variable
  char *starpos = NULL;

  if (code_seen('G'))
  {
    switch ((int)code_value())
    {
    //---------------------------------------------------------------------------------------------------------------------------------------------
    case 0: // G0 -> G1
    //---------------------------------------------------------------------------------------------------------------------------------------------
    case 1: // G1 Linear move
      endstopX = false;
      endstopY = false;
      // has_homed = false;
      get_coordinates(); // For X Y Z E F
      scara_move();

      return;
      break;
    //---------------------------------------------------------------------------------------------------------------------------------------------
    case 5: //Servo Manipulation
      Serial.println("Servo Manipulation");
      Serial.println(isDown);
      // State 1: Servo is Up
      if (isDown == false)
      {
        GoDown();
        isDown = true;
      }
      else
      {
        GoUp();
        isDown = false;
      } 
      Report_Info();
      break;

    //---------------------------------------------------------------------------------------------------------------------------------------------
    case 6: //Magnet Manipulation

      Serial.println("Magnet Manipulation");
      Serial.println(Grab);
      // Put a 500ms delay for magnet to operate
      delay(500);
      if (Grab == false)
      {
        Magnet_Grab();
        Grab = true;
      }
      else
      {
        Magnet_Release();
        Grab = false;
      }
      Report_Info();
      break;

    // ─────────────────────────────────────────────────────────────────
    case 7: // Set player button
      set_isPlayerDone();
      break;
    //---------------------------------------------------------------------------------------------------------------------------------------------
    case 10: // rotate arm segment G10X10Y20 (rotate inner arm 10 deg counter-clockwise,outer arm 20 counter-clockwise)
      get_coordinates_polar();
      polar_move();
      angleRotatedX += destination_polar[0];
      angleRotatedY += destination_polar[1];
      Serial.println("---------------------------------------------------------------------------------------");
      Serial.print("X_angle_rotated");
      Serial.println(angleRotatedX);
      Serial.print("Y_angle_rotated");
      Serial.println(angleRotatedY);
      Serial.println("---------------------------------------------------------------------------------------");
      break;
    case 13: //reset rotation degree value 
      angleRotatedX = 0;
      angleRotatedY = 0;
      Serial.println("---------------------------------------------------------------------------------------");
      Serial.print("X_angle_rotated");
      Serial.println(angleRotatedX);
      Serial.print("Y_angle_rotated");
      Serial.println(angleRotatedY);
      Serial.println("---------------------------------------------------------------------------------------");
      break;
    case 14: //print current endstop state
      Serial.print("endstopX");
      Serial.println(digitalRead(X_MIN_PIN));
      Serial.println(endstopX);
      Serial.print("endstopY");
      Serial.println(digitalRead(Y_MIN_PIN));
      Serial.println(endstopY);
      break;
    case 15: // Homing only outer arm segment
      //calibration
      ArmHoming();
      break;
    case 16:  // Homing only inner arm segment
      //calibration
      ForearmHoming();
      break;
    case 28: //G28 Home all Axis one at a time
      if (is_X_endstopped() == false)
      {
        ForearmHoming();
      }

      if (is_Y_endstopped() == false)
      {
        ArmHoming();
      }
      ForeArmHoming_back();
      ArmHoming_back();
      Scara_to_Cartersian(Y_AXIS_HOME_ANGLE, X_AXIS_HOME_ANGLE);
      Cartesian_to_Scara(start_cart[0], start_cart[1]);

      stepperX.setCurrentPosition(0);
      stepperY.setCurrentPosition(0);
      Report_Info();

      break;
    }
  }

  //---------------------------------------------------------------------------------------------------------------------------------------------

  else
  {
    Serial.println("Unknown command:");
    Serial.println(cmdbuffer[bufindr]);
  }

  ClearToSend();
}

void FlushSerialRequestResend()
{
  //char cmdbuffer[bufindr][100]="Resend:";
  Serial.flush();
  Serial.print("Resend:");
  Serial.println(gcode_LastN + 1);
  ClearToSend();
}

void ClearToSend()
{
  Serial.println("Done");
}

inline void get_coordinates()
{
  for (int i = 0; i < NUM_AXIS; i++)
  {
    if (code_seen(axis_codes[i]))
    {
      destination_cart[i] = (float)code_value();
      Serial.println((float)code_value());
    }
    else
    {
      destination_cart[i] = start_cart[i];
    }
  }
}

void endstop_X()
{
  //  X_MIN_PIN = 0 --> endstop_X is pushed
  endstopX = digitalRead(X_MIN_PIN) == 0 ? 1 : 0;
  // Serial.println("______________________");
  // Serial.println("X");
  // Serial.println("______________________");
}

void endstop_Y()
{
  //  Y_MIN_PIN = 0 --> endstop_Y is pushed
  endstopY = digitalRead(Y_MIN_PIN) == 0 ? 1 : 0;
  // Serial.println("______________________");
  // Serial.println("Y");
  // Serial.println("______________________");
}

void playerButton()
{
  // if(isPlayerDone == true)
  // {
  Serial.println("Done playing");
  // isPlayerDone = false;
  // }
}

void set_isPlayerDone()
{
  isPlayerDone = true;
}

bool get_isPlayerDone()
{
  return isPlayerDone;
}

bool is_Y_endstopped()
{
  return digitalRead(Y_MIN_PIN) == 0 ? 1 : 0;
}

bool is_X_endstopped()
{
  return digitalRead(X_MIN_PIN) == 0 ? 1 : 0;
}

inline void get_coordinates_polar()
{
  for (int i = 0; i < NUM_AXIS; i++)
  {
    if (code_seen(polar_codes[i]))
    {
      destination_polar[i] = (float)code_value();
    }
    else
    {
      destination_polar[i] = 0;
    }
  }
}