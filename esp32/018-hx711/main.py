from machine import Pin, SPI
from time import sleep_ms
from math import isfinite
from hx711_spi import HX711

SAMPLES = 10


def average_raw(sensor):
    total = 0
    for _ in range(SAMPLES):
        value = sensor.read()
        if value <= -8388608 or value >= 8388607:
            raise ValueError("ADC_SATURATED")
        total += value
    return total / SAMPLES


def calibrate(zero_raw, loaded_raw, known_g):
    if not isfinite(known_g) or not 0 < known_g <= 5000:
        raise ValueError("KNOWN_MASS_G_INVALID")
    counts_per_g = (loaded_raw - zero_raw) / known_g
    if not isfinite(counts_per_g) or abs(counts_per_g) < 1:
        raise ValueError("CALIBRATION_TOO_SMALL")
    return counts_per_g


def run():
    # HX711 SCK is driven by SPI MOSI; GPIO18 stays disconnected.
    clock = Pin(23, Pin.OUT, value=0)
    data = Pin(19, Pin.IN)
    spi = SPI(2, baudrate=1000000, polarity=0, phase=0,
              sck=Pin(18), mosi=clock, miso=data)
    try:
        sensor = HX711(clock, data, spi, gain=128)
        print("Remove load; wait until the empty platform is stable.")
        input("Press Enter to tare: ")
        zero_raw = average_raw(sensor)
        print("ZERO_OK raw=", zero_raw)
        known_g = float(input("Known mass in grams: "))
        if not isfinite(known_g) or not 0 < known_g <= 5000:
            raise ValueError("KNOWN_MASS_G_INVALID")
        print("Place that known mass; wait until stable.")
        input("Press Enter to calibrate: ")
        loaded_raw = average_raw(sensor)
        counts_per_g = calibrate(zero_raw, loaded_raw, known_g)
        print("CAL_OK counts_per_g=", counts_per_g)
        while True:
            raw = average_raw(sensor)
            mass_g = (raw - zero_raw) / counts_per_g
            print("raw=", raw, "mass_g=", round(mass_g, 1))
            sleep_ms(300)
    finally:
        spi.deinit()
        clock.init(Pin.OUT, value=0)


if __name__ == "__main__":
    try:
        run()
    except (OSError, ValueError) as error:
        print("STOP:", error)
        print("Power off both supplies before checking wiring/load.")
