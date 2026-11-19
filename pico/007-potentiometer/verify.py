import ast, contextlib, io, json, pathlib, re, runpy, sys, types
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf-8');ast.parse(source)
assert '```python\n'+source.rstrip()+'\n```' in (p/'README.md').read_text(encoding='utf-8')
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
expected={('pico:3V3','pot:VCC','red'),('pico:AGND','pot:GND','black'),('pico:GP26','pot:SIG','yellow')}
def check(d):
 assert len(d['connections'])==3 and {(a,b,c) for a,b,c,_ in d['connections']}==expected
check(d)
import copy
for i in range(3):
 bad=copy.deepcopy(d);bad['connections'][i][0]='esp:VIN'
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('unsafe mutation accepted')
h=(p/'circuit_preview.html').read_text(encoding='utf-8')
parts={x['id']:x for x in d['parts']}
for a,b,c,_ in d['connections']:
 route=re.search('data-net="'+re.escape(a)+'"[^>]*d="([^"]+)"',h).group(1)
 assert route==d['previewRoutes'][a]
 nums=re.findall(r'-?\d+(?:\.\d+)?',route);start=tuple(map(float,nums[:2]));end=tuple(map(float,nums[-2:]))
 for name,point in [(a,start),(b,end)]:
  part,pin=name.split(':');v=parts[part];x,y=v['pins'][pin];want=(v['left']+x*v['scale'],v['top']+y*v['scale']);assert all(abs(k-l)<0.02 for k,l in zip(point,want)),(name,point,want)
def run(values):
 events=[];it=iter(values)
 class Pin:
  def __init__(self,n):assert n==26
 class ADC:
  def __init__(self,pin):events.append('init')
  def read_u16(self):
   v=next(it)
   if isinstance(v,BaseException):raise v
   events.append(('read',v));return v
 def sleep(n):
  assert n==100;events.append(('sleep',n))
 m=types.ModuleType('machine');m.Pin=Pin;m.ADC=ADC;t=types.ModuleType('time');t.sleep_ms=sleep
 out=io.StringIO()
 with patch.dict(sys.modules,{'machine':m,'time':t}),contextlib.redirect_stdout(out):
  runpy.run_path(str(p/'main.py'),run_name='__main__')
 return events,out.getvalue().splitlines()
events,out=run([0,32768,65535,KeyboardInterrupt()])
assert out==['READY: potentiometer -> GP26','raw_u16 = 0','raw_u16 = 32768','raw_u16 = 65535','STOP']
assert events==['init',('read',0),('sleep',100),('read',32768),('sleep',100),('read',65535),('sleep',100)]
assert run([OSError('synthetic')])[1][-1]=='ADC_ERROR: synthetic'
e=json.loads((p/'episode.json').read_text(encoding='utf8'))
assert len(e['cards'])==10 and e['category']=='other-sensors'
assert e['cards'][6]['code'] in '\n'.join(line.strip() for line in source.splitlines())
assert 'atten' not in source and 'WIDTH_' not in source and 'deinit' not in source
assert e['caption'].count(e['repository'])==1
print('PASS: 3 nets, unsafe mutations, 6 endpoints, ADC Pin26, 0/mid/full synthetic values, order, 100ms, Ctrl+C and read error, README and card sync')
