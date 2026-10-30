from machine import Pin, ADC
from time import sleep_ms

POT_PIN = 34
PRINT_MS = 100
adc = ADC(Pin(POT_PIN), atten=ADC.ATTN_11DB)
try:
    adc.width(ADC.WIDTH_12BIT)
    print("READY: potentiometer -> GPIO34")
    while True:
        raw = adc.read_u16()
        print("raw_u16 =", raw)
        sleep_ms(PRINT_MS)
except KeyboardInterrupt:
    print("STOP")
except OSError as error:
    print("ADC_ERROR:", error)
finally:
    adc.deinit()
