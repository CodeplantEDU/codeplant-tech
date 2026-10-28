from machine import Pin, PWM
from time import sleep_ms

SERVO_PIN = 18
FREQUENCY_HZ = 50
CENTER_US = 1500
STEP_US = 100
HOLD_MS = 2000
COMPARE = False


def check_pulse(pulse_us):
    if not isinstance(pulse_us, int) or not 1400 <= pulse_us <= 1600:
        raise ValueError("pulse must be integer 1400..1600 us")
    return pulse_us


signal = None
servo = None
try:
    center = check_pulse(CENTER_US)
    if not isinstance(STEP_US, int) or not 0 <= STEP_US <= 100:
        raise ValueError("STEP_US must be integer 0..100")
    if not isinstance(HOLD_MS, int) or HOLD_MS < 2000:
        raise ValueError("HOLD_MS must be at least 2000")
    positions = (center,)
    if COMPARE:
        positions = (center, check_pulse(center - STEP_US),
                     center, check_pulse(center + STEP_US))
    signal = Pin(SERVO_PIN, Pin.OUT, value=0)
    servo = PWM(signal, freq=FREQUENCY_HZ, duty_ns=center * 1000)
    print("READY: external servo power ON only after wiring check")
    previous = None
    while True:
        for pulse_us in positions:
            servo.duty_ns(pulse_us * 1000)
            if pulse_us != previous:
                print("command_us =", pulse_us, "period_ms = 20")
                previous = pulse_us
            sleep_ms(HOLD_MS)
except KeyboardInterrupt:
    print("STOP: remove external servo power")
except (ValueError, OSError) as error:
    print("PWM_ERROR:", error)
finally:
    try:
        if servo is not None:
            servo.deinit()
    finally:
        if signal is not None:
            signal.init(Pin.OUT, value=0)
