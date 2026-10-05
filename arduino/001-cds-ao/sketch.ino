const int CDS_AO_PIN = A0;

void setup() {
  Serial.begin(9600);
}

void loop() {
  int cdsValue = analogRead(CDS_AO_PIN);

  Serial.print("CDS AO: ");
  Serial.println(cdsValue);

  delay(500);
}
