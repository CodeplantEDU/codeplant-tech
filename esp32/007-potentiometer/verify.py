import ast, contextlib, io, json, pathlib, re, runpy, sys, types
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf-8');ast.parse(source)
assert '```python\n'+source.rstrip()+'\n```' in (p/'README.md').read_text(encoding='utf-8')
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
expected={('esp:3V3','pot:VCC','red'),('esp:GND.1','pot:GND','black'),('esp:D34','pot:SIG','yellow')}
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
def run(values,width_error=False,sleep_error=False):
 events=[];it=iter(values)
 class Pin:
  def __init__(self,n):assert n==34
 class ADC:
  ATTN_11DB=11;WIDTH_12BIT=12
  def __init__(self,pin,*,atten):assert atten==11
  def width(self,n):
   assert n==12;events.append('width')
   if width_error:raise OSError('width')
  def read_u16(self):
   v=next(it)
   if isinstance(v,BaseException):raise v
   events.append(('read',v));return v
  def deinit(self):events.append('deinit')
 def sleep(n):
  assert n==100;events.append(('sleep',n))
  if sleep_error:raise KeyboardInterrupt()
 m=types.ModuleType('machine');m.Pin=Pin;m.ADC=ADC;t=types.ModuleType('time');t.sleep_ms=sleep;out=io.StringIO()
 with patch.dict(sys.modules,{'machine':m,'time':t}),contextlib.redirect_stdout(out):runpy.run_path(str(p/'main.py'),run_name='__main__')
 assert events[-1]=='deinit';return events,out.getvalue().splitlines()
e,o=run([0,32768,65535,KeyboardInterrupt()]);assert o==['READY: potentiometer -> GPIO34','raw_u16 = 0','raw_u16 = 32768','raw_u16 = 65535','STOP'];assert e[1:-1]==[('read',0),('sleep',100),('read',32768),('sleep',100),('read',65535),('sleep',100)]
for vals in [[OSError('synthetic')],[123,OSError('synthetic')]]:
 e,o=run(vals);assert o[-1]=='ADC_ERROR: synthetic'
e,o=run([],width_error=True);assert o==['ADC_ERROR: width']
e,o=run([123],sleep_error=True);assert o[-1]=='STOP'
e=json.loads((p/'episode.json').read_text());assert len(e['cards'])==10 and e['category']=='other-sensors'
assert not any(x in e['caption'] for x in ['미시험','미검증','하드웨어 시험 미완료'])
for c in e['cards']:
 for v in [c.get('image')]+[x['src'] for x in c.get('photos',[])]:
  if v:assert (p/v.split('/')[-1]).is_file()
assert e['cards'][6]['code'] in '\n'.join(line.strip() for line in source.splitlines())
print('PASS: 3 exact nets, 3 unsafe mutations rejected, 6 endpoint coordinates, source/README/card sync, synthetic values/order/100ms/interrupt/read+width error/cleanup. No hardware execution.')
