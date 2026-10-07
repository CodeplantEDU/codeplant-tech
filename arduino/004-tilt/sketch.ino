// CODEPLANT TECH 04: two-pin mechanical ball tilt switch
const byte TILT_PIN = 2;
const unsigned long DEBOUNCE_MS = 50; // Increase if contacts flicker.
int lastRaw = HIGH;
int stableState = HIGH;
unsigned long changedAt = 0;

void setup() {
  pinMode(TILT_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.begin(9600);
  lastRaw = digitalRead(TILT_PIN);
  stableState = lastRaw;
  changedAt = millis();
  digitalWrite(LED_BUILTIN, stableState == LOW ? HIGH : LOW);
  Serial.println(stableState); // Initial state, then only stable changes.
}

void loop() {
  int raw = digitalRead(TILT_PIN);
  unsigned long now = millis();
  if (raw != lastRaw) {
    lastRaw = raw;
    changedAt = now;
  }
  if (raw != stableState && now - changedAt >= DEBOUNCE_MS) {
    stableState = raw;
    digitalWrite(LED_BUILTIN, stableState == LOW ? HIGH : LOW);
    Serial.println(stableState);
  }
}
