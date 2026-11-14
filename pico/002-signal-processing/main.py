from machine import ADC, Pin, PWM
from time import sleep_ms

adc = ADC(Pin(26))
led = PWM(Pin("LED"), freq=1000, duty_u16=0)

try:
    while True:
        raw = adc.read_u16()
        led.duty_u16(raw)
        print(raw)
        sleep_ms(200)
finally:
    led.deinit()
    Pin("LED", Pin.OUT, value=0)
