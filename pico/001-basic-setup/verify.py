from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import contextlib
import io
import sys

base = Path(__file__).parent
code = (base / "main.py").read_text(encoding="utf-8")
assert code.strip() in (base / "README.md").read_text(encoding="utf-8")
events = []

class Pin:
    OUT = 1

    def __init__(self, pin, mode, value):
        assert (pin, mode, value) == ("LED", self.OUT, 0)

    def on(self):
        events.append("on")

    def off(self):
        events.append("off")

output = io.StringIO()
with patch.dict(sys.modules, {"machine": SimpleNamespace(Pin=Pin), "time": SimpleNamespace(sleep_ms=events.append)}):
    with contextlib.redirect_stdout(output):
        exec(compile(code, str(base / "main.py"), "exec"), {})
assert events == ["on", 500, "off", 500] * 3
assert output.getvalue().splitlines() == ["Pico ready", "Done"]
print("PASS: three synthetic LED cycles, Shell output, README code")
