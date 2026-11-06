from machine import Pin
from time import sleep_ms, ticks_ms, ticks_diff

CLK = Pin(18, Pin.IN, Pin.PULL_UP)
DT = Pin(19, Pin.IN, Pin.PULL_UP)
SW = Pin(21, Pin.IN, Pin.PULL_UP)
DEBOUNCE_MS = 30

# Index: previous A/B followed by current A/B.
STEP = (0, -1, 1, 0, 1, 0, 0, -1, -1, 0, 0, 1, 0, 1, -1, 0)

def read_ab():
    return (CLK.value() << 1) | DT.value()

def advance(previous, current, pending):
    if (previous ^ current) == 3:
        return 0, 0
    pending += STEP[(previous << 2) | current]
    if pending == 4:
        return 0, 1
    if pending == -4:
        return 0, -1
    return pending, 0

def run():
    previous = read_ab()
    pending = position = 0
    stable = raw = SW.value()
    changed_at = ticks_ms()
    print("pos=", position, "sw=", stable)
    while True:
        current = read_ab()
        pending, delta = advance(previous, current, pending)
        previous = current
        position += delta

        sample = SW.value()
        now = ticks_ms()
        if sample != raw:
            raw, changed_at = sample, now
        changed = raw != stable and ticks_diff(now, changed_at) >= DEBOUNCE_MS
        if changed:
            stable = raw
        if delta or changed:
            print("pos=", position, "sw=", stable)
        sleep_ms(1)

if __name__ == "__main__":
    run()
