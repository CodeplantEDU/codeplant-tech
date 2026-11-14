from machine import ADC, Pin
from time import sleep_ms

adc = ADC(Pin(26))

def read_average():
    return sum(adc.read_u16() for _ in range(8)) // 8

try:
    while True:
        print("AO raw:", read_average())
        sleep_ms(300)
except KeyboardInterrupt:
    print("Stopped")
