import ast
import json
import struct
from pathlib import Path
root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "decode"]
ns = {"unpack": struct.unpack, "ACCEL_SCALE": 16384.0, "GYRO_SCALE": 131.0}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "main.py", "exec"), ns)
a, g = ns["decode"](struct.pack(">7h", 16384, -16384, 0, 0, 131, -131, 0))
assert a == (1, -1, 0) and g == (1, -1, 0)
a, g = ns["decode"](struct.pack(">7h", -32768, 32767, 0, 0, -32768, 32767, 0))
assert a[0] == -2 and a[1] < 2 and g[0] < -250
try:
    ns["decode"](b"")
except ValueError:
    pass
else:
    raise AssertionError("Truncated data accepted")
nets = json.loads((root / "diagram.json").read_text(encoding="utf-8"))["connections"]
assert {(a,b) for a,b,*_ in nets} == {
    ("esp:3V3","mpu:VCC"), ("esp:GND.1","mpu:GND"),
    ("esp:D21","mpu:SDA"), ("esp:D22","mpu:SCL"), ("mpu:AD0","mpu:GND")}
assert source.strip() in (root / "README.md").read_text(encoding="utf-8")
print("PASS: signed decode, scale, truncated read, five connections, README")
