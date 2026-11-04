from machine import Pin
import onewire
import ds18x20
from time import sleep_ms

sensor = ds18x20.DS18X20(onewire.OneWire(Pin(18)))

while True:
    try:
        roms = [rom for rom in sensor.scan() if rom[0] == 0x28]
        if len(roms) != 1:
            print("Connect exactly one DS18B20:", len(roms))
        else:
            sensor.convert_temp()
            sleep_ms(750)
            temperature = sensor.read_temp(roms[0])
            print("{:.2f} C".format(temperature))
    except Exception as error:  # The driver raises Exception for CRC errors.
        print("1-Wire error:", error)
    sleep_ms(1000)
