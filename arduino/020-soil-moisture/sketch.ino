constexpr uint8_t SOIL_PIN = A0;
constexpr uint8_t ALERT_PIN = LED_BUILTIN;
// Replace both -1 values with your own readings; dry must exceed wet.
constexpr int DRY_RAW = -1;
constexpr int WET_RAW = -1;
// Classroom comparison thresholds, not a plant watering prescription.
constexpr int ALERT_ON_INDEX = 30;
constexpr int ALERT_OFF_INDEX = 40;
bool alert = false;

void setup() {
  Serial.begin(9600);
  pinMode(ALERT_PIN, OUTPUT);
  digitalWrite(ALERT_PIN, LOW);
  Serial.println(F("SOIL_READY: raw values first"));
}

void loop() {
  long total = 0;
  for (uint8_t i = 0; i < 10; i++) {
    total += analogRead(SOIL_PIN);
    delay(10);
  }
  const int raw = total / 10;
  Serial.print(F("raw="));
  Serial.print(raw);
  if (DRY_RAW < 0 || DRY_RAW > 1023 || WET_RAW < 0 ||
      WET_RAW > 1023 || DRY_RAW <= WET_RAW) {
    alert = false;
    Serial.println(F(" CALIBRATE_FIRST"));
  } else {
    const long indexUnclamped =
      (long)(DRY_RAW - raw) * 100L / (DRY_RAW - WET_RAW);
    const int wetIndex = constrain(indexUnclamped, 0L, 100L);
    if (wetIndex <= ALERT_ON_INDEX) alert = true;
    else if (wetIndex >= ALERT_OFF_INDEX) alert = false;
    Serial.print(F(" wet_index="));
    Serial.print(wetIndex);
    Serial.print(F(" alert="));
    Serial.print(alert ? 1 : 0);
    if (raw > DRY_RAW || raw < WET_RAW) Serial.print(F(" OUTSIDE_CAL"));
    Serial.println();
  }
  digitalWrite(ALERT_PIN, alert ? HIGH : LOW);
  delay(400);
}
