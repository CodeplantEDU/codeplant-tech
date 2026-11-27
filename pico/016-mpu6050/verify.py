
"""Host-side synthetic tests. No board or sensor is connected."""
import ast
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path
from struct import pack
from types import SimpleNamespace

root=Path(__file__).parent
source=(root/"main.py").read_text(encoding="utf-8")
tree=ast.parse(source)
readme=(root/"README.md").read_text(encoding="utf-8")
assert readme.split("~~~python\n",1)[1].split("\n~~~",1)[0]==source.strip()
diagram=json.loads((root/"diagram.json").read_text(encoding="utf-8"))
assert diagram["parts"][0]["physicalPins"]=={"3V3":36,"GND":8,"GP4":6,"GP5":7}
assert diagram["parts"][1]["logicReferences"]=={"HV":3.3,"LV":3.3}
expected=set()
for a,b in (("pico:3V3","shifter:LV"),("pico:3V3","shifter:HV"),("pico:3V3","imu:VCC"),
            ("pico:GND","shifter:GND_A"),("pico:GND","shifter:GND_B"),("pico:GND","imu:GND"),("imu:GND","imu:AD0"),
            ("pico:GP4","shifter:B1"),("pico:GP5","shifter:B2"),("shifter:A1","imu:SDA"),("shifter:A2","imu:SCL")):
    expected.add((a,b))
actual=diagram["connections"]
assert len(actual)==len(expected) and {(a,b) for a,b,*_ in actual}==expected
assert "freq=100_000" in source and "sda=Pin(4), scl=Pin(5)" in source

class Complete(Exception):
    pass

class Bus:
    def __init__(self, ids=None):
        self.ids={0x68:0x68} if ids is None else ids
        self.samples=0
        self.registers=[]
    def scan(self):
        return list(self.ids)
    def readfrom_mem(self,address,register,n):
        assert address in self.ids
        if (register,n)==(0x75,1):
            return bytes([self.ids[address]])
        assert (register,n)==(0x3b,14)
        self.samples+=1
        if self.samples>150:
            raise Complete
        gz=65 if self.samples<=100 else 3995
        return pack(">7h",0,0,16384,300,0,0,gz)
    def writeto_mem(self,address,register,data):
        assert address in self.ids
        self.registers.append((register,data[0]))

bus=Bus()
clock=0
period=2**20
def sleep_ms(ms):
    global clock
    clock+=ms*1000
def ticks_us():
    return clock%period
def ticks_diff(a,b):
    return (a-b+period//2)%period-period//2
def i2c(index,*,sda,scl,freq):
    assert (index,sda,scl,freq)==(0,4,5,100000)
    return bus
old={name:sys.modules.get(name) for name in ("machine","time")}
sys.modules["machine"]=SimpleNamespace(I2C=i2c,Pin=int)
sys.modules["time"]=SimpleNamespace(sleep_ms=sleep_ms,ticks_us=ticks_us,ticks_diff=ticks_diff)
try:
    m={"__name__":"verify"}
    exec(compile(tree,"main.py","exec"),m)
finally:
    for name,value in old.items():
        if value is None:
            sys.modules.pop(name,None)
        else:
            sys.modules[name]=value
assert m["decode"](pack(">7h",16384,-16384,0,700,131,-131,0))==(1,-1,0,1,-1,0)
assert m["decode"](pack(">7h",-32768,32767,0,0,0,0,0))[0]==-2

def close(actual,expected,tol=.1):
    assert all(abs(a-b)<tol for a,b in zip(actual,expected)),(actual,expected)
def initial(accel):
    return m["initial_orientation"](accel)
def angles(q):
    return m["angles"](q)
def update(q,accel,rate,seconds):
    return m["update_orientation"](q,accel,rate,seconds)
s,c=math.sin(math.pi/6),math.cos(math.pi/6)
close(angles(initial((0,s,c))),(30,0,0))
close(angles(initial((-s,0,c))),(0,30,0))
for accel,target in [((0,s,c),(30,0,0)),((-s,0,c),(0,30,0))]:
    q=initial((0,0,1))
    for _ in range(300):
        q=update(q,accel,(0,0,0),.02)
    close(angles(q),target)
q=initial((0,0,1))
for _ in range(50):
    q=update(q,(0,0,1),(0,0,30),.02)
close(angles(q),(0,0,30))
for _ in range(300):
    q=update(q,(0,0,1),(0,0,30),.02)
close(angles(q),(0,0,-150))
q=update(initial((0,0,1)),(5,0,0),(0,0,0),.02)
close(angles(q),(0,0,0))
for fake,error in ((Bus({}),OSError),(Bus({0x68:0x70}),ValueError)):
    try:
        m["configure"](fake)
    except error:
        pass
    else:
        raise AssertionError("Invalid I2C sensor accepted")
    assert fake.registers==[]
out=io.StringIO()
with redirect_stdout(out):
    try:
        m["run"]()
    except Complete:
        pass
lines=out.getvalue().splitlines()
assert lines[0]=="I2C: ['0x68']" and len([line for line in lines if line.startswith("R=")])==3,lines
assert lines[-1].endswith("Yrel=23.4 deg dt=20.0 ms"),lines[-1]
assert bus.registers==[(0x6b,0x80),(0x6b,1),(0x1a,4),(0x19,19),(0x1b,0),(0x1c,0)]
print("PASS: 11 wiring links, 3.3V rails, signed decode, init, synthetic tilt/yaw/wrap, I2C startup, bias and timed output")
