
import ast
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path
from types import SimpleNamespace

root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
found = {}
for node in tree.body:
    if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
        if isinstance(node.value.func, ast.Name) and node.value.func.id == "Pin":
            found[node.targets[0].id] = ast.unparse(node.value)
assert found == {key: f"Pin({gpio}, Pin.IN, Pin.PULL_UP)" for key, gpio in
                 (("CLK", 18), ("DT", 19), ("SW", 20))}
diagram = json.loads((root / "diagram.json").read_text(encoding="utf-8"))
nets = {("pico:GP18", "enc:CLK"), ("pico:GP19", "enc:DT"),
        ("pico:GP20", "enc:SW"), ("pico:3V3", "enc:VCC"), ("pico:GND", "enc:GND")}
assert {(a,b) for a,b,*_ in diagram["connections"]} == nets
assert len(diagram["connections"]) == len(nets)
assert diagram["parts"][0]["physicalPins"] == {"GP18":24, "GP19":25, "GP20":26,"3V3":36,"GND":38}
circuit = (root / "circuit_preview.html").read_text(encoding="utf-8")
assert all(f'data-net="{a} {b}"' in circuit for a,b in nets)
readme = (root / "README.md").read_text(encoding="utf-8")
assert readme.split("~~~python\n",1)[1].split("\n~~~",1)[0] == source.strip()
states = [3,1,0,2,3,2,0,1,3]
button = [1] + [1]*len(states) + [0,1,0] + [0]*31 + [1]*32
frames = list(zip(states + [3]*(len(button)-len(states)), button))
tick = 0
delays=[]
class Pin:
    IN = 0
    PULL_UP = 1
    def __init__(self, gpio, mode, pull):
        assert (mode,pull) == (self.IN,self.PULL_UP)
        self.gpio = gpio
    def value(self):
        ab, sw = frames[tick]
        return {18: ab >> 1,19: ab & 1,20: sw}[self.gpio]
def sleep_ms(ms):
    global tick
    delays.append(ms)
    tick += 1
    if tick == len(frames):
        raise KeyboardInterrupt
def ticks_ms():
    return (tick+1010) % 1024
def ticks_diff(a,b):
    return (a-b+512)%1024-512
originals = {mod:sys.modules.get(mod) for mod in ("machine","time")}
sys.modules["machine"] = SimpleNamespace(Pin=Pin)
sys.modules["time"] = SimpleNamespace(sleep_ms=sleep_ms, ticks_ms=ticks_ms, ticks_diff=ticks_diff)
try:
    ns = {"__name__":"encoder_test"}
    exec(compile(tree,"main.py","exec"),ns)
    def count(sequence):
        pending = total = 0
        for previous,current in zip(sequence,sequence[1:]):
            pending,delta = ns["advance"](previous,current,pending)
            total += delta
        return total
    assert [count(s) for s in ([3,1,0,2,3],[3,2,0,1,3],[3,1,3,1,0,2,3],[3,1,0,3,1])] == [1,-1,1,0]
    out = io.StringIO()
    with redirect_stdout(out):
        try:
            ns["run"]()
        except KeyboardInterrupt:
            pass
    assert out.getvalue().splitlines()==["pos= 0 sw= 1","pos= 1 sw= 1","pos= 0 sw= 1","pos= 0 sw= 0","pos= 0 sw= 1"],out.getvalue()
    assert all(ms == 1 for ms in delays)
finally:
    for mod,value in originals.items():
        if value is None:
            sys.modules.pop(mod,None)
        else:
            sys.modules[mod]=value
print("PASS: syntax, 5 wiring nets, 4 transition sequences, button debounce with tick wrap, 1ms loop delay, README code parity")
