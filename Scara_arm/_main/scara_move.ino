//Variables that hold the number of stepper steps

//Variables to hold the returned data from the Delta Transform routine

long step[2] = {0, 0}; //[0]: X motor - forearm ; [1]:Y motor -arm;[3] Z motor
float arm_degree = 0;
float forearm_degree = 0;

long pow_radius = pow((PRIM_ARM_LENGTH + SEC_ARM_LENGTH), 2);

// checking if  destination  coordinate in cartesian inside circle boudary of 2 arm
bool isCoordinateValid(float Cartersian_coordinate[])
{
  long result = pow(Cartersian_coordinate[0] + HOME_POS_OFFSET_X, 2) + pow(Cartersian_coordinate[1] + HOME_POS_OFFSET_Y, 2);

  if (result <= pow_radius)
  {
    return true;
  }

  return false;
}
void rotation_matrix()
{
  float tmp_x = destination_cart[0];
  float tmp_y = destination_cart[1];

  Serial.print("x: ");
  Serial.println(destination_cart[0]);
  Serial.print("y : ");
  Serial.println(destination_cart[1]);

  float rad_rotation_angle = rotation_angle * 0.0174533;
  tmp_x = destination_cart[0]*cos(rad_rotation_angle) - destination_cart[1]*sin(rad_rotation_angle);
  tmp_y = destination_cart[0]*sin(rad_rotation_angle) + destination_cart[1]*cos(rad_rotation_angle);

  Serial.print("tmp_x: ");
  Serial.println(tmp_x);
  Serial.print("tmp_y : ");
  Serial.println(tmp_y);

  destination_cart[0] = tmp_x;
  destination_cart[1] = tmp_y;
}

void scara_move()
{

  //Offset the cartesian coordinates as the zero of the arm is actually under the first pivot

  //Offset the cartesian coordinates as the zero of the arm is actually under the first pivot
  start_cart[0] = (start_cart[0] + HOME_POS_OFFSET_X);
  start_cart[1] = (start_cart[1] + HOME_POS_OFFSET_Y);

  destination_cart[0] = (destination_cart[0] + HOME_POS_OFFSET_X);
  destination_cart[1] = (destination_cart[1] + HOME_POS_OFFSET_Y);

  //Rotate the destination_cart - calibration 
  rotation_matrix();

  Cartesian_to_Scara(start_cart[0], start_cart[1]);

  start_degree[0] = forearm_degree;
  start_degree[1] = arm_degree;

  Cartesian_to_Scara(destination_cart[0], destination_cart[1]);

  destination_degree[0] = forearm_degree;
  destination_degree[1] = arm_degree;

  if(isDegreeValid()){
    degree_to_steps();

    run_motor();

  // Reset the current position values (these are the global position variables)
    start_cart[0] = destination_cart[0] - HOME_POS_OFFSET_X;
    start_cart[1] = destination_cart[1] - HOME_POS_OFFSET_X;
  }

  Report_Info();
}

bool isDegreeValid()
{
  if (arm_degree <= Y_MAX && forearm_degree >= X_MIN)
  {
    return true;
  }

  return false;
}

void set_motor_direction()
{
  /*
    forearm and arm have opposite direction of movement.
    When increasing angle, arm move CW , forearm move CCW, and vice versa for the case
    of decreasing angle
  */

  // FOREARMDIRECTION
  if (start_degree[0] < destination_degree[0])
  {
    // WRITE(X_DIR_PIN, LOW);
    step[0] = -step[0];
  }
  else
  {
    // WRITE(X_DIR_PIN, HIGH);
  }
  // ARM DIRECTION
  if (start_degree[1] < destination_degree[1])
  {
    // WRITE(Y_DIR_PIN, HIGH);
  }
  else
  {
    step[1] = -step[1];
    // WRITE(Y_DIR_PIN, LOW);
  }
}

