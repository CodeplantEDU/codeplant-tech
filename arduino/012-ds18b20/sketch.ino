// UNO R3 + one DS18B20 TO-92, external 5V power.
// Flat face forward: GND, DQ, VDD; 4.7k pull-up from DQ to 5V.
#include <OneWire.h>
#include <DallasTemperature.h>
const byte DATA_PIN = 2;
OneWire oneWire(DATA_PIN);
DallasTemperature sensors(&oneWire);

void setup() {
  Serial.begin(9600);
  sensors.begin();
  sensors.setResolution(12);
  sensors.setWaitForConversion(true);
}

void loop() {
  delay(1000);
  sensors.requestTemperatures();
  float tempC = sensors.getTempCByIndex(0);
  if (tempC == DEVICE_DISCONNECTED_C) {
    Serial.println("ERROR: DS18B20");
    return;
  }
  Serial.print("temp_C=");
  Serial.println(tempC, 2);
}
