// CODEPLANT TECH 02: UNO R3, serial input -> decision -> built-in LED.
// Send character '1' to turn LED L on, or '0' to turn it off.
// No external GPIO wiring. Serial Monitor: 9600 baud.
void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  Serial.println("Send 1: LED ON / Send 0: LED OFF");
}

void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    if (command == '0' || command == '1') {
      bool on = (command == '1');
      digitalWrite(LED_BUILTIN, on ? HIGH : LOW);
      Serial.println(on ? "LED ON" : "LED OFF");
    }
    // Other characters, including CR and LF, leave the LED unchanged.
  }
}
