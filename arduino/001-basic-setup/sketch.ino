// CODEPLANT TECH 01: UNO R3 + Arduino IDE
// LED L: 1 second on, 1 second off. Serial: one line every 2 seconds.
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(LED_BUILTIN, HIGH);
  Serial.println("UNO READY");
  delay(1000);
  digitalWrite(LED_BUILTIN, LOW);
  delay(1000);
}
