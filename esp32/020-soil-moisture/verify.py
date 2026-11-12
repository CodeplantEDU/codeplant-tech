import ast
import json
from pathlib import Path

base = Path(__file__).parent
program = (base / "main.py").read_text(encoding="utf-8")
ast.parse(program)
assert "ADC(Pin(34), atten=ADC.ATTN_11DB)" in program
assert "sensor.read_u16()" in program
assert program.strip() in (base / "README.md").read_text(encoding="utf-8")
diagram = json.loads((base / "diagram.json").read_text(encoding="utf-8"))
assert diagram["connections"] == [
    ["esp32:D34", "soil:Signal"],
    ["esp32:3V3", "soil:VCC"],
    ["esp32:GND.1", "soil:GND"],
]
preview = (base / "circuit_preview.html").read_text(encoding="utf-8")
for x, y in diagram["pins"].values():
    assert f'cx="{x}" cy="{y}"' in preview
print("PASS: MicroPython syntax, README code, nets and preview anchors")

