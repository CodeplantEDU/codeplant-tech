"""Educational geometry/net/source checks; no hardware or simulator execution."""
from pathlib import Path
import copy,json,math,re,xml.etree.ElementTree as ET
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
h=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [('uno:5V','bmp:VIN'),('uno:GND.2','bmp:GND'),('uno:A4','bmp:SDI'),('uno:A5','bmp:SCK')]}
def check_nets(data):
 groups=[]
 for a,b,_,_ in data['connections']:
  group={a,b}
  for g in list(groups):
   if group & g:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}==expected
 assert len(data['parts'])==2 and len(data['connections'])==4
check_nets(d)
bad=[]
for a,b in [('bmp:VIN','bmp:GND'),('bmp:SDI','bmp:SCK'),('bmp:3Vo','uno:5V'),('bmp:CS','uno:GND.2')]:
 v=copy.deepcopy(d);v['connections'].append([a,b,'black',[]]);bad.append(v)
v=copy.deepcopy(d);v['connections'].pop();bad.append(v)
v=copy.deepcopy(d);v['connections'][0][0]='uno:VIN';bad.append(v)
v=copy.deepcopy(d);v['connections'][2][1],v['connections'][3][1]=v['connections'][3][1],v['connections'][2][1];bad.append(v)
for v in bad:
 try:check_nets(v)
 except AssertionError:pass
 else:raise AssertionError('Unsafe/missing/swapped net accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'5V':[160,191.5],'GND.2':[169.5,191.5],'A4':[246,191.5],'A5':[255.5,191.5]}
sensor_svg=re.search(r'<div class="sensor">(.*?)</div>',h,re.S).group(1)
svg=ET.fromstring(sensor_svg)
for name,n in {'VIN':29,'3Vo':30,'GND':31,'SCK':32,'SDO':33,'SDI':34,'CS':35}.items():
 el=svg.find(f'.//*[@id="connector{n}pin"]');assert el is not None
 assert parts['bmp']['pins'][name]==[float(el.attrib['cx']),float(el.attrib['cy'])]
assert len(d['insulatedCrossings'])==5
for color,x,y in d['insulatedCrossings']:
 route=f'M{x-10:g} {y:g} Q{x:g} {y-14:g} {x+10:g} {y:g}'
 assert f'd="{route}" fill="none" stroke="white" stroke-width="14"' in h
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return v['left']+x*v['scale'],v['top']+y*v['scale']
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];assert f'data-net="{a}"' in h and f'd="{route}"' in h
 start=[float(v) for v in re.match(r'M([\d.]+) ([\d.]+)',route).groups()]
 assert all(math.isclose(v,w,abs_tol=1e-6) for v,w in zip(start,xy(a)))
 end=[float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])]
 assert all(math.isclose(v,w,abs_tol=1e-6) for v,w in zip(end,xy(b)))
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in h
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for row in ['| 5V | VIN |','| GND (아래쪽 POWER 헤더) | GND |','| A4 / SDA | SDI |','| A5 / SCL | SCK |']:assert row in readme
for s in ['uint8_t address = 0x77;','address = 0x76;','if (!bmp.begin(address))','Wire.setWireTimeout(25000, true);','Serial.begin(9600);','bmp.readPressure() / 100.0F;','!isfinite(tempC) || !isfinite(pressureHpa)','pressureHpa < 300.0F || pressureHpa > 1100.0F','tempC < -40.0F || tempC > 85.0F','ERROR: BMP280_NOT_FOUND','ERROR: BMP280_RANGE','delay(1000);']:assert s in code,s
assert code.count('if (!bmp.begin(address))')==2 and 'readAltitude' not in code
e=json.loads((p/'episode.json').read_text(encoding='utf8'))
assert len(e['cards'])==7 and e['slug']=='bmp280' and not e['review']['hardwareTested']
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
assert not any(s in e['caption'] for s in ['미시험','미검증','댓글에'])
assert e['caption'].count(e['repository'])==1
for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
print('PASS: 4 isolated nets; 7 unsafe/missing/swapped wiring mutations rejected; official SVG pin centers and endpoints; 5 insulated bridges; code/readme/table/units/addresses/limits; caption/photos. Not hardware/simulation execution.')
