"""Host-only assertions: no ESP32, servo or measured waveform execution."""
import ast,contextlib,copy,io,json,pathlib,sys,types
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf8');ast.parse(source)
assert '```python\n'+source.rstrip()+'\n```' in (p/'README.md').read_text(encoding='utf8')
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
def nets(data):
 groups=[]
 for a,b,c,_ in data['connections']:
  g={a,b};same=[x for x in groups if x&g]
  for x in same:g|=x;groups.remove(x)
  groups.append(g)
 return {frozenset(g) for g in groups}
expected={frozenset(('esp:D18','u1:2','r1:1')),frozenset(('u1:3','servo1:PWM')),frozenset(['ext5v:VCC','servo1:V+','c1:1']+[f'u1:{n}' for n in [14,4,10,13]]),frozenset(['extgnd:GND','servo1:GND','esp:GND.1','r1:2','c1:2']+[f'u1:{n}' for n in [1,7,5,9,12]])}
assert nets(d)==expected
assert all(f'u1:{n}' not in set().union(*nets(d)) for n in [6,8,11])
for forbidden in ['esp:3V3','esp:VIN','esp:5V']:
 bad=copy.deepcopy(d);bad['connections'].append(['ext5v:VCC',forbidden,'red',[]]);assert nets(bad)!=expected
parts={v['id']:v for v in d['parts']};assert parts['r1']['attrs']['value']=='10000';assert parts['c1']['attrs']['value']=='100nF'
assert parts['u1']['attrs']['package']=='TI N PDIP14'

def run(changes=None,fail=None):
 code=source
 for a,b in (changes or {}).items():code=code.replace(a,b)
 events=[];count=[0]
 class Pin:
  OUT=1
  def __init__(self,n,mode,value):assert(n,mode,value)==(18,1,0);events.append(('pin',18,0))
  def init(self,mode,value):assert(mode,value)==(1,0);events.append(('low',))
 class PWM:
  def __init__(self,pin,*,freq,duty_ns):
   assert(freq,duty_ns)==(50,1500000);events.append(('init',freq,duty_ns))
   if fail=='init':raise OSError('synthetic init')
  def duty_ns(self,n):
   assert 1400000<=n<=1600000;events.append(('pulse',n))
   if fail=='update':raise OSError('synthetic update')
  def deinit(self):
   events.append(('deinit',))
   if fail=='deinit':raise OSError('synthetic deinit')
 def sleep(n):
  assert n>=2000;events.append(('sleep',n));count[0]+=1
  if count[0]>=5:raise KeyboardInterrupt()
 machine=types.ModuleType('machine');machine.Pin=Pin;machine.PWM=PWM
 time=types.ModuleType('time');time.sleep_ms=sleep
 out=io.StringIO()
 with patch.dict(sys.modules,{'machine':machine,'time':time}),contextlib.redirect_stdout(out):
  try:exec(compile(code,'main.py','exec'),{'__name__':'__main__'})
  except OSError:
   assert fail=='deinit'
 return events,out.getvalue()
ev,out=run();assert out.count('command_us =')==1;assert ev[-2:]==[('deinit',),('low',)];assert 'STOP:' in out
assert [v[1] for v in ev if v[0]=='pulse']==[1500000]*5
ev,out=run({'COMPARE = False':'COMPARE = True'});assert [v[1] for v in ev if v[0]=='pulse']==[1500000,1400000,1500000,1600000,1500000]
ev,_=run({'COMPARE = False':'COMPARE = True','STEP_US = 100':'STEP_US = 50'});assert [v[1] for v in ev if v[0]=='pulse']==[1500000,1450000,1500000,1550000,1500000]
for changes in [{'CENTER_US = 1500':'CENTER_US = 1700'},{'STEP_US = 100':'STEP_US = 101'},{'HOLD_MS = 2000':'HOLD_MS = 20'},{'COMPARE = False':'COMPARE = True','CENTER_US = 1500':'CENTER_US = 1400'}]:
 ev,out=run(changes);assert ev==[] and 'PWM_ERROR:' in out
for fail in ['init','update','deinit']:
 ev,out=run(fail=fail);assert ev[-1]==('low',)
 if fail!='deinit':assert 'PWM_ERROR:' in out
ns={};exec(compile('\n'.join(source.splitlines()[11:15]),'check','exec'),ns)
for v in [1400,1500,1600]:assert ns['check_pulse'](v)==v
for v in [1399,1601,1500.0,'1500']:
 try:ns['check_pulse'](v)
 except ValueError:pass
 else:raise AssertionError(v)
e=json.loads((p/'episode.json').read_text(encoding='utf8'));assert len(e['cards'])==12
assert e['caption'].count(e['repository'])==1
assert not any(v in e['caption'] for v in ['미시험','미검증','하드웨어 시험 미완료'])
assert all('http' not in c.get('title','')+c.get('lead','')+c.get('note','') for c in e['cards'])
print('PASS4 exact nets/TI14pin assignments/unused outputs/unsafe-power mutations/AST/README full code/center and compare/50us step/range errors/Ctrl+C/PWM init-update-deinit faults; synthetic host only')
