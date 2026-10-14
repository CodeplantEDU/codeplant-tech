// CODEPLANT: UNO R3 + Adafruit 372 (10k NTC, B25/50=3950).
// Divider: 5V -- fixed 10k -- A0 -- NTC -- GND.
// Based on the divider/B-parameter method in Adafruit's Thermistor guide.
#include <math.h>
const byte NTC_PIN = A0;
const float R_FIXED = 10000.0;
const float R0 = 10000.0;  // NTC resistance at 25 Celsius
const float T0_K = 298.15;
const float BETA = 3950.0;

float temperatureC(int raw) {
  if (raw <= 0 || raw >= 1023) return NAN;
  float r = R_FIXED * raw / (1023.0 - raw);
  float invK = 1.0 / T0_K + log(r / R0) / BETA;
  return 1.0 / invK - 273.15;
}

void setup() {
  pinMode(NTC_PIN, INPUT);  // No internal pull-up.
  analogReference(DEFAULT);  // 5V divider; leave AREF unconnected.
  Serial.begin(9600);
}

void loop() {
  delay(1000);
  int raw = analogRead(NTC_PIN);
  float tempC = temperatureC(raw);
  if (isnan(tempC)) {
    Serial.print("ERROR: ADC_ENDPOINT raw=");
    Serial.println(raw);
    return;
  }
  Serial.print("raw=");
  Serial.print(raw);
  Serial.print(" temp_C=");
  Serial.println(tempC, 1);
}
