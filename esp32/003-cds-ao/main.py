from machine import Pin, ADC
from time import sleep_ms

SAMPLES = 8
THRESHOLD = 32768
adc = ADC(Pin(34), atten=ADC.ATTN_11DB)
adc.width(ADC.WIDTH_12BIT)
print("READY: AO -> GPIO34, 3.3V module")
try:
    while True:
        total = 0
        for _ in range(SAMPLES):
            total += adc.read_u16()
            sleep_ms(25)
        raw = total // SAMPLES
        if raw >= THRESHOLD:
            band = "AT_OR_ABOVE"
        else:
            band = "BELOW"
        print("raw_u16 =", raw, "band =", band)
except KeyboardInterrupt:
    print("STOP")
except OSError as error:
    print("ADC_ERROR:", error)
finally:
    adc.deinit()
