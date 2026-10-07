"""Run inside this lesson: python verify.py. No hardware is required."""
import json
import re
from pathlib import Path

p = Path(__file__).parent
for name, signal, board_pin, color, unused in [
    ('diagram.json', 'AO', 'A0', 'yellow', 'DO'),
    ('diagram-do.json', 'DO', '2', 'blue', 'AO'),
]:
    d = json.loads((p / name).read_text(encoding='utf8'))
    assert len(d['connections']) == 3
    assert {(a, b, c) for a, b, c, route in d['connections']} == {
        ('uno:5V', 'cds:VCC', 'red'), ('uno:GND.2', 'cds:GND', 'black'),
        (f'uno:{board_pin}', f'cds:{signal}', color)}
    assert not any(f'cds:{unused}' in pair[:2] for pair in d['connections'])
code = (p / 'sketch-do.ino').read_text(encoding='utf8')
assert re.search(r'CDS_DO_PIN\s*=\s*2', code)
assert 'pinMode(CDS_DO_PIN, INPUT)' in code
assert 'digitalRead(CDS_DO_PIN)' in code
assert 'state == LIGHT_DETECTED ? HIGH : LOW' in code
assert 'Serial.begin(9600)' in code
preview = (p / 'circuit_preview_do.html').read_text(encoding='utf8')
# Official pin coordinates: UNO D2=(236.5,9), LDR DO=(172,35.8).
assert (180 + 236.5 * 1.2, 145 + 9 * 1.2) == (463.8, 155.8)
assert (907.5 - 172 * 1.25, 321.875 - 35.8 * 1.25) == (692.5, 277.125)
assert 'M463.8 155.8 V115 H600 V277.125 H692.5' in preview
assert 'AO 미사용' in preview and 'DO 미사용' not in preview
assert (p / 'README.md').read_text(encoding='utf8').count('CDS_DO_PIN = 2') >= 1
print('PASS: distinct AO/DO nets, unused pins, D2 code, official pin endpoints, README code')
