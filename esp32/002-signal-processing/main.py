from machine import Pin, PWM

levels = {"0": 0, "25": 16384, "50": 32768,
          "75": 49151, "100": 65535}
pwm = PWM(Pin(25), freq=1000, duty_u16=0)
print("READY: 0 / 25 / 50 / 75 / 100, q: stop")
try:
    while True:
        command = input("duty> ").strip()
        if command == "q":
            break
        if command not in levels:
            print("USE: 0 / 25 / 50 / 75 / 100 / q")
            continue
        requested = levels[command]
        pwm.duty_u16(requested)
        print("requested_u16 =", requested)
except (KeyboardInterrupt, EOFError):
    pass
finally:
    pwm.duty_u16(0)
    pwm.deinit()
    Pin(25, Pin.OUT, value=0)
    print("STOP")
