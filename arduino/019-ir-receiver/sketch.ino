#include <IRremote.hpp>

constexpr uint8_t IR_RECEIVE_PIN = 2;

void setup() {
  Serial.begin(115200);
  IrReceiver.begin(IR_RECEIVE_PIN, DISABLE_LED_FEEDBACK);
  Serial.println(F("IR_READY: point the remote at the receiver"));
}

void loop() {
  if (IrReceiver.decode()) {
    const uint8_t flags = IrReceiver.decodedIRData.flags;
    if (flags & IRDATA_FLAGS_WAS_OVERFLOW) {
      Serial.println(F("OVERFLOW: frame too long"));
    } else if (flags & IRDATA_FLAGS_PARITY_FAILED) {
      Serial.println(F("PARITY_ERROR: try again"));
    } else if (IrReceiver.decodedIRData.protocol == UNKNOWN) {
      Serial.println(F("UNKNOWN: unsupported protocol or noise"));
    } else {
      IrReceiver.printIRResultShort(&Serial);
      if (flags & IRDATA_FLAGS_IS_REPEAT) {
        Serial.println(F("REPEAT: held button frame"));
      } else {
        Serial.println(F("FRAME: decoded frame"));
      }
    }
    IrReceiver.resume();
  }
}
