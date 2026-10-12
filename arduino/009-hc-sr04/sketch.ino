const byte TRIG_PIN = 9;
const byte ECHO_PIN = 10;
const unsigned long ECHO_TIMEOUT_US = 30000UL;
const unsigned long MEASURE_MS = 100;
const float US_PER_CM = 58.0f;
const float MIN_CM = 2.0f;
const float MAX_CM = 400.0f;

void setup() {
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  digitalWrite(TRIG_PIN, LOW);
  Serial.begin(9600);
}

void loop() {
  delay(MEASURE_MS);
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  unsigned long echoUs = pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US);
  if (echoUs == 0) {
    Serial.println("NO_ECHO");
    return;
  }
  float cm = echoUs / US_PER_CM;
  if (cm < MIN_CM || cm > MAX_CM) {
    Serial.println("OUT_OF_RANGE");
    return;
  }
  Serial.print("distance_cm=");
  Serial.println(cm, 1);
}
