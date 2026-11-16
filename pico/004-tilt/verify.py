from pathlib import Path
import ast, json, runpy, sys
from unittest.mock import Mock, patch
from types import SimpleNamespace
folder = Path(__file__).resolve().parent
code = (folder / 'main.py').read_text(encoding='utf-8')
ast.parse(code)
assert '```python\n' + code.strip() + '\n```' in (folder / 'README.md').read_text(encoding='utf-8')
diagram = json.loads((folder / 'diagram.json').read_text(encoding='utf-8'))
assert [(a, b) for a, b, *_ in diagram['connections']] == [('pico:GP15', 'tilt:1'), ('pico:GND', 'tilt:2')]
pins = {part['id']: part['pins'] for part in diagram['parts']}
svg = (folder / 'circuit_preview.html').read_text(encoding='utf-8')
for start, end, color, points in diagram['connections']:
    for target, coords in [(start, points[0]), (end, points[-1])]:
        part, pin = target.split(':')
        assert pins[part][pin] == coords
        x, y = coords
        assert f'cx="{x}" cy="{y}"' in svg
clock = 1000
values = iter([1] * 13 + [0, 1] + [0] * 16)
def read():
    try:
        return next(values)
    except StopIteration:
        raise KeyboardInterrupt
def sleep(delay):
    global clock
    assert delay == 5
    clock += delay
pin = Mock(IN=0, PULL_UP=1, return_value=SimpleNamespace(value=read))
timer = SimpleNamespace(ticks_ms=lambda: clock % 1024,
                        ticks_diff=lambda a, b: (a - b + 512) % 1024 - 512,
                        sleep_ms=sleep)
reports = []
with patch.dict(sys.modules, machine=SimpleNamespace(Pin=pin), time=timer):
    with patch('builtins.print', side_effect=lambda *args: reports.append((clock, args))):
        runpy.run_path(str(folder / 'main.py'))
pin.assert_called_once_with(15, 0, 1)
assert [entry for entry in reports if entry[1][0] == 'state ='] == [
    (1050, ('state =', 1, 'contact =', 'OPEN')),
    (1120, ('state =', 0, 'contact =', 'CLOSED')),
]
print('PASS: diagram endpoints, README code, pin, tick wrap and bounce timing')
