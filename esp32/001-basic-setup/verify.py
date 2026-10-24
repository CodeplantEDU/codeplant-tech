import ast, contextlib, io, json, pathlib, runpy, time
from unittest.mock import patch
p = pathlib.Path(__file__).resolve().parent
source = (p / "main.py").read_text(encoding="utf8")
ast.parse(source)
expected = ["ESP32_READY"] + ["count = " + str(n) for n in range(1, 6)] + ["DONE"]
out = io.StringIO()
with patch.object(time, "sleep") as wait, contextlib.redirect_stdout(out):
    runpy.run_path(str(p / "main.py"), run_name="__main__")
assert out.getvalue().splitlines() == expected
assert wait.call_count == 5 and all(c.args == (1,) for c in wait.call_args_list)
assert "```python\n" + source.rstrip() + "\n```" in (p / "README.md").read_text(encoding="utf8")
wiring = json.loads((p / "diagram.json").read_text(encoding="utf8"))
assert wiring["externalGPIOConnections"] == []
assert wiring["connections"][0]["to"] == "board Micro-USB"
assert wiring["connections"][0]["purpose"] == ["power", "serial data"]
assert wiring["simulationExecutable"] is False
print("PASS: host syntax/output/sleep arguments, README code, USB-only metadata; no board test")
