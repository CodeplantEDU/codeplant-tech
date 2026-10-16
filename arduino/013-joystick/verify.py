"""Joystick five-net/coordinate/code consistency checks; no hardware execution."""
from pathlib import Path
import copy,json,math,re
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
h=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')

def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  group={a,b}
  for g in list(groups):
   if group & g:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}=={frozenset(pair) for pair in [('uno:5V','joy:VCC'),('uno:GND.1','joy:GND'),('uno:A0','joy:HORZ'),('uno:A1','joy:VERT'),('uno:2','joy:SEL')]}
 assert len(data['parts'])==2 and len(data['connections'])==5
check_nets(d)
invalid=[]
for a,b in [('uno:5V','uno:GND.1'),('joy:SEL','joy:VCC'),('joy:HORZ','joy:VERT')]:
 bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]]);invalid.append(bad)
bad=copy.deepcopy(d);bad['connections'].pop();invalid.append(bad)
bad=copy.deepcopy(d);bad['connections'][1][1]='joy:HORZ';invalid.append(bad)
for bad in invalid:
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('Unsafe/missing/swapped wiring accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'2':[236.5,9],'5V':[160,191.5],'GND.1':[115.5,9],'A0':[208,191.5],'A1':[217.5,191.5]}
assert parts['joy']['pins']=={'VCC':[33,115.8],'VERT':[42.6012,115.8],'HORZ':[52.2024,115.8],'SEL':[61.8036,115.8],'GND':[71.4048,115.8]}
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return v['left']+x*v['scale'],v['top']+y*v['scale']
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];nums=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
 assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(nums[:2],xy(a)))
 assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
 assert f'data-net="{a}"' in h and f'd="{route}"' in h
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in h
for bridge in ['Q382 564 387 580','Q396.25 564 401.25 580','Q957.09056 676 937.09056 700']:assert h.count(bridge)>=2
assert 'stroke="white" stroke-width="12"' in h and 'stroke="white" stroke-width="14"' in h
for value in ['const byte X_PIN = A0;','const byte Y_PIN = A1;','const byte SW_PIN = 2;','pinMode(SW_PIN, INPUT_PULLUP);','analogReference(DEFAULT);','analogRead(X_PIN)','analogRead(Y_PIN)','digitalRead(SW_PIN)','Serial.begin(9600);','delay(100);']:
 assert value in code
assert 'analogReference(EXTERNAL)' not in code and 'digitalWrite(SW_PIN' not in code
assert code.index('Serial.print("x=");')<code.index('Serial.print(x);')<code.index('Serial.print(" y=");')<code.index('Serial.print(y);')<code.index('Serial.print(" sw=");')<code.index('Serial.println(sw);')
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for row in ['| A0 | VRX | HORZ |','| A1 | VRY | VERT |','| D2 | SW | SEL |']:assert row in readme
if (p/'episode.json').is_file():
 e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert e['slug']=='joystick' and e['category']=='other-sensors' and not e['review']['hardwareTested']
 assert e['caption'].count(e['repository'])==1 and not re.search(r'\bDM\b',e['caption'])
 assert not any(v in e['caption'] for v in ['미시험','미검증','시험하지','댓글에'])
 assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
 for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
 assert e['cards'][4]['code']=='int x = analogRead(A0);\nint y = analogRead(A1);\nint sw = digitalRead(2);'
print('PASS: five independent nets; five unsafe/missing/swapped connections rejected; official pin endpoints; three insulated crossings; A0/A1/D2 INPUT_PULLUP/DEFAULT; Serial field order; README code/physical-Wokwi mapping; caption/photos')
