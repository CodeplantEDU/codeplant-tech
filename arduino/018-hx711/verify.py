"""Physical net/geometry and conversion checks; not a simulator or hardware test."""
from pathlib import Path
import copy,json,re,math,xml.etree.ElementTree as ET
p=Path(__file__).parent;d=json.loads((p/'diagram.json').read_text(encoding='utf8'));e=json.loads((p/'episode.json').read_text(encoding='utf8'));code=(p/'sketch.ino').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [('uno:5V','hx:VDD','hx:VCC'),('uno:GND.2','hx:GND'),('uno:3','hx:DAT'),('uno:2','hx:SCK'),('cell:E+','hx:RED'),('cell:E-','hx:BLK'),('cell:S+','hx:GRN'),('cell:S-','hx:WHT')]}
def check_nets(data):
 groups=[]
 for a,b,*_ in data['connections']:
  g={a,b}
  for old in list(groups):
   if g & old:g.update(old);groups.remove(old)
  groups.append(g)
 assert {frozenset(x) for x in groups}==expected and len(data['connections'])==9
check_nets(d)
bad=[]
for a,b in [('uno:5V','uno:GND.2'),('hx:DAT','hx:SCK'),('cell:S+','hx:WHT'),('hx:RED','hx:VCC'),('hx:YLW','cell:S-')]:
 v=copy.deepcopy(d);v['connections'].append([a,b,'red',[]]);bad.append(v)
v=copy.deepcopy(d);v['connections'].pop();bad.append(v)
v=copy.deepcopy(d);v['connections'][0][0]='uno:VIN';bad.append(v)
v=copy.deepcopy(d);v['connections'][7][1],v['connections'][8][1]=v['connections'][8][1],v['connections'][7][1];bad.append(v)
for v in bad:
 try:check_nets(v)
 except AssertionError:pass
 else:raise AssertionError('Wrong physical wiring accepted')
parts={x['id']:x for x in d['parts']};assert parts['uno']['pins']=={'3':[227,9],'2':[236.5,9],'5V':[160,191.5],'GND.2':[169.5,191.5]}
assert parts['hx']['pinIds']['GRN']=='connector24pin' and parts['hx']['pinIds']['WHT']=='connector25pin'
assert parts['hx']['pins']['GRN'][1]>parts['hx']['pins']['WHT'][1]
for fname in ['circuit_preview.html','circuit_preview_control.html']:
 h=(p/fname).read_text(encoding='utf8');sv=ET.fromstring(re.search(r'<div class="hx"[^>]*>(.*?)</div>',h,re.S).group(1));parents={c:n for n in sv.iter() for c in n}
 for name,id in parts['hx']['pinIds'].items():
  el=sv.find(f'.//*[@id="{id}"]');assert [float(el.attrib['cx']),float(el.attrib['cy'])]==parts['hx']['pins'][name]
  while el is not None:
   assert not el.attrib.get('transform');el=parents.get(el)
def xy(part,pin):
 a=parts[part];x,y=a['pins'][pin];return a['left']+x*a['scale'],a['top']+y*a['scale']
ends={'VDD':('5V',),'VCC':None,'GND':('GND.2',),'DAT':('3',),'SCK':('2',)}
h=(p/'circuit_preview.html').read_text(encoding='utf8')
for pin,points in d['previewRoutes'].items():
 for actual,desired in [(points[0],xy('hx',pin))]+([(points[-1],xy('uno',ends[pin][0]))] if ends[pin] else []):assert all(math.isclose(a,b,abs_tol=2e-5) for a,b in zip(actual,desired))
 if pin=='VCC':assert points[-1]==[906,520] and points[-1] in d['previewRoutes']['VDD']
 v=re.search(fr'data-net="{pin}" d="([^"]+)"',h).group(1);rendered=[[float(a),float(b)] for a,b in re.findall(r'[ML]([\d.]+) ([\d.]+)',v)];assert len(rendered)==len(points)
 assert all(math.isclose(a,b,abs_tol=2e-5) for row,desired in zip(rendered,points) for a,b in zip(row,desired))
assert len(d['insulatedCrossings'])==6
for signal,pin in [('E+','RED'),('E-','BLK'),('S+','GRN'),('S-','WHT')]:
 v=d['loadcellPreview'];actual=v['routes'][signal][-1];x,y=parts['hx']['pins'][pin];assert all(math.isclose(a,b,abs_tol=2e-5) for a,b in zip(actual,[v['left']+x*v['scale'],v['top']+y*v['scale']]))
assert f'```cpp\n{code.rstrip()}\n```' in readme
assert re.search(r'KNOWN_MASS_G\s*=\s*0\.0f',code)
average=code.split('bool averageRaw')[1].split('void setup')[0]
assert average.index('wait_ready_timeout(1000, 1)')<average.index('scale.read()')<average.index('sum += sample')
assert 'sample <= -8388608L || sample >= 8388607L' in average and average.count('return false;')==2
assert "zeroed = calibrated = false;" in code and "if (calibrated)" in code
assert 'KNOWN_MASS_G <= 0 || KNOWN_MASS_G > 5000' in code and 'isfinite(countsPerGram) && countsPerGram != 0' in code
# Evaluate the exact two firmware expressions with positive/negative gain and an independent known-mass check.
factor=re.search(r'countsPerGram = ([^;]+);',code[code.index('void loop'):]).group(1)
mass=re.search(r'float massG = ([^;]+);',code).group(1)
for zeroRaw,referenceRaw,checkRaw,known,expectedG in [(1000,11000,6000,100,50),(1000,-9000,-4000,100,50),(-10000,0,-5000,100,50)]:
 countsPerGram=eval(factor,{'__builtins__':{}},dict(raw=referenceRaw,zeroRaw=zeroRaw,KNOWN_MASS_G=known));got=eval(mass,{'__builtins__':{}},dict(raw=checkRaw,zeroRaw=zeroRaw,countsPerGram=countsPerGram));assert math.isclose(got,expectedG)
assert (8388607*10)<2147483647
assert e['cards'][3]['rows'][3]==['초록','GRN','A+ · 신호 +'] and e['cards'][3]['rows'][4]==['흰색','WHT','A− · 신호 −']
assert '초록→GRN(A+), 흰색→WHT(A−)' in e['caption']
assert not re.search('미검증|미시험|하드웨어 시험',e['caption'])
assert len(e['cards'])==8 and e['cards'][-1]['title']=='전체 코드는\nGitHub에서 확인하세요'
for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]+[v['image'] for v in e['cards'] if 'image' in v]:assert (p/Path(src).name).is_file()
print('PASS: nine physical connections/eight nets; eight bad wiring mutations rejected; official connector geometry and six bridges; signed calibration expressions; per-sample timeout/static guards; README/code/table/caption/assets. No hardware or simulator execution.')
