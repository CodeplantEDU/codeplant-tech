import ast
import json
from math import isfinite
from pathlib import Path
p = Path(__file__).parent
source = (p / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in ("average_raw", "calibrate")]
ns = {"SAMPLES": 10, "isfinite": isfinite}
exec(compile(ast.Module(body=functions, type_ignores=[]), "main.py", "exec"), ns)
class Sensor:
    def __init__(self, values): self.values = iter(values)
    def read(self): return next(self.values)
assert ns["average_raw"](Sensor(range(10))) == 4.5
for raw in (-8388608, 8388607):
    try: ns["average_raw"](Sensor([raw]*10))
    except ValueError: pass
    else: raise AssertionError("ADC saturation accepted")
class Timeout:
    def read(self): raise OSError("Sensor does not respond")
try: ns["average_raw"](Timeout())
except OSError: pass
else: raise AssertionError("Timeout swallowed")
for delta in (10000, -10000):
    scale = ns["calibrate"](200, 200+delta, 100)
    assert (200+delta/2 - 200)/scale == 50
for mass in (0, -1, 5001, float("nan"), float("inf")):
    try: ns["calibrate"](0, 10000, mass)
    except ValueError: pass
    else: raise AssertionError("Invalid mass accepted")
for delta in (0, 50):
    try: ns["calibrate"](100, 100+delta, 100)
    except ValueError: pass
    else: raise AssertionError("Tiny calibration accepted")
assert ns["calibrate"](0, 10000, 5000) == 2
j = json.loads((p / "diagram.json").read_text(encoding="utf-8"))
nets = {(a,b) for a,b,*_ in j["connections"]}
assert nets == {("esp:3V3","hx:VDD"),("supply:+5V","hx:VCC"),("esp:D19","hx:DAT"),("esp:D23","hx:SCK"),("esp:GND.1","hx:GND"),("supply:GND","hx:GND"),("cell:E+","hx:RED"),("cell:E-","hx:BLK"),("cell:S+","hx:GRN"),("cell:S-","hx:WHT")}
assert all("esp:D18" not in pair for pair in nets)
assert source.strip() in (p / "README.md").read_text(encoding="utf-8")
e = json.loads((p / "episode.json").read_text(encoding="utf-8"))
assert len(e["cards"]) == 10
assert e["repository"] in e["caption"]
assert not any(s in e["caption"] for s in ["미시험", "미검증", "댓글에"])
print("PASS: mean, ADC bounds, timeout, signed calibration, invalid mass, tiny delta, 10 nets, README and caption")

# Exercise the complete application with synthetic devices; no hardware claim.
import sys
import types
import runpy
import builtins
import contextlib
import io
pins = {}
cleanup = []
class Pin:
    OUT, IN = 1, 0
    def __init__(self, number, *args, **kwargs): self.number = number; pins[number] = self
    def init(self, *args, **kwargs): cleanup.append((self.number, kwargs.get("value")))
class SPI:
    def __init__(self, number, **kwargs):
        assert number == 2 and kwargs["mosi"].number == 23 and kwargs["miso"].number == 19
        assert kwargs["sck"].number == 18 and kwargs["baudrate"] == 1000000
    def deinit(self): cleanup.append("spi")
class HX711:
    def __init__(self, clock, data, spi, gain):
        assert clock.number == 23 and data.number == 19 and gain == 128
        self.values = iter([200]*10 + [10200]*10 + [5200]*10)
    def read(self):
        try: return next(self.values)
        except StopIteration: raise KeyboardInterrupt
saved = {k: sys.modules.get(k) for k in ("machine", "time", "hx711_spi")}
old_input = builtins.input
try:
    sys.modules["machine"] = types.SimpleNamespace(Pin=Pin, SPI=SPI)
    sys.modules["time"] = types.SimpleNamespace(sleep_ms=lambda x: None)
    sys.modules["hx711_spi"] = types.SimpleNamespace(HX711=HX711)
    app = runpy.run_path(str(p / "main.py"), run_name="synthetic_test")
    answers = iter(["", "100", ""])
    builtins.input = lambda _: next(answers)
    capture = io.StringIO()
    with contextlib.redirect_stdout(capture):
        try: app["run"]()
        except KeyboardInterrupt: pass
    assert "mass_g= 50.0" in capture.getvalue()
    assert cleanup[-2:] == ["spi", (23, 0)]
    answers = iter(["", "nan"])
    try:
        with contextlib.redirect_stdout(io.StringIO()): app["run"]()
    except ValueError as e: assert str(e) == "KNOWN_MASS_G_INVALID"
    else: raise AssertionError("Invalid application input accepted")
    assert cleanup[-2:] == ["spi", (23, 0)]
finally:
    builtins.input = old_input
    for key, value in saved.items():
        if value is None: sys.modules.pop(key, None)
        else: sys.modules[key] = value
print("PASS: full synthetic tare/calibration/display and cleanup on interrupt/invalid input")
