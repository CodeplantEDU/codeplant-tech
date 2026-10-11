#include <DHT.h>
const byte DHT_PIN = 2;
const unsigned long READ_MS = 2500;
DHT dht(DHT_PIN, DHT22);

void setup() {
  Serial.begin(9600);
  dht.begin();
}

void loop() {
  delay(READ_MS);
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) {
    Serial.println("ERROR: DHT22");
    return;
  }
  Serial.print("temp_C=");
  Serial.print(t, 1);
  Serial.print(" humidity_pct=");
  Serial.println(h, 1);
}
