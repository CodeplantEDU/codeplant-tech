import ast
import json
from pathlib import Path

root = Path(__file__).parent
code = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(code)
assert code.strip() in (root / "README.md").read_text(encoding="utf-8")
assert "ADC(Pin(26))" in code
read_average = next(node for node in tree.body if isinstance(node, ast.FunctionDef))
samples = iter(range(8))
from types import SimpleNamespace
runtime = {"adc": SimpleNamespace(read_u16=lambda: next(samples))}
exec(compile(ast.Module(body=[read_average], type_ignores=[]), "<average>", "exec"), runtime)
assert runtime["read_average"]() == 3
diagram = json.loads((root / "diagram.json").read_text(encoding="utf-8"))
assert diagram["connections"] == [["Pico 36 · 3V3(OUT)", "VCC"], ["Pico 33 · AGND", "GND"], ["Pico 31 · GP26", "AO"]]
assert diagram["unconnected"] == ["DO"]
print("PASS: syntax, README code, synthetic eight-sample average and three connections")
