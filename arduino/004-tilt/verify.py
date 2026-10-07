"""Run: python episodes/arduino-004-tilt/verify.py (no hardware needed)."""
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

p = Path(__file__).parent
d = json.loads((p / 'diagram.json').read_text(encoding='utf8'))
readme = (p / 'README.md').read_text(encoding='utf8')
caption = (p / 'caption.md').read_text(encoding='utf8')
code = (p / 'sketch.ino').read_text(encoding='utf8')
parts = {part['id']: part for part in d['parts']}
assert len(parts) == 2 and len(d['connections']) == 2
assert [(a, b, c) for a, b, c, _ in d['connections']] == [
    ('uno:2', 'tilt:1', 'yellow'), ('uno:GND.2', 'tilt:2', 'black')]
html = (p / 'circuit_preview.html').read_text(encoding='utf8')
svg = ET.fromstring(re.search(r'<svg class="sensor".*?</svg>', html, re.S).group())
for pin in ('1', '2'):
    leg = svg.find(f".//*[@id='connector{int(pin)-1}leg']")
    assert parts['tilt']['pins'][pin] == [float(leg.get('x2')), float(leg.get('y2'))]
for a, b, _, points in d['connections']:
    for endpoint, point in ((a, points[0]), (b, points[-1])):
        part_id, pin = endpoint.split(':')
        part = parts[part_id]
        expected = [part['left'] + part['pins'][pin][0] * part['scale'],
                    part['top'] + part['pins'][pin][1] * part['scale']]
        assert all(abs(x-y) < .001 for x, y in zip(point, expected))
    assert ' '.join(f'{x},{y}' for x,y in points) in html
assert re.search(r'TILT_PIN\s*=\s*2', code)
assert 'pinMode(TILT_PIN, INPUT_PULLUP)' in code
assert 'stableState == LOW ? HIGH : LOW' in code
assert '| D2 | 한쪽 다리 |' in readme
assert '| GND | 다른 다리 |' in readme
assert caption.count('https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/004-tilt') == 1
assert (p / 'sketch.ino').is_file()
print('PASS: two-pin contact net, source SVG pin endpoints, preview routes, D2 code/table, caption URL')
