"""RP2040 Pico + Adafruit HC-SR04 #3942. Echo divider: 10k + 10k."""
from machine import Pin, time_pulse_us
from time import sleep_us, sleep_ms

TRIG_GP = 16
ECHO_GP = 17
TIMEOUT_US = 30000
WAIT_MS = 100

trig = Pin(TRIG_GP, Pin.OUT, value=0)
echo = Pin(ECHO_GP, Pin.IN)

def measure_cm():
    trig.value(0)
    sleep_us(2)
    trig.value(1)
    sleep_us(10)
    trig.value(0)
    pulse_us = time_pulse_us(echo, 1, TIMEOUT_US)
    if pulse_us < 0:
        return None
    distance_cm = pulse_us / 58.0
    if not 2 <= distance_cm <= 400:
        return None
    return distance_cm

sleep_ms(WAIT_MS)
print("READY: HC-SR04, cm")
try:
    while True:
        distance = measure_cm()
        if distance is None:
            print("NO_READING: check target and wiring")
        else:
            print("distance_cm=%.1f" % distance)
        sleep_ms(WAIT_MS)
except KeyboardInterrupt:
    print("STOP")
finally:
    trig.value(0)
