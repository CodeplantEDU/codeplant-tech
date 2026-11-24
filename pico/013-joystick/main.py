from machine import ADC, Pin
from time import sleep_ms

x_axis = ADC(Pin(26))
y_axis = ADC(Pin(27))
button = Pin(16, Pin.IN)  # External 10k pull-up to 3V3 OUT

try:
    while True:
        x = x_axis.read_u16()
        y = y_axis.read_u16()
        pressed = button.value() == 0
        state = "pressed" if pressed else "released"
        print("X={} Y={} SW={}".format(x, y, state))
        sleep_ms(150)
except KeyboardInterrupt:
    print("STOP")
