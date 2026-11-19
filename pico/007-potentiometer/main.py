from machine import Pin, ADC
from time import sleep_ms

POT_PIN = 26
PRINT_MS = 100
adc = ADC(Pin(POT_PIN))
try:
    print("READY: potentiometer -> GP26")
    while True:
        raw = adc.read_u16()
        print("raw_u16 =", raw)
        sleep_ms(PRINT_MS)
except KeyboardInterrupt:
    print("STOP")
except OSError as error:
    print("ADC_ERROR:", error)
