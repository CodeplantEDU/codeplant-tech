from machine import Pin
from time import sleep_ms

PIR_PIN = 27
WARMUP_MS = 60000
SAMPLE_MS = 50
pir = Pin(PIR_PIN, Pin.IN, pull=None)
last_state = None

try:
    print("WAIT_60S")
    sleep_ms(WARMUP_MS)
    print("READY: GPIO27 input")
    while True:
        state = pir.value()
        if state != last_state:
            level = "HIGH" if state else "LOW"
            print("pir = {}, level = {}".format(state, level))
            last_state = state
        sleep_ms(SAMPLE_MS)
except KeyboardInterrupt:
    print("STOP")
