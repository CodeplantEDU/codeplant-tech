"""DS18B20 external-power wiring and source consistency. No hardware test."""
from pathlib import Path
import copy,json,math,re,xml.etree.ElementTree as ET
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
 assert {frozenset(g) for g in groups}=={frozenset(['uno:5V','temp:VCC','r1:2']),frozenset(['uno:GND.1','temp:GND']),frozenset(['uno:2','temp:DQ','r1:1'])}
 parts={v['id']:v for v in data['parts']}
 assert len(parts)==3 and parts['r1']['attrs']['value']=='4700'
 assert len(data['connections'])==5
check_nets(d)
invalid=[]
for a,b in [('uno:5V','uno:GND.1'),('temp:DQ','uno:GND.1'),('temp:DQ','uno:5V')]:
 bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]]);invalid.append(bad)
bad=copy.deepcopy(d);bad['connections'].pop();invalid.append(bad)
bad=copy.deepcopy(d);bad['parts'][2]['attrs']['value']='10000';invalid.append(bad)
for bad in invalid:
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('Unsafe wiring or wrong pull-up accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'2':[236.5,9],'5V':[160,191.5],'GND.1':[115.5,9]}
assert parts['temp']['pins']=={'GND':[1.46,13],'DQ':[4,13],'VCC':[6.54,13]}
assert parts['r1']['pins']=={'1':[0,5.65],'2':[58.8,5.65]}
sensor=ET.fromstring(re.search(r'<svg class="sensor".*?</svg>',h,re.S).group())
assert sensor.attrib['viewBox']=='0 0 8.564 13.388'
assert 'translate(-71.965 -103.44)' in h and 'value="4700"' in h

def xy(endpoint):
 a,b=endpoint.split(':');v=parts[a];x,y=v['pins'][b];s=v['scale']
 return (v['left']-y*s,v['top']+x*s) if v.get('rotate')==90 else (v['left']+x*s,v['top']+y*s)
for a,b,_,_ in d['connections']:
 route=d['previewRoutes'][a];nums=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
 assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(nums[:2],xy(a)))
 assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
 assert f'data-net="{a}"' in h and f'd="{route}"' in h
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in h
for value in ['#include <OneWire.h>','#include <DallasTemperature.h>','const byte DATA_PIN = 2;','OneWire oneWire(DATA_PIN);','DallasTemperature sensors(&oneWire);','sensors.setResolution(12);','sensors.setWaitForConversion(true);','delay(1000);','Serial.begin(9600);']:
 assert value in code
assert code.index('sensors.requestTemperatures();')<code.index('sensors.getTempCByIndex(0)')<code.index('if (tempC == DEVICE_DISCONNECTED_C)')<code.index('return;')<code.index('Serial.print("temp_C=");')
assert 'Serial.println(tempC, 2);' in code
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
assert (p/'libraries.txt').read_text(encoding='utf8').splitlines()[:2]==['DallasTemperature@4.0.6','OneWire@2.3.8']
if (p/'episode.json').is_file():
 e=json.loads((p/'episode.json').read_text(encoding='utf8'))
 assert e['slug']=='ds18b20' and e['category']=='other-sensors' and not e['review']['hardwareTested']
 assert e['caption'].count(e['repository'])==1
 assert not any(v in e['caption'] for v in ['미검증','미시험','시험하지','git 댓글','댓글에'])
 assert not re.search(r'\bDM\b',e['caption'])
 assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
 for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
print('PASS: 3 isolated nets; 5 unsafe/missing/wrong-pullup mutations rejected; official pin coordinates and preview endpoints; D2/12bit/wait/error guard; README full code; library versions; caption/photos')
