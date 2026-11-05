from machine import ADC, Pin
from time import sleep_ms

x_axis = ADC(Pin(34), atten=ADC.ATTN_11DB)
y_axis = ADC(Pin(35), atten=ADC.ATTN_11DB)
button = Pin(18, Pin.IN, Pin.PULL_UP)

while True:
    x = x_axis.read_u16()
    y = y_axis.read_u16()
    pressed = button.value() == 0
    state = "pressed" if pressed else "released"
    print("X={} Y={} SW={}".format(x, y, state))
    sleep_ms(150)
