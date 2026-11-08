from machine import I2C, Pin
from time import sleep_ms
from struct import unpack

ADDR = 0x68
ACCEL_SCALE = 16384.0
GYRO_SCALE = 131.0

def decode(data):
    if len(data) != 14:
        raise ValueError("Expected 14 bytes")
    ax, ay, az, temp, gx, gy, gz = unpack(">7h", data)
    accel_g = (ax / ACCEL_SCALE, ay / ACCEL_SCALE, az / ACCEL_SCALE)
    gyro_dps = (gx / GYRO_SCALE, gy / GYRO_SCALE, gz / GYRO_SCALE)
    return accel_g, gyro_dps

def run():
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    sleep_ms(100)
    print("I2C:", [hex(a) for a in i2c.scan()])
    if i2c.readfrom_mem(ADDR, 0x75, 1) != b'\x68':
        raise ValueError("MPU6050 ID mismatch")
    i2c.writeto_mem(ADDR, 0x6B, b'\x01')
    sleep_ms(100)
    i2c.writeto_mem(ADDR, 0x1A, b'\x03')
    i2c.writeto_mem(ADDR, 0x19, b'\x09')
    i2c.writeto_mem(ADDR, 0x1B, b'\x00')
    i2c.writeto_mem(ADDR, 0x1C, b'\x00')
    while True:
        data = i2c.readfrom_mem(ADDR, 0x3B, 14)
        accel_g, gyro_dps = decode(data)
        print("a[g] X={:.2f} Y={:.2f} Z={:.2f}".format(*accel_g))
        print("w[deg/s] X={:.2f} Y={:.2f} Z={:.2f}".format(*gyro_dps))
        sleep_ms(200)

if __name__ == "__main__":
    run()
