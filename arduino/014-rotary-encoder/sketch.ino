// UNO R3 + KY-040-type module, 5V; relative count, not degrees.
#include <RotaryEncoder.h>
const byte CLK_PIN = 2;
const byte DT_PIN = 3;
const byte SW_PIN = 4;
const unsigned long DEBOUNCE_MS = 50;
RotaryEncoder encoder(CLK_PIN, DT_PIN, RotaryEncoder::LatchMode::FOUR3);
long lastPosition = 0;
int lastRawSW = HIGH;
int stableSW = HIGH;
unsigned long changedAt = 0;

void setup() {
  pinMode(CLK_PIN, INPUT_PULLUP);
  pinMode(DT_PIN, INPUT_PULLUP);
  pinMode(SW_PIN, INPUT_PULLUP);
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(115200);
  lastRawSW = digitalRead(SW_PIN);
  changedAt = millis();
  Serial.println("READY pos=0 sw=1");
}

void loop() {
  encoder.tick();
  unsigned long now = millis();
  int rawSW = digitalRead(SW_PIN);
  if (rawSW != lastRawSW) {
    lastRawSW = rawSW;
    changedAt = now;
  }
  bool swChanged = false;
  if (rawSW != stableSW && now - changedAt >= DEBOUNCE_MS) {
    stableSW = rawSW;
    swChanged = true;
  }
  digitalWrite(LED_BUILTIN, stableSW == LOW ? HIGH : LOW);
  long position = encoder.getPosition();
  if (position != lastPosition || swChanged) {
    lastPosition = position;
    Serial.print("pos=");
    Serial.print(position);
    Serial.print(" sw=");
    Serial.println(stableSW);
  }
}
