"""KY040 nets, coordinates, source consistency and pure state-model checks. Not hardware."""
from pathlib import Path
import copy,json,math,re
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'));h=(p/'circuit_preview.html').read_text(encoding='utf8');code=(p/'sketch.ino').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  group={a,b}
  for g in list(groups):
   if group & g:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}=={frozenset(pair) for pair in [('uno:5V','enc:VCC'),('uno:GND.1','enc:GND'),('uno:2','enc:CLK'),('uno:3','enc:DT'),('uno:4','enc:SW')]}
 assert len(data['parts'])==2 and len(data['connections'])==5
check_nets(d)
invalid=[]
for a,b in [('uno:5V','uno:GND.1'),('enc:SW','enc:VCC'),('enc:CLK','enc:DT')]:
 bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]]);invalid.append(bad)
bad=copy.deepcopy(d);bad['connections'].pop();invalid.append(bad)
bad=copy.deepcopy(d);bad['connections'][1][1]='enc:CLK';invalid.append(bad)
for bad in invalid:
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('Unsafe/missing/swapped wiring accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'2':[236.5,9],'3':[227,9],'4':[217.5,9],'5V':[160,191.5],'GND.1':[115.5,9]}
assert parts['enc']['pins']=={'CLK':[116,7.9],'DT':[116,17.4],'SW':[116,27],'VCC':[116,36.3],'GND':[116,45.5]}
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return v['left']+x*v['scale'],v['top']+y*v['scale']
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];nums=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
 assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(nums[:2],xy(a)))
 assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
 assert f'data-net="{a}"' in h and f'd="{route}"' in h
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in h
assert h.count('Q1065 371 1050 361')==3 and 'stroke="white" stroke-width="14"' in h
for value in ['#include <RotaryEncoder.h>','const byte CLK_PIN = 2;','const byte DT_PIN = 3;','const byte SW_PIN = 4;','const unsigned long DEBOUNCE_MS = 50;','RotaryEncoder encoder(CLK_PIN, DT_PIN, RotaryEncoder::LatchMode::FOUR3);','pinMode(CLK_PIN, INPUT_PULLUP);','pinMode(DT_PIN, INPUT_PULLUP);','pinMode(SW_PIN, INPUT_PULLUP);','encoder.tick();','long position = encoder.getPosition();','Serial.begin(115200);']:
 assert value in code,value
assert 'delay(' not in code and 'attachInterrupt' not in code and 'encoder.setPosition' not in code
assert code.index('if (rawSW != lastRawSW)')<code.index('changedAt = now;')<code.index('if (rawSW != stableSW && now - changedAt >= DEBOUNCE_MS)')<code.index('stableSW = rawSW;')
assert 'digitalWrite(LED_BUILTIN, stableSW == LOW ? HIGH : LOW);' in code and 'if (position != lastPosition || swChanged)' in code
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
assert (p/'libraries.txt').read_text(encoding='utf8').splitlines()[0]=='RotaryEncoder@1.6.0 by Matthias Hertel'
for row in ['| D2 | CLK |','| D3 | DT |','| D4 | SW |']:assert row in readme
# Independent input models of official 1.6.0 KNOBDIR/FOUR3 and the sketch's unsigned debounce.
def count(sequence):
 table=[0,-1,1,0,1,0,0,-1,-1,0,0,1,0,1,-1,0];old=3;raw=0;pos=0
 for state in sequence:
  if old!=state:
   raw+=table[state|(old<<2)];old=state
   if state==3:pos=raw>>2
 return pos
assert count([1,0,2,3])==1 and count([2,0,1,3])==-1
assert count([1,3,1,0,2,0,2,3])==1
assert count([1,3,1,3])==0 and count([1,0,2,3,2,0,1,3])==0
assert count([1,0,2,3]*10)==10 and count([2,0,1,3]*10)==-10

def debounce(samples,initial_raw=1,start=0):
 last=initial_raw;stable=1;changed=start;events=[]
 for now,raw in samples:
  if raw!=last:last=raw;changed=now
  if raw!=stable and ((now-changed)&0xffffffff)>=50:stable=raw;events.append((now,stable))
 return stable,events
assert debounce([(0,1),(1,0),(5,1),(9,0),(58,0),(59,0)])==(0,[(59,0)])
assert debounce([(1,0),(50,0),(51,1),(101,1)])==(1,[])
assert debounce([(0,0),(49,0),(50,0),(80,1),(129,1),(130,1)],0)==(1,[(50,0),(130,1)])
assert debounce([(0xfffffff0,0),(0x21,0),(0x22,0)],1,0xffffffef)==(0,[(0x22,0)])
assert debounce([(0,1),(1,0),(51,0),(52,0),(100,0),(200,0)])==(0,[(51,0)])
if (p/'episode.json').is_file():
 e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert e['slug']=='rotary-encoder' and e['category']=='other-sensors' and not e['review']['hardwareTested']
 assert e['caption'].count(e['repository'])==1 and not re.search(r'\bDM\b',e['caption'])
 assert not any(v in e['caption'] for v in ['미시험','미검증','시험하지','댓글에'])
 assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
 for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
print('PASS: 5 nets / 5 unsafe-missing-swapped mutations; official endpoints/bridge; D2 D3 D4 pullups/FOUR3/no delay; README-code; model +/- cycles/bounce reversal; SW 49/50ms/hold/release/start-held/32-bit wrap; caption/photos. Models are not hardware or simulator execution.')
