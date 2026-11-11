from machine import Pin
from time import sleep_ms
from ir_rx.nec import NEC_8


def on_receive(data, addr, ctrl):
    if data < 0:
        print("REPEAT")
    else:
        print("ADDR={:02X} CMD={:02X}".format(addr, data))


def on_error(code):
    print("RX_ERROR", code)


receiver = NEC_8(Pin(18, Pin.IN), on_receive)
receiver.error_function(on_error)
try:
    print("READY")
    while True:
        sleep_ms(100)
finally:
    receiver.close()

