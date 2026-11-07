from machine import I2C, Pin
from time import sleep_ms
from struct import unpack

def compensate(raw_t, raw_p, trim):
    t1, t2, t3, p1, p2, p3, p4, p5, p6, p7, p8, p9 = trim
    dt = raw_t / 16384 - t1 / 1024
    fine = dt * t2 + (raw_t / 131072 - t1 / 8192) ** 2 * t3
    v = fine / 2 - 64000
    offset = (v * v * p6 / 32768 + v * p5 * 2) / 4 + p4 * 65536
    gain = (1 + (p3 * v * v / 524288 + p2 * v) / 524288 / 32768) * p1
    if gain == 0:
        raise ValueError("BMP280 trim")
    pressure = (1048576 - raw_p - offset / 4096) * 6250 / gain
    pressure += (p9 * pressure * pressure / 2147483648
                 + pressure * p8 / 32768 + p7) / 16
    return fine / 5120, pressure / 100

def run():
    i2c = I2C(0, sda=Pin(21), scl=Pin(22), freq=100000)
    sleep_ms(10)
    addresses = i2c.scan()
    print("I2C:", [hex(a) for a in addresses])
    matches = [a for a in (0x77, 0x76) if a in addresses
               and i2c.readfrom_mem(a, 0xD0, 1) == b'\x58']
    if len(matches) != 1:
        raise ValueError("Connect exactly one BMP280 (ID 0x58)")
    addr = matches[0]
    trim = unpack("<HhhHhhhhhhhh", i2c.readfrom_mem(addr, 0x88, 24))
    while True:
        i2c.writeto_mem(addr, 0xF4, b'\x25')
        sleep_ms(20)
        if i2c.readfrom_mem(addr, 0xF3, 1)[0] & 0x08:
            raise OSError("BMP280 conversion still busy")
        data = i2c.readfrom_mem(addr, 0xF7, 6)
        raw_p = int.from_bytes(data[:3], "big") >> 4
        raw_t = int.from_bytes(data[3:], "big") >> 4
        if 0x80000 in (raw_t, raw_p):
            raise ValueError("BMP280 measurement unavailable")
        temp_c, pressure_hpa = compensate(raw_t, raw_p, trim)
        print("T={:.2f} C  P={:.2f} hPa".format(temp_c, pressure_hpa))
        sleep_ms(1000)

if __name__ == "__main__":
    run()
