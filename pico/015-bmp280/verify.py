
"""Host-side checks with a fake I2C bus; this is not a hardware test."""
import ast
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from struct import pack
from types import SimpleNamespace

root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
assert "sda=Pin(4), scl=Pin(5), freq=100_000" in source
diagram = json.loads((root / "diagram.json").read_text(encoding="utf-8"))
assert diagram["parts"][0]["physicalPins"] == {"3V3": 36, "GND": 8, "GP4": 6, "GP5": 7}
nets = {("pico:3V3", "bmp:VIN"), ("pico:GND", "bmp:GND"),
        ("pico:GP4", "bmp:SDI"), ("pico:GP5", "bmp:SCK")}
assert {(a,b) for a,b,*_ in diagram["connections"]} == nets
assert len(diagram["connections"]) == len(nets)
schematic = (root / "circuit_preview.html").read_text(encoding="utf-8")
assert all(f'data-net="{a} {b}"' in schematic for a,b in nets)
readme = (root / "README.md").read_text(encoding="utf-8")
assert readme.split("~~~python\n",1)[1].split("\n~~~",1)[0] == source.strip()

TRIM = (27504, 26435, -1000, 36477, -10685, 3024, 2855, 140, -7, 15500, -14600, 6000)
RAW = (415148 << 4).to_bytes(3, "big") + (519888 << 4).to_bytes(3, "big")

class SampleComplete(Exception):
    pass

class Bus:
    def __init__(self, sensors, status=(0,0)):
        self.sensors = sensors
        self.status = iter(status)
        self.trace = []

    def scan(self):
        return list(self.sensors)

    def readfrom_mem(self, address, register, size):
        self.trace.append(("read", address, register, size))
        assert address in self.sensors
        if (register,size) == (0xD0,1):
            return bytes([self.sensors[address]])
        if (register,size) == (0xF3,1):
            return bytes([next(self.status)])
        if (register,size) == (0x88,24):
            return pack("<HhhHhhhhhhhh", *TRIM)
        if (register,size) == (0xF7,6):
            return RAW
        raise AssertionError((address,register,size))

    def writeto_mem(self, address, register, data):
        assert address in self.sensors
        self.trace.append(("write",address,register,data))

def simulate(sensors,status=(0,0),error=None):
    bus = Bus(sensors,status)
    delays = []
    def i2c(index,*,sda,scl,freq):
        assert (index,sda,scl,freq) == (0,4,5,100000)
        return bus
    def sleep(ms):
        delays.append(ms)
        if ms == 1000:
            raise SampleComplete
    try:
        previous_machine = sys.modules.get("machine")
        previous_time = sys.modules.get("time")
        sys.modules["machine"] = SimpleNamespace(I2C=i2c, Pin=int)
        sys.modules["time"] = SimpleNamespace(sleep_ms=sleep)
        module = {"__name__":"bench"}
        exec(compile(tree,"main.py","exec"),module)
    finally:
        sys.modules["time"] = previous_time
        if previous_machine is None:
            sys.modules.pop("machine",None)
        else:
            sys.modules["machine"] = previous_machine
    output = io.StringIO()
    caught = None
    with redirect_stdout(output):
        try:
            module["run"]()
        except (SampleComplete, OSError, ValueError) as exc:
            caught = exc
    assert isinstance(caught,error or SampleComplete),(caught,output.getvalue())
    if error is None:
        address = next(iter(sensors))
        assert ("write",address,0xF4,b"\x25") in bus.trace
        assert bus.trace[-2:]==[("read",address,0xF3,1),("read",address,0xF7,6)]
        assert delays==[10,20,1000]
        assert output.getvalue().splitlines()==[f"I2C: ['{hex(address)}']","T=25.08 C  P=1006.53 hPa"],output.getvalue()
        try:
            module["compensate"](519888,415148,TRIM[:3]+(0,)+TRIM[4:])
        except ValueError:
            pass
        else:
            raise AssertionError("Zero calibration gain accepted")
    else:
        assert not any(step[:1] == ("read",) and step[2] == 0xF7 for step in bus.trace)
simulate({0x77:0x58})
simulate({0x76:0x58})
simulate({},error=ValueError)
simulate({0x77:0x60},error=ValueError)
simulate({0x77:0x58,0x76:0x58},error=ValueError)
simulate({0x77:0x58},status=(1,),error=OSError)
simulate({0x77:0x58},status=(0,8),error=OSError)
print("PASS: 4 wiring nets, GPIO/README parity, both addresses, forced capture, compensation and error paths")
