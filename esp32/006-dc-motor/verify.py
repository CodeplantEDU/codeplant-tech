"""Host assertions only: do not claim physical motor or MicroPython execution."""
import ast,contextlib,copy,io,json,pathlib,sys,types
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf8');ast.parse(source)
assert '```python\n'+source.rstrip()+'\n```' in (p/'README.md').read_text(encoding='utf8')
e=json.loads((p/'episode.json').read_text(encoding='utf8'));d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
expected={('esp:D25','driver:ENA','yellow'),('esp:D26','driver:IN1','blue'),('esp:D27','driver:IN2','green'),('logic5v:VCC','driver:5V','red'),('esp:GND.1','driver:GND','black'),('ext6v:VCC','driver:12V','red'),('extgnd:GND','driver:GND','black'),('driver:OUT1','motor:1','orange'),('driver:OUT2','motor:2','purple'),('driver:ENB','driver:GND','black'),('driver:IN3','driver:GND','black'),('driver:IN4','driver:GND','black'),('logicgnd:GND','driver:GND','black'),('driver:ENA','r:1','yellow'),('r:2','driver:GND','black')}
def check(data):
 assert len(data['connections'])==15
 assert {(a,b,c) for a,b,c,_ in data['connections']}==expected
 attrs=next(v['attrs'] for v in data['parts'] if v['id']=='driver');assert all(attrs[n]=='removed' for n in ['5V-EN','ENA-jumper','ENB-jumper'])
 assert next(v['attrs']['value'] for v in data['parts'] if v['id']=='r')=='10000'
check(d)
for badpin in ['esp:VIN','esp:3V3','esp:D25']:
 bad=copy.deepcopy(d);bad['connections'].append(['ext6v:VCC',badpin,'red',[]])
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError('unsafe power accepted')
for file,key in [('circuit_preview.html','powerPaths'),('circuit_preview_control.html','controlPaths')]:
 text=(p/file).read_text(encoding='utf8')
 for name,color,path in e['circuit'][key]:assert 'd="'+path+'"' in text,(name,path)
# Photo terminal points, from unchanged SunFounder851px-wide source, transformed.
for pin,left,top,width,file in [('12V',600,70,500,'circuit_preview.html'),('GND',600,70,500,'circuit_preview.html'),('5V',600,70,500,'circuit_preview.html'),('ENA',100,60,450,'circuit_preview_control.html'),('IN1',100,60,450,'circuit_preview_control.html'),('IN2',100,60,450,'circuit_preview_control.html'),('OUT1',100,60,450,'circuit_preview_control.html'),('OUT2',100,60,450,'circuit_preview_control.html')]:
 x,y=e['circuit']['photoPinCenters'][pin];assert f'cx="{round(left+x*width/851,3)}" cy="{round(top+y*width/851,3)}"' in (p/file).read_text(encoding='utf8')

def run(inputs,changes=None,fail=None):
 code=source
 for a,b in (changes or {}).items():code=code.replace(a,b)
 events=[];state={};duty=[0];sleepcount=[0];faulted=[False]
 class Pin:
  OUT=1
  def __init__(self,n,mode,value):assert n in (25,26,27) and(mode,value)==(1,0);self.n=n;state[n]=0;events.append(('pin',n,0))
  def value(self,v):
   assert v in (0,1);assert duty[0]==0,'direction changed while enabled';state[self.n]=v;events.append(('dir',self.n,v))
  def init(self,mode,value):assert(mode,value)==(1,0);state[self.n]=0;events.append(('low',self.n))
 class PWM:
  def __init__(self,pin,*,freq,duty_u16):
   assert pin.n==25 and(freq,duty_u16)==(1000,0);events.append(('init',))
   if fail=='init':raise OSError('synthetic init')
  def duty_u16(self,v):
   assert 0<=v<=65535
   if fail=='update' and v>0 and not faulted[0]:faulted[0]=True;raise OSError('synthetic update')
   duty[0]=v;events.append(('duty',v,state.get(26),state.get(27)))
  def deinit(self):
   duty[0]=0;events.append(('deinit',))
   if fail=='deinit':raise OSError('synthetic deinit')
 def sleep(ms):
  assert ms>=2000;sleepcount[0]+=1;events.append(('sleep',ms,duty[0],state.get(26),state.get(27)))
  if fail=='interrupt' and sleepcount[0]==2:raise KeyboardInterrupt()
 m=types.ModuleType('machine');m.Pin=Pin;m.PWM=PWM;t=types.ModuleType('time');t.sleep_ms=sleep
 out=io.StringIO();namespace={}
 with patch.dict(sys.modules,{'machine':m,'time':t}),patch('builtins.input',side_effect=inputs),contextlib.redirect_stdout(out):
  try:exec(compile(code,'main.py','exec'),namespace)
  except OSError:assert fail=='deinit'
 assert duty[0]==0 and all(v==0 for v in state.values())
 if state:assert events[-3:]==[('low',25),('low',26),('low',27)]
 return events,out.getvalue(),namespace

ev,out,ns=run(['run','q']);assert [v[1:] for v in ev if v[0]=='duty' and v[1]>0]==[(45875,1,0),(58982,1,0),(45875,0,1),(58982,0,1)]
assert [v[2:] for v in ev if v[0]=='sleep']==[(0,0,0),(45875,1,0),(58982,1,0),(0,0,0),(45875,0,1),(58982,0,1),(0,0,0)]
ev,out,_=run(['bad','q']);assert not any(v[0]=='duty' and v[1]>0 for v in ev);assert 'USE run or q' in out
ev,out,_=run([' RUN ','q']);assert out.count('direction =')==4
for changes in [{'LOW_PERCENT = 70':'LOW_PERCENT = -1'},{'HIGH_PERCENT = 90':'HIGH_PERCENT = 101'},{'LOW_PERCENT = 70':'LOW_PERCENT = 90'},{'STOP_MS = 2000':'STOP_MS = 100'},{'RUN_MS = 2000':'RUN_MS = 100'}]:
 ev,out,_=run(['q'],changes);assert not ev and 'MOTOR_ERROR:' in out
for fail in ['init','update','interrupt','deinit']:
 ev,out,_=run(['run','q'],fail=fail)
 if fail in ('init','update'):assert 'MOTOR_ERROR:' in out
 if fail=='interrupt':assert 'STOP:' in out
for val,expectedval in [(0,0),(100,65535),(70,45875),(90,58982)]:assert ns['duty_value'](val)==expectedval
for val in [-1,101,70.0,True,'70']:
 try:ns['duty_value'](val)
 except ValueError:pass
 else:raise AssertionError(val)
assert len(e['cards'])==12;assert e['caption'].count(e['repository'])==1;assert len(e['caption'])<=2200
assert not any(x in e['caption'] for x in ['미시험','미검증','하드웨어 시험 미완료'])
assert all('http' not in c.get('title','')+c.get('lead','')+c.get('note','') for c in e['cards'])
print('PASS15 connections/3 removed jumpers/isolated5V-6V/10kENA/8photo endpoints/AST+README/rounding/range/unknown command/sequence with coast-before-reverse/Ctrl+C/PWM init-update-deinit faults; synthetic host only')
