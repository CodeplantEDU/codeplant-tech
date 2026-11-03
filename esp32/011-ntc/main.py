from machine import ADC, Pin
from time import sleep_ms

ADC_PIN = 34
SAMPLES = 10
GAP_MS = 10
WAIT_MS = 1000
adc = ADC(Pin(ADC_PIN), atten=ADC.ATTN_11DB)

try:
    print("READY: NTC raw input GPIO34")
    while True:
        sleep_ms(WAIT_MS)
        total = 0
        endpoint = False
        for _ in range(SAMPLES):
            value = adc.read_u16()
            total += value
            if value == 0 or value == 65535:
                endpoint = True
            sleep_ms(GAP_MS)
        raw = total // SAMPLES
        if endpoint:
            print("ADC_ENDPOINT raw_u16 =", raw)
        else:
            print("raw_u16 =", raw)
except KeyboardInterrupt:
    print("STOP")
except OSError as error:
    print("ADC_ERROR:", error)
