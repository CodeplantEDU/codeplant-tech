from machine import Pin
from time import sleep_ms

led = Pin("LED", Pin.OUT, value=0)
print("Pico ready")

for _ in range(3):
    led.on()
    sleep_ms(500)
    led.off()
    sleep_ms(500)

print("Done")