void run_motor()
{
  Serial.print("step_x: ");
  Serial.println(step[0]);
  Serial.print("step_y : ");
  Serial.println(step[1]);

  stepperX.setCurrentPosition(0);
  stepperY.setCurrentPosition(0);

  steppers.moveTo(step);
  while (byPassSmallAngle() && steppers.run())
  {
  }

  while ((endstopX == false && endstopY == false) && steppers.run())
  {
  }

  Report_Info();
}

bool byPassSmallAngle()
{
  return (stepperX.currentPosition() <= 600);
}

//Convert current arm degree to cartersian coordinate
void Scara_to_Cartersian(float m_arm_degree, float m_forearm_degree)
{
  start_degree[0] = arm_degree;
  start_degree[1] = forearm_degree;

  arm_degree = m_arm_degree * 0.0174533;
  forearm_degree = m_forearm_degree * 0.0174533;

  start_cart[0] = PRIM_ARM_LENGTH * cos(arm_degree) + SEC_ARM_LENGTH * cos(arm_degree + forearm_degree);
  start_cart[1] = PRIM_ARM_LENGTH * sin(arm_degree) + SEC_ARM_LENGTH * sin(arm_degree + forearm_degree);

  // Cartesian_to_Scara(start_cart[0],start_cart[1]);

  Serial.print("x ");
  Serial.println(start_cart[0]);
  Serial.print("y ");
  Serial.println(start_cart[1]);
}

void Cartesian_to_Scara(float x_cartesian, float y_cartesian) //Converts XYZ cartesian coordinates into Scara stepper motor steps
{
  float tophalf;    //to calculate the top half of the cosine rule equation
  float bottomhalf; //to calculate the bottom half of the cosine rule equation

  DistB = sqrt(pow(x_cartesian, 2) + pow(y_cartesian, 2));
  Theta = (atan2(y_cartesian, x_cartesian)) * 180 / Pi;
  Phi = (acos((pow(DistB, 2) + pow(PRIM_ARM_LENGTH, 2) - pow(SEC_ARM_LENGTH, 2)) / (2 * DistB * PRIM_ARM_LENGTH))) * 180 / Pi;
  //Calculate the cosine rule equation for the secondary arm angle
  tophalf = -pow(SEC_ARM_LENGTH, 2) - pow(PRIM_ARM_LENGTH, 2) + pow(DistB, 2);
  bottomhalf = 2 * SEC_ARM_LENGTH * PRIM_ARM_LENGTH;

  forearm_degree = (((acos(tophalf / bottomhalf)) * 180 / Pi)); //forearm

  if (-180 <= Theta && Theta <= -90)
  {
    Theta = Theta + 360;
  }

  arm_degree = ((Theta - Phi)); // arm

  Serial.print("arm_degree ");
  Serial.println(arm_degree);
  Serial.print("forearm ");
  Serial.println(forearm_degree);
}

void degree_to_steps()
{
  //offset for parallel arm
  //	start_degree[0] = start_degree[0] + (destination_degree[1] - start_degree[1]);

  float x_lag_degree = destination_degree[0] - start_degree[0];
  float y_lag_degree = destination_degree[1] - start_degree[1];

  Serial.print("ARM_LAG: ");
  Serial.println(y_lag_degree);
  Serial.print("FOREARM_LAG: ");
  Serial.println(x_lag_degree);

  //forearm
  step[0] = x_lag_degree * x_steps_per_degree;
  //primary arm
  step[1] = y_lag_degree * y_steps_per_degree;

  // Serial.println((destination_degree[0] - start_degree[0]));
  // Serial.println((destination_degree[1] - start_degree[1]));

  // Serial.print("X -forearm  steps: ");Serial.println(step[0]);
  // Serial.print("Y - arm steps: ");Serial.println(step[1]);
}

void Report_Info() //Feeds back to the host PC information about the move
{
  Serial.println("Done");
}

void Magnet_Grab()
{
  WRITE(MAGNET_PIN, HIGH);
}
void Magnet_Release()
{
  WRITE(MAGNET_PIN, LOW);
}
void GoUp()
{
  WRITE(SERVO_PIN, HIGH);
  piece_graber.write(160); // 0 degree
  WRITE(SERVO_PIN, LOW);
}
void GoDown()
{
  WRITE(SERVO_PIN, HIGH);
  piece_graber.write(8); // 0 degree
  WRITE(SERVO_PIN, LOW);
}

