from machine import Pin, time_pulse_us
from time import sleep_us, sleep_ms

TRIG_PIN = 25
ECHO_PIN = 26
TIMEOUT_US = 30000
SAMPLE_MS = 100
US_PER_CM = 58.0
trig = Pin(TRIG_PIN, Pin.OUT, value=0)
echo = Pin(ECHO_PIN, Pin.IN)

try:
    print("READY: HC-SR04 -> GPIO25/GPIO26")
    while True:
        sleep_ms(SAMPLE_MS)
        try:
            trig.value(0)
            sleep_us(2)
            trig.value(1)
            sleep_us(10)
            trig.value(0)
            echo_us = time_pulse_us(echo, 1, TIMEOUT_US)
            if echo_us <= 0:
                print("NO_ECHO:", echo_us)
                continue
            distance_cm = echo_us / US_PER_CM
            if 2 <= distance_cm <= 400:
                print("echo_us = {}, distance_cm = {:.1f}".format(
                    echo_us, distance_cm))
            else:
                print("OUT_OF_RANGE")
        except OSError as error:
            print("SENSOR_ERROR:", error)
except KeyboardInterrupt:
    print("STOP")
finally:
    trig.value(0)
