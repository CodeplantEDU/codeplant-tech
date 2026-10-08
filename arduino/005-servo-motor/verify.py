"""Run in this lesson: python verify.py. Wiring/content checks, no hardware."""
import json
import re
from pathlib import Path

p = Path(__file__).parent
d = json.loads((p / 'diagram.json').read_text(encoding='utf8'))
episode = json.loads((p / 'episode.json').read_text(encoding='utf8'))
code = (p / 'sketch.ino').read_text(encoding='utf8')
readme = (p / 'README.md').read_text(encoding='utf8')
preview = (p / 'circuit_preview.html').read_text(encoding='utf8')
assert {(a, b, color) for a, b, color, _ in d['connections']} == {
    ('ext5v:VCC', 'servo1:V+', 'red'),
    ('extgnd:GND', 'servo1:GND', 'black'),
    ('uno:GND.2', 'servo1:GND', 'black'),
    ('servo1:PWM', 'uno:9', 'yellow')}
assert len(d['connections']) == 4
assert not any(pin in c[:2] for pin in ('uno:5V', 'uno:3.3V', 'uno:VIN') for c in d['connections'])
# Official local coordinates, transformed by the preview's left/top/scale.
assert abs(355 + 163 * 1.15 - 542.45) < .001  # UNO D9
assert abs(145 + 9 * 1.15 - 155.35) < .001
assert abs(355 + 169.5 * 1.15 - 549.925) < .001  # UNO GND.2
assert abs(145 + 191.5 * 1.15 - 365.225) < .001
for local_y, final_y in ((50, 507.5), (59.5, 522.225), (69, 536.95)):
    assert abs(430 + local_y * 1.55 - final_y) < .001
assert 'M285 502 V560 H800 V522.225 H885' in preview
assert 'M285 448 H760 V507.5 H885' in preview
assert 'M549.925 365.225 V448 H760' in preview
assert 'M542.45 155.35 V138 H840 V405 H1180 V620 H840 V536.95 H885' in preview
assert re.search(r'SERVO_PIN\s*=\s*9;', code)
assert re.search(r'MIN_PULSE_US\s*=\s*1000;', code)
assert re.search(r'MAX_PULSE_US\s*=\s*2000;', code)
assert 'servoMotor.attach(SERVO_PIN, MIN_PULSE_US, MAX_PULSE_US)' in code
assert 'servoMotor.write(commandAngle)' in code and 'delay(HOLD_MS)' in code
assert 'Serial.begin(9600)' in code
loop = re.search(r'void loop\(\)\s*\{([^}]+)\}', code).group(1)
assert re.findall(r'moveToAngle\((\d+)\)', loop) == ['60', '90', '120']
assert re.search(r'void setup\(\).*?moveToAngle\(90\)', code, re.S)
assert re.search(r'```cpp\n(.*?)\n```', readme, re.S).group(1).strip() == code.strip()
assert '| 신호(주황/노랑) | UNO D9 |' in readme
assert '| 접지(갈색/검정) | 외부 − · UNO GND |' in readme
assert episode['caption'].count(episode['repository']) == 1
assert len(re.findall(r'(?<!\S)#[^\s#]+', episode['caption'])) == 5
assert episode['review']['hardwareTested'] is False
for src in episode['documentationImages'] + [v['src'] for v in episode['cards'][0]['photos']]:
    assert (p / Path(src).name).is_file()
print('PASS: external 5V/common GND/D9 nets, official pin endpoints, 60/90/120 commands, README code, caption/photos')
