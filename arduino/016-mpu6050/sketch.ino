// CODEPLANT TECH 16: UNO R3 + blue 8-pin GY-521 + BSS138 I2C level shifter.
// Educational 6-DoF attitude estimate. Yaw is relative, not a compass heading.
#include <Wire.h>
#include <MadgwickAHRS.h>
#include <math.h>

const uint8_t ADDRESS = 0x68;  // AD0 -> GND
const uint32_t PERIOD_US = 20000;  // target 50 updates/s
const float G0 = 9.80665f;
Madgwick filter;
float biasX = 0, biasY = 0, biasZ = 0;  // stationary gyro bias, deg/s
float yawZero = 0;
uint32_t lastSample = 0, lastPrint = 0;
struct Sample { float ax, ay, az, gx, gy, gz; };

void stopWith(const __FlashStringHelper *message) {
  Serial.println(message);
  while (true) { delay(1000); }  // fix the cause, then press RESET
}

bool writeRegister(uint8_t reg, uint8_t value) {
  Wire.beginTransmission(ADDRESS);
  Wire.write(reg); Wire.write(value);
  return Wire.endTransmission() == 0;
}

bool readBytes(uint8_t reg, uint8_t count, uint8_t *data) {
  Wire.clearWireTimeoutFlag();
  Wire.beginTransmission(ADDRESS); Wire.write(reg);
  if (Wire.endTransmission(false) != 0) return false;
  if (Wire.requestFrom(ADDRESS, count) != count) return false;
  for (uint8_t i = 0; i < count; ++i) data[i] = Wire.read();
  return !Wire.getWireTimeoutFlag();
}

int16_t signed16(const uint8_t *b) {
  return (int16_t)(((uint16_t)b[0] << 8) | b[1]);
}

bool readSample(Sample &s) {
  uint8_t b[14];
  if (!readBytes(0x3B, sizeof(b), b)) return false;
  // +/-2g: 16384 LSB/g; +/-250 deg/s: 131 LSB/(deg/s).
  s.ax = signed16(b) * (G0 / 16384.0f);
  s.ay = signed16(b + 2) * (G0 / 16384.0f);
  s.az = signed16(b + 4) * (G0 / 16384.0f);
  // b[6..7] is temperature, not a gyro axis.
  s.gx = signed16(b + 8) / 131.0f;
  s.gy = signed16(b + 10) / 131.0f;
  s.gz = signed16(b + 12) / 131.0f;
  return true;
}

float norm(const Sample &s) {
  return sqrtf(s.ax*s.ax + s.ay*s.ay + s.az*s.az);
}

float wrap180(float degrees) {
  while (degrees >= 180.0f) degrees -= 360.0f;
  while (degrees < -180.0f) degrees += 360.0f;
  return degrees;
}

void calibrate() {
  Serial.println(F("CALIBRATING: flat, component side up; keep still for 5 s"));
  float sum[3] = {0}, sum2[3] = {0};
  const uint16_t N = 250;
  for (uint16_t i = 0; i < N; ++i) {
    Sample s;
    if (!readSample(s)) stopWith(F("ERROR: I2C_READ"));
    // Teaching thresholds: require a nearly level, stationary start.
    if (fabsf(norm(s)-G0) > 0.6f || fabsf(s.ax) > 1.7f ||
        fabsf(s.ay) > 1.7f || s.az < 9.0f ||
        fabsf(s.gx) > 5 || fabsf(s.gy) > 5 || fabsf(s.gz) > 5)
      stopWith(F("ERROR: CAL_MOVE_OR_NOT_LEVEL"));
    float g[3] = {s.gx, s.gy, s.gz};
    for (uint8_t k = 0; k < 3; ++k) { sum[k] += g[k]; sum2[k] += g[k]*g[k]; }
    delay(20);
  }
  float mean[3];
  for (uint8_t k = 0; k < 3; ++k) {
    mean[k] = sum[k]/N;
    float variance = sum2[k]/N - mean[k]*mean[k];
    if (variance > 0.64f) stopWith(F("ERROR: CAL_NOISE"));
  }
  biasX = mean[0]; biasY = mean[1]; biasZ = mean[2];
}

void setup() {
  Serial.begin(115200);
  Wire.begin(); Wire.setClock(100000); Wire.setWireTimeout(25000, true);
  uint8_t who = 0;
  if (!readBytes(0x75, 1, &who) || who != 0x68)
    stopWith(F("ERROR: MPU6050_NOT_FOUND"));
  if (!writeRegister(0x6B, 0x80)) stopWith(F("ERROR: I2C_CONFIG"));
  delay(100);  // reset any settings left by an earlier sketch
  if (!writeRegister(0x6B, 0x01)) stopWith(F("ERROR: I2C_CONFIG"));
  delay(100);  // wake, use X gyro PLL clock
  if (!writeRegister(0x1A, 0x04) || !writeRegister(0x19, 19) ||
      !writeRegister(0x1B, 0x00) || !writeRegister(0x1C, 0x00))
    stopWith(F("ERROR: I2C_CONFIG"));
  delay(1000);
  calibrate();
  filter.begin(50.0f);
  yawZero = filter.getYaw();
  Serial.print(F("BIAS_DPS=")); Serial.print(biasX, 3); Serial.print(',');
  Serial.print(biasY, 3); Serial.print(','); Serial.println(biasZ, 3);
  Serial.println(F("READY: roll_deg pitch_deg yaw_rel_deg; send z to zero yaw"));
  lastSample = micros(); lastPrint = millis();
}

void loop() {
  if ((uint32_t)(micros()-lastSample) < PERIOD_US) return;
  Sample s;
  if (!readSample(s)) stopWith(F("ERROR: I2C_READ"));
  uint32_t now = micros();
  uint32_t elapsed = now-lastSample; lastSample = now;
  if (elapsed > 100000UL) stopWith(F("ERROR: TIME_GAP"));
  if (fabsf(s.ax) > 19.0f || fabsf(s.ay) > 19.0f || fabsf(s.az) > 19.0f ||
      fabsf(s.gx) > 240 || fabsf(s.gy) > 240 || fabsf(s.gz) > 240)
    stopWith(F("ERROR: NEAR_RANGE_LIMIT"));
  // begin() updates only dt; it does not reset the quaternion.
  filter.begin(1000000.0f/elapsed);
  filter.updateIMU(s.gx-biasX, s.gy-biasY, s.gz-biasZ, s.ax, s.ay, s.az);
  float roll = filter.getRoll(), pitch = filter.getPitch(), yaw = filter.getYaw();
  if (!isfinite(roll) || !isfinite(pitch) || !isfinite(yaw))
    stopWith(F("ERROR: FILTER_VALUE"));
  while (Serial.available()) {
    char command = Serial.read();
    if (command == 'z' || command == 'Z') { yawZero = yaw; Serial.println(F("YAW_ZERO")); }
  }
  if ((uint32_t)(millis()-lastPrint) >= 100) {
    lastPrint = millis();
    Serial.print(F("roll_deg=")); Serial.print(roll, 1);
    Serial.print(F(" pitch_deg=")); Serial.print(pitch, 1);
    Serial.print(F(" yaw_rel_deg=")); Serial.print(wrap180(yaw-yawZero), 1);
    Serial.print(F(" acc_ms2=")); Serial.print(norm(s), 2);
    Serial.print(F(" dt_ms=")); Serial.println(elapsed/1000.0f, 1);
  }
}
