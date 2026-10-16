// UNO R3 + SunFounder 5-pin joystick, powered by UNO 5V.
const byte X_PIN = A0;
const byte Y_PIN = A1;
const byte SW_PIN = 2;

void setup() {
  pinMode(X_PIN, INPUT);
  pinMode(Y_PIN, INPUT);
  pinMode(SW_PIN, INPUT_PULLUP);
  analogReference(DEFAULT);
  Serial.begin(9600);
}

void loop() {
  int x = analogRead(X_PIN);
  int y = analogRead(Y_PIN);
  int sw = digitalRead(SW_PIN);
  Serial.print("x=");
  Serial.print(x);
  Serial.print(" y=");
  Serial.print(y);
  Serial.print(" sw=");
  Serial.println(sw);
  delay(100);
}
