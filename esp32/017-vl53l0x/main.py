from machine import I2C, Pin
from time import sleep_ms
from vl53l0x import VL53L0X

MIN_MM = 50
MAX_MM = 1000

def sample(sensor):
    distance_mm = sensor.range
    if MIN_MM <= distance_mm <= MAX_MM:
        return distance_mm
    return None

def run():
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    sleep_ms(100)
    addresses = i2c.scan()
    print("I2C:", [hex(a) for a in addresses])
    if 0x29 not in addresses:
        raise OSError("VL53L0X address 0x29 not found")
    sensor = VL53L0X(i2c, io_timeout_ms=1000)
    sensor.measurement_timing_budget = 33000
    while True:
        distance_mm = sample(sensor)
        if distance_mm is None:
            print("CHECK_TARGET")
        else:
            print("distance_mm=", distance_mm)
        sleep_ms(200)

if __name__ == "__main__":
    run()
