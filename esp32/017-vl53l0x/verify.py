import ast
import json
from pathlib import Path

root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "sample")
ns = {"MIN_MM": 50, "MAX_MM": 1000}
exec(compile(ast.Module(body=[fn], type_ignores=[]), "main.py", "exec"), ns)

class Sensor:
    def __init__(self, value):
        self.range = value

for x in [50, 300, 1000]:
    assert ns["sample"](Sensor(x)) == x
for x in [0, 49, 1001, 8190]:
    assert ns["sample"](Sensor(x)) is None

class Timeout:
    @property
    def range(self):
        raise RuntimeError("Timeout")

try:
    ns["sample"](Timeout())
except RuntimeError:
    pass
else:
    raise AssertionError("Timeout swallowed")
nets = json.loads((root / "diagram.json").read_text(encoding="utf-8"))["connections"]
assert {(a,b) for a,b,*_ in nets} == {
    ("esp:3V3","tof:VIN"), ("esp:GND.1","tof:GND"),
    ("esp:D21","tof:SDA"), ("esp:D22","tof:SCL")}
assert source.strip() in (root / "README.md").read_text(encoding="utf-8")
print("PASS: seven boundary inputs, timeout, four nets, README")
