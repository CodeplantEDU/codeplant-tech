import ast
import json
from pathlib import Path

root = Path(__file__).parent
code = (root / "main.py").read_text(encoding="utf-8")
ast.parse(code)
assert code.strip() in (root / "README.md").read_text(encoding="utf-8")
assert 'ADC(Pin(26))' in code and 'PWM(Pin("LED"), freq=1000, duty_u16=0)' in code
assert 'led.duty_u16(raw)' in code and 'led.deinit()' in code
assert json.loads((root / "diagram.json").read_text(encoding="utf-8"))["connections"] == [
    ["pico:36 3V3(OUT)", "pot:outer1"],
    ["pico:31 GP26", "pot:wiper"],
    ["pico:33 AGND", "pot:outer2"],
]
print("PASS: syntax, README, ADC/PWM mapping and three wiring connections")
