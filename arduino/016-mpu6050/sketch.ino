// UNO R3 + Adafruit MPU6050 #3886 STEMMA QT, 5V I2C.
#include <Wire.h>
#include <Adafruit_MPU6050.h>
Adafruit_MPU6050 mpu;
const uint8_t ADDRESS = 0x68;

void setup() {
  Serial.begin(115200);
  Wire.begin();
  Wire.setWireTimeout(25000, true);
  if (!mpu.begin(ADDRESS)) {
    Serial.println("ERROR: MPU6050_NOT_FOUND");
    while (true) { delay(1000); }
  }
  mpu.setAccelerometerRange(MPU6050_RANGE_2_G);
  mpu.setGyroRange(MPU6050_RANGE_250_DEG);
  mpu.setFilterBandwidth(MPU6050_BAND_21_HZ);
  Serial.println("READY address=0x68");
}

void loop() {
  Wire.beginTransmission(ADDRESS);
  if (Wire.endTransmission() != 0) {
    Serial.println("ERROR: I2C_ACK");
    delay(500);
    return;
  }
  sensors_event_t a, g, t;
  mpu.getEvent(&a, &g, &t);
  Serial.print("acc_ms2=");
  Serial.print(a.acceleration.x, 2); Serial.print(",");
  Serial.print(a.acceleration.y, 2); Serial.print(",");
  Serial.print(a.acceleration.z, 2);
  Serial.print(" gyro_rads=");
  Serial.print(g.gyro.x, 2); Serial.print(",");
  Serial.print(g.gyro.y, 2); Serial.print(",");
  Serial.println(g.gyro.z, 2);
  delay(500);
}
