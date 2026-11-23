from pathlib import Path
import json,copy,types,sys,contextlib,io,ast
p=Path(__file__).parent;source=(p/'main.py').read_text(encoding='utf-8');ast.parse(source)
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
def nets(x):
 expected=[('pico:3V3','temp:VCC'),('pico:GND','temp:GND'),('pico:GP16','temp:DQ'),('r1:1','temp:DQ'),('r1:2','temp:VCC')]
 assert {frozenset(c[:2]) for c in x['connections']}=={frozenset(c) for c in expected} and len(x['connections'])==5
 assert x['parts'][2]['attrs']['value']=='4700'
nets(d)
for i,j,bad in [(0,0,'pico:VBUS'),(2,0,'pico:GP18'),(3,1,'temp:GND'),(4,1,'temp:GND')]:
 m=copy.deepcopy(d);m['connections'][i][j]=bad
 try:nets(m)
 except AssertionError:pass
 else:raise AssertionError('unsafe net accepted')
assert d['parts'][0]['physicalPins']=={'3V3':36,'GP16':21,'GND':38}
assert d['parts'][1]['pins']=={'GND':[1.46,13],'DQ':[4,13],'VCC':[6.54,13]}
assert source in (p/'README.md').read_text(encoding='utf-8')
def run(roms,temp=23.5,error=None,stopat=None):
 log=[]
 class Pin:
  def __init__(self,n):assert n==16
 class Sensor:
  def __init__(self,ow):pass
  def scan(self):log.append('scan');return roms
  def convert_temp(self):log.append('convert')
  def read_temp(self,rom):
   log.append('read')
   if error:raise error
   return temp
 def sleep(ms):
  log.append(ms)
  if ms==1000 or stopat==ms:raise KeyboardInterrupt
 mocks={'machine':types.SimpleNamespace(Pin=Pin),'onewire':types.SimpleNamespace(OneWire=lambda p:p),'ds18x20':types.SimpleNamespace(DS18X20=Sensor),'time':types.SimpleNamespace(sleep_ms=sleep)}
 saved={k:sys.modules.get(k) for k in mocks};sys.modules.update(mocks);out=io.StringIO()
 try:
  with contextlib.redirect_stdout(out):exec(compile(source,'main.py','exec'),{})
 finally:
  for k,v in saved.items():
   if v is None:sys.modules.pop(k,None)
   else:sys.modules[k]=v
 return out.getvalue(),log
rom=bytes([0x28])+bytes(7)
out,log=run([rom]);assert out=='23.50 C\nSTOP\n' and log==['scan','convert',750,'read',1000]
out,log=run([rom],-10.125);assert out.startswith('-10.12 C')
for rs,count in [([],0),([rom,rom],2),([bytes([0x10])+bytes(7)],0)]:
 out,log=run(rs);assert 'Connect exactly one DS18B20: '+str(count) in out and log==['scan',1000]
out,log=run([rom],error=Exception('CRC error'));assert '1-Wire error: CRC error' in out
out,log=run([rom],stopat=750);assert out=='STOP\n' and log==['scan','convert',750]
print('PASS: five wiring nets, unsafe changes rejected, physical and sensor pins, syntax/README match, normal/negative/absent/multiple/other-family/CRC/Ctrl+C and conversion wait order. Hardware untested.')
