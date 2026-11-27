from machine import I2C, Pin
from math import asin, atan2, cos, pi, sin, sqrt
from struct import unpack
from time import sleep_ms, ticks_diff, ticks_us

ADDRESS = 0x68
DEG = 180 / pi
RAD = pi / 180
GRAVITY_GAIN = 2.0
CAL_SAMPLES = 100

def decode(data):
    ax, ay, az, _temperature, gx, gy, gz = unpack(">7h", data)
    return (ax / 16384, ay / 16384, az / 16384,
            gx / 131, gy / 131, gz / 131)

def configure(i2c):
    addresses = i2c.scan()
    print("I2C:", [hex(address) for address in addresses])
    if ADDRESS not in addresses:
        raise OSError("MPU6050 0x68 not found; check AD0, wiring and power")
    if i2c.readfrom_mem(ADDRESS, 0x75, 1) != b'\x68':
        raise ValueError("MPU6050 WHO_AM_I mismatch")

    i2c.writeto_mem(ADDRESS, 0x6B, b'\x80')
    sleep_ms(100)
    i2c.writeto_mem(ADDRESS, 0x6B, b'\x01')
    sleep_ms(100)
    for register, value in ((0x1A, 4), (0x19, 19), (0x1B, 0), (0x1C, 0)):
        i2c.writeto_mem(ADDRESS, register, bytes([value]))

def read_sample(i2c):
    return decode(i2c.readfrom_mem(ADDRESS, 0x3B, 14))

def calibrate(i2c):
    print("Keep the sensor still for about 2 seconds.")
    sums = [0.0] * 6
    for _ in range(CAL_SAMPLES):
        sample = read_sample(i2c)
        for axis, value in enumerate(sample):
            sums[axis] += value
        sleep_ms(20)
    means = tuple(value / CAL_SAMPLES for value in sums)
    return means[:3], means[3:]

def initial_orientation(accel):
    ax, ay, az = accel
    magnitude = sqrt(ax * ax + ay * ay + az * az)
    if not 0.8 <= magnitude <= 1.2:
        raise ValueError("Start again with the module resting still")
    roll = atan2(ay, az)
    pitch = atan2(-ax, sqrt(ay * ay + az * az))
    cr, sr = cos(roll / 2), sin(roll / 2)
    cp, sp = cos(pitch / 2), sin(pitch / 2)
    return cr * cp, sr * cp, cr * sp, -sr * sp

def update_orientation(q, accel, corrected_dps, dt):
    w, x, y, z = q
    gx, gy, gz = (rate * RAD for rate in corrected_dps)
    ax, ay, az = accel
    magnitude = sqrt(ax * ax + ay * ay + az * az)
    if 0.90 <= magnitude <= 1.10:
        ax, ay, az = ax / magnitude, ay / magnitude, az / magnitude
        up_x = 2 * (x * z - w * y)
        up_y = 2 * (y * z + w * x)
        up_z = 1 - 2 * (x * x + y * y)
        gx += GRAVITY_GAIN * (ay * up_z - az * up_y)
        gy += GRAVITY_GAIN * (az * up_x - ax * up_z)
        gz += GRAVITY_GAIN * (ax * up_y - ay * up_x)

    half = dt / 2
    next_q = (w + half * (-x * gx - y * gy - z * gz),
              x + half * (w * gx + y * gz - z * gy),
              y + half * (w * gy - x * gz + z * gx),
              z + half * (w * gz + x * gy - y * gx))
    length = sqrt(sum(value * value for value in next_q))
    return tuple(value / length for value in next_q)

def angles(q):
    w, x, y, z = q
    roll = atan2(2 * (w * x + y * z), 1 - 2 * (x * x + y * y)) * DEG
    sin_pitch = max(-1.0, min(1.0, 2 * (w * y - z * x)))
    pitch = asin(sin_pitch) * DEG
    yaw = atan2(2 * (w * z + x * y), 1 - 2 * (y * y + z * z)) * DEG
    return roll, pitch, (yaw + 180) % 360 - 180

def run():
    i2c = I2C(0, sda=Pin(4), scl=Pin(5), freq=100_000)
    sleep_ms(100)
    configure(i2c)
    accel, gyro_bias = calibrate(i2c)
    q = initial_orientation(accel)
    print("gyro_bias [deg/s]:", gyro_bias)
    print("READY: roll_deg  pitch_deg  yaw_rel_deg")
    previous = last_print = ticks_us()

    while True:
        sleep_ms(20)
        sample = read_sample(i2c)
        now = ticks_us()
        dt = ticks_diff(now, previous) / 1_000_000
        previous = now
        if not 0 < dt <= 0.1:
            raise OSError("Sample timing gap; restart while the sensor is still")
        rotation = tuple(value - bias for value, bias in zip(sample[3:], gyro_bias))
        q = update_orientation(q, sample[:3], rotation, dt)
        if ticks_diff(now, last_print) >= 250_000:
            roll, pitch, yaw = angles(q)
            print("R={:.1f} P={:.1f} Yrel={:.1f} deg dt={:.1f} ms".format(
                  roll, pitch, yaw, dt * 1000))
            last_print = now

if __name__ == "__main__":
    run()
