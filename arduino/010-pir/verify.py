"""Static PIR wiring/content checks; not hardware or simulation."""
from pathlib import Path
import json,re,copy,math
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
code=(p/'sketch.ino').read_text(encoding='utf8');html=(p/'circuit_preview.html').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  merge=[g for g in groups if a in g or b in g];group={a,b}
  for g in merge:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}=={frozenset(['uno:5V','pir:VCC']),frozenset(['uno:GND.1','pir:GND']),frozenset(['uno:2','pir:OUT'])}
check_nets(d)
for a,b in [('uno:5V','uno:GND.1'),('pir:OUT','pir:VCC'),('pir:OUT','pir:GND')]:
 bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]])
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('unsafe net accepted')
parts={v['id']:v for v in d['parts']}
assert len(parts)==2 and len(d['connections'])==3
assert parts['uno']['pins']=={'2':[236.5,9],'5V':[160,191.5],'GND.1':[115.5,9]}
assert parts['pir']['pins']=={'VCC':[36.178,92],'OUT':[45.9175,92],'GND':[55.6415,92]}
def xy(ep):
 part,pin=ep.split(':');v=parts[part];return tuple(v[k]+v['pins'][pin][i]*v['scale'] for i,k in enumerate(['left','top']))
for a,b,color,_ in d['connections']:
 route=d['previewRoutes'][a];assert f'data-net="{a}"' in html and f'd="{route}"' in html
 vals=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
 assert all(math.isclose(float(n),x,abs_tol=1e-6) for n,x in zip(vals[:2],xy(a)))
 assert all(math.isclose(n,x,abs_tol=1e-6) for n,x in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
 assert color==('red' if a=='uno:5V' else 'black' if a=='uno:GND.1' else 'yellow')
for line in ['const byte PIR_PIN = 2;','const unsigned long WARMUP_MS = 60000UL;','int lastMotion = -1;','pinMode(PIR_PIN, INPUT);','pinMode(LED_BUILTIN, OUTPUT);','digitalWrite(LED_BUILTIN, LOW);','Serial.begin(9600);','delay(WARMUP_MS);','int motion = digitalRead(PIR_PIN);','digitalWrite(LED_BUILTIN, motion);','if (motion != lastMotion)','lastMotion = motion;','delay(50);']:assert line in code,line
assert 'INPUT_PULLUP' not in code
assert code.index('WAIT_60S')<code.index('delay(WARMUP_MS)')<code.index('READY')<code.index('digitalRead')
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S)[1].strip()==code.strip()
assert '| D2 (INPUT) | OUT / DO |' in readme
if (p/'episode.json').exists():
 e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert e['review']['hardwareTested'] is False
 assert 'DM으로' not in e['caption'] and e['caption'].count(e['repository'])==1
 assert not any('git을 남기면' in str(c) for c in e['cards'])
 for src in e['documentationImages']+[c['image'] for c in e['cards'] if c.get('image')]+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file(),src
print('PASS: 3 isolated PIR nets; 3 unsafe mutations rejected; official pin endpoints; INPUT/60s/LED/state-change; full code README; direct caption; no hardware proof')
