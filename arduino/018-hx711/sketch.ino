#include <HX711.h>
#include <math.h>

const byte DOUT_PIN = 3;
const byte SCK_PIN = 2;
// Set this to the actual known mass in grams before uploading; 0 disables calibration.
const float KNOWN_MASS_G = 0.0f;
const byte SAMPLES = 10;
HX711 scale;
long zeroRaw = 0;
float countsPerGram = 0;
bool zeroed = false;
bool calibrated = false;

bool averageRaw(long &value) {
  long sum = 0;
  for (byte i = 0; i < SAMPLES; ++i) {
    if (!scale.wait_ready_timeout(1000, 1)) {
      Serial.println(F("HX711_TIMEOUT: check wiring with USB disconnected"));
      return false;
    }
    long sample = scale.read();
    if (sample <= -8388608L || sample >= 8388607L) {
      Serial.println(F("ADC_SATURATED: check load and wiring"));
      return false;
    }
    sum += sample;
  }
  value = sum / SAMPLES;
  return true;
}

void setup() {
  Serial.begin(115200);
  scale.begin(DOUT_PIN, SCK_PIN, 128);
  Serial.println(F("Empty the mounted tray, wait for settling, then send t"));
  Serial.println(F("Set KNOWN_MASS_G before upload; place that mass then send c"));
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();
    if (command == 't') {
      zeroed = calibrated = false;
      if (averageRaw(zeroRaw)) {
        zeroed = true;
        Serial.println(F("ZERO_OK: place known mass, wait, then send c"));
      }
    } else if (command == 'c') {
      calibrated = false;
      if (!zeroed || !isfinite(KNOWN_MASS_G) ||
          KNOWN_MASS_G <= 0 || KNOWN_MASS_G > 5000) {
        Serial.println(F("CAL_REQUIRED: set known grams (0 < g <= 5000) and tare first"));
      } else {
        long raw;
        if (averageRaw(raw)) {
          countsPerGram = (raw - zeroRaw) / KNOWN_MASS_G;
          if (isfinite(countsPerGram) && countsPerGram != 0) {
            calibrated = true;
            Serial.print(F("CAL_OK counts_per_g="));
            Serial.println(countsPerGram, 6);
          } else {
            Serial.println(F("CAL_FAILED: no usable change; check mounting and known mass"));
          }
        }
      }
    }
  }
  if (calibrated) {
    long raw;
    if (averageRaw(raw)) {
      float massG = (raw - zeroRaw) / countsPerGram;
      if (fabs(massG) > 5000) Serial.println(F("OUT_OF_RANGE: remove load"));
      else {
        Serial.print(F("mass_g="));
        Serial.println(massG, 1);
      }
    }
  }
  delay(250);
}
