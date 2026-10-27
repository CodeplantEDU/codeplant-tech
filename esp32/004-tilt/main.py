# CODEPLANT TECH 04 - ESP32 DevKit v1 / MicroPython 1.29.0
from machine import Pin
from time import ticks_ms, ticks_diff, sleep_ms

TILT_PIN = 27
DEBOUNCE_MS = 50
POLL_MS = 5

tilt = Pin(TILT_PIN, Pin.IN, Pin.PULL_UP)
try:
    last_raw = tilt.value()
    stable = None
    changed_at = ticks_ms()
    print("READY: GPIO27, pull-up, debounce 50ms")
    while True:
        raw = tilt.value()
        now = ticks_ms()
        if raw != last_raw:
            last_raw = raw
            changed_at = now
        if (stable is None or raw != stable) and (
            ticks_diff(now, changed_at) >= DEBOUNCE_MS
        ):
            stable = raw
            contact = "CLOSED" if stable == 0 else "OPEN"
            print("state =", stable, "contact =", contact)
        sleep_ms(POLL_MS)
except KeyboardInterrupt:
    print("STOP")
except OSError as exc:
    print("PIN_ERROR:", exc)
