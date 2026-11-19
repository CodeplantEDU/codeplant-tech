from machine import Pin
from time import sleep_ms
import dht

DHT_PIN = 16
WAIT_MS = 2500
sensor = dht.DHT22(Pin(DHT_PIN))

try:
    print("READY: DHT22 -> GP16")
    sleep_ms(WAIT_MS)
    while True:
        try:
            sensor.measure()
            temperature = sensor.temperature()
            humidity = sensor.humidity()
            print("T = {:.1f} C, RH = {:.1f} %".format(
                temperature, humidity))
        except OSError as error:
            print("DHT_ERROR:", error)
        sleep_ms(WAIT_MS)
except KeyboardInterrupt:
    print("STOP")
