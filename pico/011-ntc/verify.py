"""Synthetic host checks. No physical ADC or NTC measurements."""
from pathlib import Path
import ast,contextlib,io,json,sys,types,copy,re
p=Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf-8');ast.parse(source)
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
def check_nets(x):
 expected=[('pico:3V3','r1:1'),('r1:2','ntc:1'),('pico:GP26','ntc:1'),('pico:AGND','ntc:2')]
 assert len(x['connections'])==4 and {frozenset(c[:2]) for c in x['connections']}=={frozenset(c) for c in expected}
 assert x['parts'][1]['attrs']['value']=='10000'
check_nets(d)
for i,j,pin in [(0,0,'pico:VBUS'),(0,0,'pico:AGND'),(2,0,'pico:GP27'),(3,1,'ntc:1')]:
 bad=copy.deepcopy(d);bad['connections'][i][j]=pin
 try:check_nets(bad)
 except AssertionError:pass
 else:raise AssertionError('unsafe wiring accepted')
assert d['parts'][0]['physicalPins']=={'3V3':36,'GP26':31,'AGND':33}
assert abs(3.3*10000/20000-1.65)<1e-9 and abs(3.3*5000/15000-1.10)<1e-9

def run(events,interrupt_wait=False):
 frames=iter(events);log=[]
 class Pin:
  def __init__(self,n):assert n==26
 class ADC:
  ATTN_11DB=11
  def __init__(self,pin):pass
  def read_u16(self):
   log.append('read');v=next(frames)
   if isinstance(v,BaseException):raise v
   assert 0<=v<=65535;return v
 def sleep(ms):
  assert ms in [1000,10];log.append(ms)
  if ms==1000 and interrupt_wait:raise KeyboardInterrupt
 mocks={'machine':types.SimpleNamespace(Pin=Pin,ADC=ADC),'time':types.SimpleNamespace(sleep_ms=sleep)}
 saved={k:sys.modules.get(k) for k in mocks};sys.modules.update(mocks);out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):exec(compile(source,str(p/'main.py'),'exec'),{})
 finally:
  for k,v in saved.items():
   if v is None:sys.modules.pop(k,None)
   else:sys.modules[k]=v
 return out.getvalue(),log
out,log=run(list(range(1000,1010))+[0,65535]+[30000]*8+[20000]*10+[KeyboardInterrupt()])
assert out.splitlines()==['READY: NTC raw input GP26','raw_u16 = 1004','ADC_ENDPOINT raw_u16 = 30553','raw_u16 = 20000','STOP']
assert log==[v for _ in range(3) for v in [1000]+['read',10]*10]+[1000,'read']
out,log=run([65535]*10+[KeyboardInterrupt()]);assert 'ADC_ENDPOINT raw_u16 = 65535' in out
out,log=run([],True);assert out.endswith('STOP\n') and log==[1000]
out,log=run([OSError('mock')]);assert 'ADC_ERROR: mock' in out and log==[1000,'read'] and 'raw_u16 =' not in out
assert source in (p/'README.md').read_text(encoding='utf-8')
if (p/'episode.json').exists():
 e=json.loads((p/'episode.json').read_text(encoding='utf-8'))
 assert len(e['cards'])==10 and e['category']=='other-sensors'
 assert not any(t in e['caption'] for t in ['미시험','미검증','검증 완료','댓글에'])
 for c in e['cards']:assert 'http' not in c['title']+c['lead']+c.get('note','')
else:
 assert len(list((p/'cards').glob('[0-9][0-9].png')))==10
 print('SKIP: local-only episode metadata/caption checks; episode.json is not in the public package.')
print('PASS: Pico 4 wiring nets and unsafe mutations; synthetic averaging/endpoints/reset/waits/Ctrl+C/OSError; README exact code. Hardware untested.')
