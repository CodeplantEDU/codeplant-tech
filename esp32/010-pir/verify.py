"""Host synthetic input checks. No physical sensor/firmware test."""
from pathlib import Path
import ast, contextlib, io, json, sys, types, copy
p=Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf-8'); ast.parse(source)
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
def check_nets(data):
 expected=[('supply:V+','pir:VCC'),('supply:GND','pir:GND'),('esp:GND.1','supply:GND'),('pir:OUT','esp:D27')]
 assert len(data['connections'])==4
 assert {frozenset(x[:2]) for x in data['connections']}=={frozenset(x) for x in expected}
check_nets(d)
for i,end,pin in [(0,0,'esp:VIN'),(0,0,'esp:3V3'),(3,1,'esp:D34'),(2,0,'esp:3V3')]:
 bad=copy.deepcopy(d); bad['connections'][i][end]=pin
 try: check_nets(bad)
 except AssertionError: pass
 else: raise AssertionError('unsafe mutation accepted')
preview=(p/'circuit_preview.html').read_text(encoding='utf-8')
for route in d['previewRoutes'].values(): assert 'd="'+route+'"' in preview
assert d['parts'][0]['pins']=={'D27':[5,110.8],'GND.1':[101.3,149]}
def run(events, stop_warmup=False):
 log=[]; frames=iter(events)
 class Pin:
  IN=0
  def __init__(self,n,mode,pull): assert (n,mode,pull)==(27,0,None)
  def value(self):
   assert log[0]==('sleep',60000)
   log.append(('read',27)); event=next(frames)
   if isinstance(event,BaseException): raise event
   return event
 def sleep(ms):
  assert ms in [50,60000]; log.append(('sleep',ms))
  if ms==60000 and stop_warmup: raise KeyboardInterrupt
 mocks={'machine':types.SimpleNamespace(Pin=Pin),'time':types.SimpleNamespace(sleep_ms=sleep)}
 saved={k:sys.modules.get(k) for k in mocks}; sys.modules.update(mocks)
 out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out): exec(compile(source,str(p/'main.py'),'exec'),{})
 finally:
  for k,v in saved.items():
   if v is None: sys.modules.pop(k,None)
   else: sys.modules[k]=v
 return out.getvalue(),log
out,log=run([0,0,1,1,0,KeyboardInterrupt()])
assert out.splitlines()==['WAIT_60S','READY: GPIO27 input','pir = 0, level = LOW','pir = 1, level = HIGH','pir = 0, level = LOW','STOP']
assert log==[('sleep',60000)]+[v for _ in range(5) for v in [('read',27),('sleep',50)]]+[('read',27)]
out,log=run([1,1,KeyboardInterrupt()]); assert out.count('pir = 1')==1 and out.count('pir = 0')==0
out,log=run([],True); assert out=='WAIT_60S\nSTOP\n' and log==[('sleep',60000)]
try: run([OSError('pin read')])
except OSError: pass
else: raise AssertionError('pin error silently swallowed')
assert source in (p/'README.md').read_text(encoding='utf-8')
e=json.loads((p/'episode.json').read_text(encoding='utf-8'))
assert e['category']=='other-sensors' and len(e['cards'])==10
assert e['repository'].endswith('/esp32/010-pir')
assert not any(t in e['caption'] for t in ['미시험','미검증','검증 완료','댓글에'])
for c in e['cards']: assert 'http' not in c['title']+c['lead']+c.get('note','')
print('PASS: syntax/README code parity, 4 exact nets, unsafe pin/power mutations, 60s before first read, initial HIGH/LOW, change-only printing, 50ms each loop, Ctrl+C during warmup/read, pin error propagation. Hardware NOT tested.')
