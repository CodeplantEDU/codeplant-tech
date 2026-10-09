// Arduino UNO R3 + SunFounder L298N + Adafruit TT motor #3777
// Remove 5V-EN and ENA jumpers before wiring. UNO: USB; motor: external 6V.
const byte ENA_PIN = 9;
const byte IN1_PIN = 8;
const byte IN2_PIN = 7;
const byte PWM_LOW = 180;   // Adjust upward if the unloaded motor cannot start.
const byte PWM_HIGH = 230;  // PWM command, not measured RPM.
const unsigned long RUN_MS = 2000;
const unsigned long STOP_MS = 1500; // Increase if the shaft is still moving.

void stopMotor() {
  analogWrite(ENA_PIN, 0);  // Disable the bridge: coast, not active braking.
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  Serial.println("STOP pwm=0");
  delay(STOP_MS);
}

void runMotor(bool directionA, byte pwm) {
  // Caller stops the motor before changing direction.
  digitalWrite(IN1_PIN, directionA ? HIGH : LOW);
  digitalWrite(IN2_PIN, directionA ? LOW : HIGH);
  analogWrite(ENA_PIN, pwm);
  Serial.print(directionA ? "A pwm=" : "B pwm=");
  Serial.println(pwm);
  delay(RUN_MS);
}

void setup() {
  digitalWrite(ENA_PIN, LOW);
  digitalWrite(IN1_PIN, LOW);
  digitalWrite(IN2_PIN, LOW);
  pinMode(ENA_PIN, OUTPUT);
  pinMode(IN1_PIN, OUTPUT);
  pinMode(IN2_PIN, OUTPUT);
  Serial.begin(9600);
  stopMotor();
}

void loop() {
  runMotor(true, PWM_LOW);
  runMotor(true, PWM_HIGH);
  stopMotor();
  runMotor(false, PWM_LOW);
  runMotor(false, PWM_HIGH);
  stopMotor();
}
