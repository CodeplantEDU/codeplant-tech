"""Run python verify.py: static electrical/content checks; not hardware or simulation."""
from pathlib import Path
import json,re,copy,math
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
e=json.loads((p/'episode.json').read_text(encoding='utf8'))
html=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')
def check_nets(diagram):
    groups=[]
    for a,b,color,_ in diagram['connections']:
        merge=[g for g in groups if a in g or b in g]
        group={a,b}
        for g in merge:group.update(g);groups.remove(g)
        groups.append(group)
    assert {frozenset(g) for g in groups}=={
        frozenset(['uno:5V','dht:VCC','r1:2']),
        frozenset(['uno:2','dht:SDA','r1:1']),
        frozenset(['uno:GND.1','dht:GND'])},'Power/DATA/GND/NC net error'
    r=next(v for v in diagram['parts'] if v['id']=='r1')
    assert r['attrs']['value']=='10000','Pullup must be 10k ohms'
check_nets(d)
# The checker must reject a short, a grounded DATA line and a wired NC.
for a,b in [('uno:5V','uno:GND.1'),('dht:SDA','dht:GND'),('dht:NC','dht:GND')]:
    bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]])
    try:check_nets(bad)
    except AssertionError:pass
    else:raise AssertionError('Failed to reject unsafe net mutation')
parts={v['id']:v for v in d['parts']}
assert len(parts)==3 and len(d['connections'])==5
expected={'uno':{'2':[236.5,9],'5V':[160,191.5],'GND.1':[115.5,9]},'dht':{'VCC':[15,114.9],'SDA':[24.5,114.9],'NC':[34.1,114.9],'GND':[43.8,114.9]},'r1':{'1':[0,5.65],'2':[58.8,5.65]}}
for part,pins in expected.items():assert parts[part]['pins']==pins

def xy(endpoint):
    part,pin=endpoint.split(':');v=parts[part];x,y=v['pins'][pin];s=v['scale']
    return (v['left']-y*s,v['top']+x*s) if v.get('rotate')==90 else (v['left']+x*s,v['top']+y*s)
for a,b,c,_ in d['connections']:
    assert c==('black' if 'GND' in a else 'red' if a in ['uno:5V','r1:2'] else 'yellow')
    route=d['previewRoutes'][a]
    assert f'data-net="{a}"' in html and f'd="{route}"' in html
    numbers=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
    assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(numbers[:2],xy(a)))
    assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
    for ep in (a,b):
        x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in html
assert 'const byte DHT_PIN = 2;' in code and 'DHT dht(DHT_PIN, DHT22);' in code
assert 'const unsigned long READ_MS = 2500;' in code and code.index('delay(READ_MS)')<code.index('dht.readHumidity()')
fail=re.search(r'if \(isnan\(h\) \|\| isnan\(t\)\) \{(.*?)\}',code,re.S).group(1)
assert 'Serial.println("ERROR: DHT22");' in fail and 'return;' in fail
assert code.index('return;')<code.index('Serial.print("temp_C=")')
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for name in ['readHumidity','readTemperature','Serial.begin(9600)','Serial.print(t, 1)','Serial.println(h, 1)']:assert name in code
assert '| D2 | 2번 DATA |' in readme and '| 위쪽 GND | 4번 GND |' in readme
assert '| 연결하지 않음 | 3번 NC' in readme and 'DATA↔5V' in readme
assert e['review']['hardwareTested'] is False and e['caption'].count(e['repository'])==1
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
assert '1.4.7' in (p/'libraries.txt').read_text() and '1.1.15' in (p/'libraries.txt').read_text()
for src in e['documentationImages']+[c['image'] for c in e['cards'] if c.get('image')]+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file(),src
print('PASS: DHT22 DATA/5V/GND nets; 10k pullup; NC unused; 3 unsafe mutations rejected; official pin/rotated resistor endpoints; 2500ms/error guard; code/README/caption/photos')
