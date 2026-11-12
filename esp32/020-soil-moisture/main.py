from machine import ADC, Pin
from time import sleep_ms

sensor = ADC(Pin(34), atten=ADC.ATTN_11DB)

while True:
    raw = sensor.read_u16()
    print('raw:', raw)
    sleep_ms(500)

