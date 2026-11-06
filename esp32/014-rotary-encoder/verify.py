import ast
import json
from pathlib import Path

root = Path(__file__).parent
source = (root / "main.py").read_text(encoding="utf-8")
tree = ast.parse(source)
nodes = [node for node in tree.body if (
    isinstance(node, ast.FunctionDef) and node.name == "advance"
) or (
    isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name)
    and node.targets[0].id == "STEP"
)]
ns = {}
exec(compile(ast.Module(body=nodes, type_ignores=[]), "main.py", "exec"), ns)

def count(states):
    pending = total = 0
    for previous, current in zip(states, states[1:]):
        pending, delta = ns["advance"](previous, current, pending)
        total += delta
    return total

assert count([3, 1, 0, 2, 3]) == 1
assert count([3, 2, 0, 1, 3]) == -1
assert count([3, 1, 3, 1, 0, 2, 3]) == 1
assert count([3, 1, 0, 3, 1]) == 0
assert all(f"{name} = Pin({pin}, Pin.IN, Pin.PULL_UP)" in source
           for name, pin in [("CLK", 18), ("DT", 19), ("SW", 21)])
diagram = json.loads((root / "diagram.json").read_text(encoding="utf-8"))
assert {(a, b) for a, b, *_ in diagram["connections"]} == {
    ("esp:D18", "enc:CLK"), ("esp:D19", "enc:DT"), ("esp:D21", "enc:SW"),
    ("esp:3V3", "enc:VCC"), ("esp:GND.1", "enc:GND"),
}
print("PASS: syntax, four A/B sequences, input pull-ups, five nets")
