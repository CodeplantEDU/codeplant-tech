"""python verify.py: pin/net/content checks, not hardware validation."""
import json
import re
from pathlib import Path

p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
e=json.loads((p/'episode.json').read_text(encoding='utf8'))
html=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')
parts={v['id']:v for v in d['parts']}
assert len(parts)==2
assert {(a,b,c) for a,b,c,_ in d['connections']}=={
 ('uno:5V','pot:VCC','red'),('uno:GND.1','pot:GND','black'),('uno:A0','pot:SIG','yellow')}
assert len(d['connections'])==3
assert parts['uno']['pins']=={'GND.1':[115.5,9],'5V':[160,191.5],'A0':[208,191.5]}
assert parts['pot']['pins']=={'GND':[29,68.5],'SIG':[39,68.5],'VCC':[49,68.5]}
for a,b,_,_ in d['connections']:
    route=d['previewRoutes'][a]
    assert f'data-net="{a}"' in html and f'd="{route}"' in html
    for endpoint in (a,b):
        part,pin=endpoint.split(':');v=parts[part]
        x=v['left']+v['pins'][pin][0]*v['scale'];y=v['top']+v['pins'][pin][1]*v['scale']
        assert f'cx="{x:g}" cy="{y:g}"' in html
    numbers=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
    assert float(numbers[0])==parts['uno']['left']+parts['uno']['pins'][a.split(':')[1]][0]*parts['uno']['scale']
    assert float(numbers[1])==parts['uno']['top']+parts['uno']['pins'][a.split(':')[1]][1]*parts['uno']['scale']
    assert float(re.findall(r'H([\d.]+)',route)[-1])==parts['pot']['left']+parts['pot']['pins'][b.split(':')[1]][0]*parts['pot']['scale']
    assert float(re.findall(r'V([\d.]+)',route)[-1])==parts['pot']['top']+parts['pot']['pins'][b.split(':')[1]][1]*parts['pot']['scale']
assert 'const byte POT_PIN = A0;' in code
assert 'const unsigned long PRINT_MS = 100;' in code
assert 'pinMode(POT_PIN, INPUT);' in code and 'pinMode(POT_PIN, INPUT_PULLUP)' not in code
assert 'analogRead(POT_PIN)' in code and 'Serial.println(raw)' in code and 'delay(PRINT_MS)' in code
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
assert '| A0 | 가운데 접점' in readme and '| 위쪽 GND |' in readme
assert e['review']['hardwareTested'] is False
assert e['caption'].count(e['repository'])==1
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
for src in e['documentationImages']+[c['image'] for c in e['cards'] if c.get('image')]+[v['src'] for v in e['cards'][0]['photos']]:
    assert (p/Path(src).name).is_file(),src
print('PASS: 3 nets, official UNO/pot pin coordinates, preview endpoints, A0 INPUT/100ms, README code and caption/photos')
