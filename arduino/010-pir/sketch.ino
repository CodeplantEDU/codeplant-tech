const byte PIR_PIN = 2;
const unsigned long WARMUP_MS = 60000UL;
int lastMotion = -1;

void setup() {
  pinMode(PIR_PIN, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
  Serial.println("WAIT_60S");
  delay(WARMUP_MS);
  Serial.println("READY");
}

void loop() {
  int motion = digitalRead(PIR_PIN);
  digitalWrite(LED_BUILTIN, motion);
  if (motion != lastMotion) {
    Serial.print("pir=");
    Serial.println(motion);
    lastMotion = motion;
  }
  delay(50);
}
