// CODEPLANT TECH 03: 5V-compatible four-pin LDR module, DO example.
const int CDS_DO_PIN = 2;
const int LIGHT_DETECTED = LOW; // SunFounder example; change after checking your module.

void setup() {
  pinMode(CDS_DO_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  int state = digitalRead(CDS_DO_PIN);
  digitalWrite(LED_BUILTIN, state == LIGHT_DETECTED ? HIGH : LOW);
  Serial.print("CDS DO: ");
  Serial.println(state);
  delay(500);
}
