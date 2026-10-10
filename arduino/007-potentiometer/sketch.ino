// UNO R3: outer terminals to 5V/GND; middle wiper to A0.
const byte POT_PIN = A0;
const unsigned long PRINT_MS = 100;

void setup() {
  pinMode(POT_PIN, INPUT);  // Do not enable INPUT_PULLUP.
  Serial.begin(9600);
}

void loop() {
  int raw = analogRead(POT_PIN);
  Serial.print("raw=");
  Serial.println(raw);
  delay(PRINT_MS);
}
