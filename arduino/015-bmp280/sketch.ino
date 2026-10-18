// Arduino UNO R3 + Adafruit BMP280 #2651 STEMMA QT, I2C.
#include <Wire.h>
#include <Adafruit_BMP280.h>
#include <math.h>
Adafruit_BMP280 bmp;
uint8_t address = 0x77;

void setup() {
  Serial.begin(9600);
  Wire.begin();
  Wire.setWireTimeout(25000, true);
  if (!bmp.begin(address)) {
    address = 0x76;
    if (!bmp.begin(address)) {
      Serial.println("ERROR: BMP280_NOT_FOUND");
      while (true) { delay(1000); }
    }
  }
  Serial.print("READY address=0x");
  Serial.println(address, HEX);
}

void loop() {
  float tempC = bmp.readTemperature();
  float pressureHpa = bmp.readPressure() / 100.0F;
  if (!isfinite(tempC) || !isfinite(pressureHpa) ||
      tempC < -40.0F || tempC > 85.0F ||
      pressureHpa < 300.0F || pressureHpa > 1100.0F) {
    Serial.println("ERROR: BMP280_RANGE");
  } else {
    Serial.print("temp_C=");
    Serial.print(tempC, 2);
    Serial.print(" pressure_hPa=");
    Serial.println(pressureHpa, 2);
  }
  delay(1000);
}
