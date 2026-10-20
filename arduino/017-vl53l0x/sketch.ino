// UNO R3 + Adafruit VL53L0X #3317 STEMMA QT, I2C, default mode.
#include <Wire.h>
#include <Adafruit_VL53L0X.h>
Adafruit_VL53L0X lox;
const uint8_t ADDRESS = 0x29;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setWireTimeout(25000, true);
  if (!lox.begin(ADDRESS, false, &Wire)) {
    Serial.println(F("ERROR: VL53L0X_NOT_FOUND_OR_INIT"));
    while (true) { delay(1000); }
  }
  Wire.setClock(100000);
  Wire.setWireTimeout(25000, true);
  Serial.println(F("READY address=0x29, distance in mm and cm"));
}

void loop() {
  VL53L0X_RangingMeasurementData_t measure = {};
  Wire.clearWireTimeoutFlag();
  VL53L0X_Error error = lox.rangingTest(&measure, false);
  if (Wire.getWireTimeoutFlag()) {
    Serial.println(F("ERROR: I2C_TIMEOUT"));
    Wire.clearWireTimeoutFlag();
  } else if (error != VL53L0X_ERROR_NONE) {
    Serial.print(F("ERROR: API_ERROR code="));
    Serial.println((int)error);
  } else if (measure.RangeStatus != 0) {
    Serial.print(F("RANGE_INVALID status="));
    Serial.println(measure.RangeStatus);
  } else {
    Serial.print(F("distance_mm="));
    Serial.print(measure.RangeMilliMeter);
    Serial.print(F(" distance_cm="));
    Serial.println(measure.RangeMilliMeter / 10.0f, 1);
  }
  delay(250);  // measurement time is added to this wait
}
