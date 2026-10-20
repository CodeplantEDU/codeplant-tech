"""Dedicated physical-net/geometry and source-consistency checks, not a hardware test."""
from pathlib import Path
import copy,json,math,re,xml.etree.ElementTree as ET
p=Path(__file__).parent;d=json.loads((p/'diagram.json').read_text(encoding='utf8'));h=(p/'circuit_preview.html').read_text(encoding='utf8');code=(p/'sketch.ino').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [('uno:5V','tof:VIN'),('uno:GND.2','tof:GND'),('uno:A4','tof:SDA'),('uno:A5','tof:SCL')]}
def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  g={a,b}
  for old in list(groups):
   if g & old:g.update(old);groups.remove(old)
  groups.append(g)
 assert {frozenset(x) for x in groups}==expected
 assert len(data['connections'])==4 and len(data['parts'])==2
check_nets(d);bad=[]
for a,b in [('tof:VIN','tof:GND'),('tof:SDA','tof:SCL'),('tof:GPIO','uno:5V'),('tof:XSHUT','uno:5V')]:
 v=copy.deepcopy(d);v['connections'].append([a,b,'red',[]]);bad.append(v)
v=copy.deepcopy(d);v['connections'].pop();bad.append(v)
v=copy.deepcopy(d);v['connections'][0][0]='uno:VIN';bad.append(v)
v=copy.deepcopy(d);v['connections'][2][1],v['connections'][3][1]=v['connections'][3][1],v['connections'][2][1];bad.append(v)
for v in bad:
 try:check_nets(v)
 except AssertionError:pass
 else:raise AssertionError('Wrong/missing/shorted wiring accepted')
parts={x['id']:x for x in d['parts']};assert parts['uno']['pins']=={'5V':[160,191.5],'GND.2':[169.5,191.5],'A4':[246,191.5],'A5':[255.5,191.5]}
assert parts['tof']['pinIds']=={'VIN':29,'GND':30,'SCL':31,'SDA':32,'GPIO':33,'XSHUT':34}
svg=ET.fromstring(re.search(r'<div class="sensor">(.*?)</div>',h,re.S).group(1));parents={c:n for n in svg.iter() for c in n}
for name,i in parts['tof']['pinIds'].items():
 el=svg.find(f'.//*[@id="connector{i}pin"]');assert [float(el.attrib['cx']),float(el.attrib['cy'])]==parts['tof']['pins'][name]
 node=el
 while node is not None:
  assert not node.attrib.get('transform');node=parents.get(node)
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return v['left']+x*v['scale'],v['top']+y*v['scale']
def n(x):return f'{x:.6f}'.rstrip('0').rstrip('.')
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];assert f'data-net="{a}"' in h and f'd="{route}"' in h
 start=map(float,re.match(r'M([\d.]+) ([\d.]+)',route).groups());end=[float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])]
 for given,desired in [(start,xy(a)),(end,xy(b))]:assert all(math.isclose(x,y,abs_tol=1e-6) for x,y in zip(given,desired))
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{n(x)}" cy="{n(y)}"' in h
assert len(d['insulatedCrossings'])==5
for color,x,y in d['insulatedCrossings']:
 path=f'M{n(x-10)} {y} Q{n(x)} {y-14} {n(x+10)} {y}'
 assert f'd="{path}" fill="none" stroke="white" stroke-width="14"' in h
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for s in ['const uint8_t ADDRESS = 0x29;','Serial.begin(115200);','Wire.setWireTimeout(25000, true);','!lox.begin(ADDRESS, false, &Wire)','Wire.clearWireTimeoutFlag();','VL53L0X_Error error = lox.rangingTest(&measure, false);','if (Wire.getWireTimeoutFlag())','else if (error != VL53L0X_ERROR_NONE)','else if (measure.RangeStatus != 0)','RANGE_INVALID status=','measure.RangeMilliMeter / 10.0f','delay(250);']:assert s in code,s
# Only the final else may print distance: timeout/API/status errors must win first.
valid=code[code.index('  } else {\n    Serial.print(F("distance_mm="))'):]
assert 'distance_cm=' in valid and 'RangeMilliMeter' in valid
prefix=code[:code.index('  } else {\n    Serial.print(F("distance_mm="))')]
assert 'distance_mm=' not in prefix
assert prefix.index('if (Wire.getWireTimeoutFlag())')<prefix.index('else if (error !=')<prefix.index('else if (measure.RangeStatus !=')
assert 'measure.RangeStatus != 4' not in code
# Independent unit examples, not sensor readings.
assert 100/10==10 and 200/10==20 and 300/10==30
for row in ['| 5V | VIN |','| A4 / SDA | SDA |','| A5 / SCL | SCL |']:assert row in readme
assert 'not runnable Wokwi simulation' in d['note']
e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert e['id']=='arduino-017-vl53l0x' and len(e['cards'])==7 and not e['review']['hardwareTested']
assert e['caption']==(p/'caption.md').read_text(encoding='utf8') and e['caption'].count(e['repository'])==1
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5 and not any(x in e['caption'] for x in ['미시험','미검증','댓글에'])
for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
print('PASS: four independent nets; seven bad wiring mutations rejected; official six pin geometry/endpoints and five insulated bridges; full code/README/table; timeout/API/status precedence and mm/cm units; 7 cards/caption/photo sources. No hardware/simulator proof.')
