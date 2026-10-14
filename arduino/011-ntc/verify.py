"""NTC divider/net/coordinate/formula checks. Not a hardware or simulation test."""
from pathlib import Path
import json,math,re,copy,xml.etree.ElementTree as ET
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
h=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')
def check_nets(data):
 groups=[]
 for a,b,c,_ in data['connections']:
  merge=[g for g in groups if a in g or b in g];group={a,b}
  for g in merge:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}=={frozenset(['uno:5V','r1:1']),frozenset(['uno:A0','r1:2','ntc:1']),frozenset(['uno:GND.1','ntc:2'])}
 parts={v['id']:v for v in data['parts']}
 assert len(parts)==3 and parts['r1']['attrs']['value']=='10000'
 assert parts['ntc']['attrs']=={'r25':'10000','beta25_50':'3950'}
check_nets(d)
for a,b in [('uno:5V','uno:GND.1'),('uno:A0','uno:5V'),('ntc:1','uno:GND.1')]:
 bad=copy.deepcopy(d);bad['connections'].append([a,b,'black',[]])
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('Unsafe wiring accepted')
bad=copy.deepcopy(d);bad['connections'].pop()
try:check_nets(bad)
except AssertionError:pass
else:raise AssertionError('Missing ground accepted')
parts={v['id']:v for v in d['parts']}
assert parts['uno']['pins']=={'5V':[160,191.5],'GND.1':[115.5,9],'A0':[208,191.5]}
assert parts['r1']['pins']=={'1':[0,5.65],'2':[58.8,5.65]}
assert parts['ntc']['pins']=={'1':[1.5,41.25],'2':[21.5,41.25]}
ntc=ET.fromstring(re.search(r'<svg class="ntc".*?</svg>',h,re.S).group())
for pin,x in [('connector0leg',1.5),('connector1leg',21.5)]:
 node=next(v for v in ntc.iter() if v.attrib.get('id')==pin)
 assert float(node.attrib['x2'])==x and float(node.attrib['y2'])==41.25
assert ntc.attrib['viewBox']=='0 0 23 44'
def xy(endpoint):
 a,b=endpoint.split(':');v=parts[a];x,y=v['pins'][b];s=v['scale']
 return (v['left']-y*s,v['top']+x*s) if v.get('rotate')==90 else (v['left']+x*s,v['top']+y*s)
for a,b,c,_ in d['connections']:
 route=d['previewRoutes'][a];nums=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
 assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(nums[:2],xy(a)))
 assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
 assert f'data-net="{a}"' in h and f'd="{route}"' in h
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in h
assert 'M680 600 Q690 585 700 600' in h and 'stroke="white" stroke-width="14"' in h
assert 'const byte NTC_PIN = A0;' in code and 'pinMode(NTC_PIN, INPUT);' in code
assert 'analogReference(DEFAULT);' in code and 'analogReference(EXTERNAL)' not in code
assert 'const float R_FIXED = 10000.0;' in code and 'const float R0 = 10000.0;' in code
assert 'const float T0_K = 298.15;' in code and 'const float BETA = 3950.0;' in code
assert code.index('if (raw <= 0 || raw >= 1023) return NAN;')<code.index('R_FIXED * raw / (1023.0 - raw)')
assert code.index('if (isnan(tempC))')<code.index('Serial.print("raw=")')
assert 'log(r / R0) / BETA' in code and '1.0 / invK - 273.15' in code
assert 'delay(1000);' in code and 'Serial.begin(9600);' in code
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
def t(raw):
 if raw<=0 or raw>=1023:return math.nan
 r=10000*raw/(1023-raw);return 1/(1/298.15+math.log(r/10000)/3950)-273.15
assert math.isnan(t(0)) and math.isnan(t(1023)) and math.isnan(t(-1))
assert abs(t(511.5)-25)<1e-9 and abs(t(400)-35.3)<.1
assert all(math.isfinite(t(v)) for v in range(1,1023))
assert all(t(v)>t(v+1) for v in range(1,1022))
for target in [15,25,35]:
 r=10000*math.exp(3950*(1/(target+273.15)-1/298.15));adc=round(1023*r/(10000+r))
 assert abs(t(adc)-target)<.1
# Published folders omit editor JSON. Run extra editable-caption/photo checks locally.
if (p/'episode.json').is_file():
 e=json.loads((p/'episode.json').read_text(encoding='utf8'))
 assert e['slug']=='ntc' and e['category']=='other-sensors' and not e['review']['hardwareTested']
 assert e['caption'].count(e['repository'])==1 and "'git'" not in e['caption']
 assert not any('git' in c['lead'].lower().replace('github','') for c in e['cards'])
 for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
 assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
print('PASS: 3 isolated divider nets; 4 unsafe/missing connections rejected; official UNO/resistor/NTC endpoints; bridge; R/B/DEFAULT/error guard; monotonic conversion and 15/25/35C inverse checks; code README/direct caption/photos')
