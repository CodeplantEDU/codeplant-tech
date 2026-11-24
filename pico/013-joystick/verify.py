from pathlib import Path
import json,copy,types,sys,io,contextlib,ast
p=Path(__file__).parent;source=(p/'main.py').read_text(encoding='utf-8');ast.parse(source)
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
def nets(x):
 pairs=[('pico:3V3','joy:VCC'),('pico:GP26','joy:VRX'),('pico:GP27','joy:VRY'),('pico:GP16','joy:SW'),('pico:GND','joy:GND'),('r1:1','joy:VCC'),('r1:2','joy:SW')]
 assert len(x['connections'])==7 and {frozenset(c[:2]) for c in x['connections']}=={frozenset(c) for c in pairs}
 assert x['parts'][2]['attrs']['value']=='10000'
nets(d)
for i,j,bad in [(0,0,'pico:VBUS'),(1,0,'pico:GP28'),(2,1,'joy:VRX'),(6,1,'joy:GND')]:
 m=copy.deepcopy(d);m['connections'][i][j]=bad
 try:nets(m)
 except AssertionError:pass
 else:raise AssertionError('unsafe mutation accepted')
assert d['parts'][0]['physicalPins']=={'3V3':36,'GP26':31,'GP27':32,'GP16':21,'GND':38}
assert source in (p/'README.md').read_text(encoding='utf-8')
def run(fail=False):
 frames=[(0,65535,1),(65535,0,0),(32000,33000,1)];index=[0];log=[]
 class Pin:
  IN=0
  def __init__(self,n,mode=None):
   self.n=n;assert (n in [26,27] and mode is None) or (n==16 and mode==Pin.IN)
  def value(self):log.append('SW');return frames[index[0]][2]
 class ADC:
  def __init__(self,pin):self.n=pin.n
  def read_u16(self):
   log.append(self.n)
   if fail:raise OSError('mock ADC error')
   return frames[index[0]][0 if self.n==26 else 1]
 def sleep(ms):
  assert ms==150;log.append(ms);index[0]+=1
  if index[0]==len(frames):raise KeyboardInterrupt
 mocks={'machine':types.SimpleNamespace(Pin=Pin,ADC=ADC),'time':types.SimpleNamespace(sleep_ms=sleep)}
 saved={k:sys.modules.get(k) for k in mocks};sys.modules.update(mocks);out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):exec(compile(source,'main.py','exec'),{})
 finally:
  for k,v in saved.items():
   if v is None:sys.modules.pop(k,None)
   else:sys.modules[k]=v
 return out.getvalue().splitlines(),log
out,log=run();assert out==['X=0 Y=65535 SW=released','X=65535 Y=0 SW=pressed','X=32000 Y=33000 SW=released','STOP'];assert log==[26,27,'SW',150]*3
try:run(True)
except OSError:pass
else:raise AssertionError('read error hidden')
print('PASS: seven exact nets, external10k, unsafe mutations, Pico physical pins, syntax/README exact code, X/Y endpoints, SW states, read order/150ms/Ctrl+C, propagated ADC error. Hardware untested.')
