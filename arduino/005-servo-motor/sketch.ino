#include <Servo.h>

Servo servoMotor;
const int SERVO_PIN = 9;
// Start with the standard pulse range; calibrate against the actual servo.
const int MIN_PULSE_US = 1000;
const int MAX_PULSE_US = 2000;
const unsigned long HOLD_MS = 1000;

void moveToAngle(int commandAngle) {
  servoMotor.write(commandAngle);
  Serial.print("command=");
  Serial.println(commandAngle);
  delay(HOLD_MS);
}

void setup() {
  Serial.begin(9600);
  servoMotor.attach(SERVO_PIN, MIN_PULSE_US, MAX_PULSE_US);
  moveToAngle(90);
}

void loop() {
  moveToAngle(60);
  moveToAngle(90);
  moveToAngle(120);
}
