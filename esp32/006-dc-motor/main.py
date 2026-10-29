from machine import Pin, PWM
from time import sleep_ms

ENA_PIN = 25
IN1_PIN = 26
IN2_PIN = 27
FREQUENCY_HZ = 1000
LOW_PERCENT = 70
HIGH_PERCENT = 90
RUN_MS = 2000
STOP_MS = 2000


def duty_value(percent):
    if type(percent) is not int or not 0 <= percent <= 100:
        raise ValueError("percent must be integer 0..100")
    return (percent * 65535 + 50) // 100


def coast():
    pwm.duty_u16(0)
    in1.value(0)
    in2.value(0)
    print("COAST: drive disabled, wait_ms =", STOP_MS)
    sleep_ms(STOP_MS)


def stage(reverse, percent):
    value = duty_value(percent)
    pwm.duty_u16(0)
    in1.value(0 if reverse else 1)
    in2.value(1 if reverse else 0)
    pwm.duty_u16(value)
    print("direction =", "B" if reverse else "A",
          "command_pct =", percent, "duty_u16 =", value)
    sleep_ms(RUN_MS)


ena = None
in1 = None
in2 = None
pwm = None
try:
    duty_value(LOW_PERCENT)
    duty_value(HIGH_PERCENT)
    if not 0 < LOW_PERCENT < HIGH_PERCENT <= 100:
        raise ValueError("require 0 < LOW_PERCENT < HIGH_PERCENT <= 100")
    if type(RUN_MS) is not int or RUN_MS < 2000:
        raise ValueError("RUN_MS must be at least 2000")
    if type(STOP_MS) is not int or STOP_MS < 2000:
        raise ValueError("STOP_MS must be at least 2000")
    ena = Pin(ENA_PIN, Pin.OUT, value=0)
    in1 = Pin(IN1_PIN, Pin.OUT, value=0)
    in2 = Pin(IN2_PIN, Pin.OUT, value=0)
    pwm = PWM(ena, freq=FREQUENCY_HZ, duty_u16=0)
    print("READY: check wiring, then external logic 5V and motor 6V ON")
    while True:
        command = input("run = one sequence, q = quit > ").strip().lower()
        if command == "q":
            break
        if command != "run":
            print("USE run or q; drive remains disabled")
            continue
        coast()
        stage(False, LOW_PERCENT)
        stage(False, HIGH_PERCENT)
        coast()
        stage(True, LOW_PERCENT)
        stage(True, HIGH_PERCENT)
        coast()
except KeyboardInterrupt:
    print("STOP: remove external power")
except (ValueError, OSError, EOFError) as error:
    print("MOTOR_ERROR:", error)
finally:
    try:
        if pwm is not None:
            try:
                pwm.duty_u16(0)
            finally:
                pwm.deinit()
    finally:
        try:
            if ena is not None:
                ena.init(Pin.OUT, value=0)
        finally:
            try:
                if in1 is not None:
                    in1.init(Pin.OUT, value=0)
            finally:
                if in2 is not None:
                    in2.init(Pin.OUT, value=0)