void polar_move()
{

  step[0] = destination_polar[0] * x_steps_per_degree;
  step[1] = destination_polar[1] * y_steps_per_degree;

  ArmRotation(step[1]);
  ForeArmRotation(step[0]);
}

void ArmHoming()
{
  WRITE(Y_DIR_PIN, LOW); //Direction of travel is towards minus end
  float homing_step = -1;
  stepperY.setCurrentPosition(0);
  while (!endstopY)
  {
    WRITE(Y_STEP_PIN, HIGH);
    delayMicroseconds(500);
    WRITE(Y_STEP_PIN, LOW);
    delayMicroseconds(500);
    // ANCHOR  CALIBRATE
    // ─── USE FOR CALIBRATE HOME ANGLE ───────────────────────────────────────────────
    //
    /*  stepperY.moveTo(homing_step);
    homing_step--;
    stepperY.run();
    delayMicroseconds(500); */
    // ────────────────────────────────────────────────────────────────────────────────
  }
  Serial.print("Arm homing step");
  Serial.println(stepperY.currentPosition());
  delayMicroseconds(1000);

  // ArmHoming_back();
}

void ForearmHoming()
{
  WRITE(X_DIR_PIN, HIGH); //Direction of travel is towards minus end
  // endstopX = false;
  float homing_step = 1;
  stepperX.setCurrentPosition(0);
  while (!endstopX)
  {
    WRITE(X_STEP_PIN, HIGH);
    delayMicroseconds(600);
    WRITE(X_STEP_PIN, LOW);
    delayMicroseconds(600);
    // ANCHOR CALIBRATE
    // ─── USE FOR CALIBRATE HOME ANGLE ───────────────────────────────────────────────
    //
    /*     stepperX.moveTo(homing_step);
    homing_step++;
    stepperX.run();
    delayMicroseconds(1000);
 */
    // ────────────────────────────────────────────────────────────────────────────────
  }
  Serial.print("ForeArm homing step");
  Serial.println(stepperX.currentPosition());
  delayMicroseconds(1000);
  // ForeArmHoming_back();
}

void ArmRotation(int step)
{
  endstopY = false;
  stepperY.setCurrentPosition(0);
  stepperY.moveTo(step);
  while (endstopY == false && stepperY.run())
    ;
}

void ForeArmRotation(int step)
{
  endstopX = false;
  stepperX.setCurrentPosition(0);
  stepperX.moveTo(step);
  while (endstopX == false && stepperX.run())
    ;
}

void ArmHoming_back()
{
  WRITE(Y_DIR_PIN, HIGH);
  int step = 104;
  while (step > 0)
  {
    step = step - 1;
    WRITE(Y_STEP_PIN, HIGH);
    delayMicroseconds(2000);
    WRITE(Y_STEP_PIN, LOW);
    delayMicroseconds(2000);
  }

  WRITE(Y_DIR_PIN, LOW);
  while (!endstopY)
  {
    WRITE(Y_STEP_PIN, HIGH);
    delayMicroseconds(2000);
    WRITE(Y_STEP_PIN, LOW);
    delayMicroseconds(2000);
  }
}

void ForeArmHoming_back()
{
  WRITE(X_DIR_PIN, LOW);
  int step = 104;
  while (step > 0)
  {
    step = step - 1;
    WRITE(X_STEP_PIN, HIGH);
    delayMicroseconds(2000);
    WRITE(X_STEP_PIN, LOW);
    delayMicroseconds(2000);
  }

  WRITE(X_DIR_PIN, HIGH);
  while (!endstopX)
  {
    WRITE(X_STEP_PIN, HIGH);
    delayMicroseconds(2000);
    WRITE(X_STEP_PIN, LOW);
    delayMicroseconds(2000);
  }
}
