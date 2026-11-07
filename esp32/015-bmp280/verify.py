import ast
import json
from pathlib import Path

root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
fn = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "compensate")
ns = {}
exec(compile(ast.Module(body=[fn], type_ignores=[]), "main.py", "exec"), ns)
trim = (27504, 26435, -1000, 36477, -10685, 3024, 2855, 140, -7, 15500, -14600, 6000)
t, p = ns["compensate"](519888, 415148, trim)
assert abs(t - 25.08) < .02 and abs(p - 1006.53) < .02, (t, p)
try:
    ns["compensate"](519888, 415148, trim[:3] + (0,) + trim[4:])
except ValueError:
    pass
else:
    raise AssertionError("Invalid gain accepted")
diagram = json.loads((root / "diagram.json").read_text(encoding="utf-8"))
assert {(a, b) for a, b, *_ in diagram["connections"]} == {
    ("esp:3V3", "bmp:VIN"), ("esp:GND.1", "bmp:GND"),
    ("esp:D21", "bmp:SDI"), ("esp:D22", "bmp:SCK"),
}
assert "sda=Pin(21), scl=Pin(22)" in source
assert source.strip() in (root / "README.md").read_text(encoding="utf-8")
print("PASS: compensation vector, zero gain, four nets, README code")
