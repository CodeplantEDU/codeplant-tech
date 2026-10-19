"""MPU6050 educational net/geometry/source checks, not hardware execution."""
from pathlib import Path
import copy,json,math,re,xml.etree.ElementTree as ET
p=Path(__file__).parent;d=json.loads((p/'diagram.json').read_text(encoding='utf8'));h=(p/'circuit_preview.html').read_text(encoding='utf8');code=(p/'sketch.ino').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [('uno:5V','mpu:VIN'),('uno:GND.2','mpu:GND'),('uno:A4','mpu:SDA'),('uno:A5','mpu:SCL')]}
def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  group={a,b}
  for g in list(groups):
   if group & g:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}==expected
 assert len(data['parts'])==2 and len(data['connections'])==4
check_nets(d);bad=[]
for a,b in [('mpu:VIN','mpu:GND'),('mpu:SDA','mpu:SCL'),('mpu:3Vo','uno:5V'),('mpu:INT','uno:5V')]:
 v=copy.deepcopy(d);v['connections'].append([a,b,'red',[]]);bad.append(v)
v=copy.deepcopy(d);v['connections'].pop();bad.append(v)
v=copy.deepcopy(d);v['connections'][0][0]='uno:VIN';bad.append(v)
v=copy.deepcopy(d);v['connections'][2][1],v['connections'][3][1]=v['connections'][3][1],v['connections'][2][1];bad.append(v)
for v in bad:
 try:check_nets(v)
 except AssertionError:pass
 else:raise AssertionError('Unsafe/missing/swapped wiring accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'5V':[160,191.5],'GND.2':[169.5,191.5],'A4':[246,191.5],'A5':[255.5,191.5]}
svg=ET.fromstring(re.search(r'<div class="sensor">(.*?)</div>',h,re.S).group(1));parents={c:n for n in svg.iter() for c in n}
assert parts['mpu']['pinIds']=={'VIN':37,'3Vo':38,'GND':39,'SCL':40,'SDA':41,'INT':42,'AD0':31,'FS':32,'SCE':33,'SDE':34,'CLKIN':35,'GND_TOP':36}
for name,i in parts['mpu']['pinIds'].items():
 el=svg.find(f'.//*[@id="connector{i}pin"]');assert el is not None
 x=float(el.attrib['cx']);y=float(el.attrib['cy']);node=el
 while node is not None:
  t=node.attrib.get('transform')
  if t:
   m=re.fullmatch(r'translate\(([-.\d]+)(?:,\s*([-.\d]+))?\)',t);assert m
   x+=float(m[1]);y+=float(m[2] or 0)
  node=parents.get(node)
 assert all(math.isclose(a,b,abs_tol=1e-8) for a,b in zip([x,y],parts['mpu']['pins'][name]))
# This external header has two ancestor translations, not raw circle coordinates.
assert math.isclose(parts['mpu']['pins']['VIN'][0],22.0292613,abs_tol=1e-7)
assert math.isclose(parts['mpu']['pins']['VIN'][1],43.2000008,abs_tol=1e-7)
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return v['left']+x*v['scale'],v['top']+y*v['scale']
def n(x):return f'{x:.6f}'.rstrip('0').rstrip('.')
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];assert f'data-net="{a}"' in h and f'd="{route}"' in h
 start=map(float,re.match(r'M([\d.]+) ([\d.]+)',route).groups());end=[float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])]
 assert all(math.isclose(v,w,abs_tol=1e-6) for v,w in zip(start,xy(a)))
 assert all(math.isclose(v,w,abs_tol=1e-6) for v,w in zip(end,xy(b)))
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{n(x)}" cy="{n(y)}"' in h
assert len(d['insulatedCrossings'])==5
for color,x,y in d['insulatedCrossings']:
 route=f'M{n(x-10)} {y} Q{n(x)} {y-14} {n(x+10)} {y}'
 assert f'd="{route}" fill="none" stroke="white" stroke-width="14"' in h
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for row in ['| 5V | VIN |','| GND (아래쪽 POWER 헤더) | GND |','| A4 / SDA | SDA |','| A5 / SCL | SCL |']:assert row in readme
for s in ['Serial.begin(115200);','const uint8_t ADDRESS = 0x68;','Wire.setWireTimeout(25000, true);','if (!mpu.begin(ADDRESS))','MPU6050_RANGE_2_G','MPU6050_RANGE_250_DEG','MPU6050_BAND_21_HZ','Wire.beginTransmission(ADDRESS);','if (Wire.endTransmission() != 0)','ERROR: I2C_ACK','ERROR: MPU6050_NOT_FOUND','mpu.getEvent(&a, &g, &t);','Serial.print("acc_ms2=");','Serial.print(" gyro_rads=");']:assert s in code,s
assert code.index('if (Wire.endTransmission() != 0)')<code.index('return;')<code.index('mpu.getEvent')
assert [*re.findall(r'a.acceleration.([xyz])',code)]==['x','y','z'] and [*re.findall(r'g.gyro.([xyz])',code)]==['x','y','z']
assert 'getAngle' not in code and 'atan2' not in code
e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert e['slug']=='mpu6050' and len(e['cards'])==7 and not e['review']['hardwareTested']
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5 and e['caption'].count(e['repository'])==1
assert not any(s in e['caption'] for s in ['미시험','미검증','댓글에'])
for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
print('PASS: four independent nets; seven unsafe/missing/swapped wiring mutations rejected; official cumulative SVG transforms, pin centers/endpoints and five bridges; full README-code/table, address/units/order and caption/photos. Not hardware/simulator proof.')
