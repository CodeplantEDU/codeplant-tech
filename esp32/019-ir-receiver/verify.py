import ast
import contextlib
import io
import json
from pathlib import Path

p = Path(__file__).parent
source = (p / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
functions = [n for n in tree.body if isinstance(n, ast.FunctionDef)]
namespace = {}
exec(compile(ast.Module(body=functions, type_ignores=[]), "main.py", "exec"), namespace)
out = io.StringIO()
with contextlib.redirect_stdout(out):
    namespace["on_receive"](0, 255, 0)
    namespace["on_receive"](-1, 255, 0)
    namespace["on_error"](-3)
assert out.getvalue().splitlines() == ["ADDR=FF CMD=00", "REPEAT", "RX_ERROR -3"]
diagram = json.loads((p / "diagram.json").read_text(encoding="utf-8"))
assert {(a,b) for a,b,*_ in diagram["connections"]} == {
    ("esp:D18","ir:OUT"), ("esp:GND.1","ir:GND"), ("esp:3V3","ir:VS")
}
html = (p / "circuit_preview.html").read_text(encoding="utf-8")
for part in diagram["parts"]:
    for name, (x,y) in part["pins"].items():
        px = round(part["left"] + part["scale"] * x, 2)
        py = round(part["top"] + part["scale"] * y, 2)
        assert f'data-pin="{part["id"]}:{name}" d="M{px:g} {py:g}l' in html
assert "NEC_8(Pin(18, Pin.IN), on_receive)" in source
assert source.strip() in (p / "README.md").read_text(encoding="utf-8")
print("PASS: normal/repeat/error output, three wiring nets, six anchors, README code match")

