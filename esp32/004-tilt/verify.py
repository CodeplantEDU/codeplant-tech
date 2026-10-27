"""Host replacement-object checks. No actual ESP32 execution."""
import ast,contextlib,io,json,pathlib,re,runpy,sys,types,xml.etree.ElementTree as ET
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf8'); ast.parse(source)
assert '```python\n'+source.rstrip()+'\n```' in (p/'README.md').read_text(encoding='utf8')
d=json.loads((p/'diagram.json').read_text(encoding='utf8'));parts={v['id']:v for v in d['parts']};html=(p/'circuit_preview.html').read_text(encoding='utf8')
assert [(a,b,c) for a,b,c,_ in d['connections']]==[('esp:D27','tilt:2','yellow'),('esp:GND.2','tilt:1','black')]
assert parts['esp']['pins']=={'D27':[5,110.8],'GND.2':[5,149]}
svg=ET.fromstring(re.search(r'<svg class="sensor".*?</svg>',html,re.S).group())
for key in ('1','2'):
 leg=svg.find(".//*[@id='connector"+str(int(key)-1)+"leg']");assert parts['tilt']['pins'][key]==[float(leg.get('x2')),float(leg.get('y2'))]
for a,b,color,pts in d['connections']:
 for ep,point in ((a,pts[0]),(b,pts[-1])):
  partid,pin=ep.split(':');v=parts[partid];x,y=v['pins'][pin]
  if v.get('rotate')==-90:x,y=y,30-x
  expected=[v['left']+x*v['scale'],v['top']+y*v['scale']];assert all(abs(i-j)<.001 for i,j in zip(expected,point))
 assert ' '.join(f'{x},{y}' for x,y in pts) in html
assert not (p/'sketch.ino').exists()

def run(samples,start=0):
 clock=[start]; count=[0]; events=[]; samples=iter(samples);last=[None]
 class Pin:
  IN=0;PULL_UP=1
  def __init__(self,n,mode,pull):assert(n,mode,pull)==(27,0,1)
  def value(self):
   if count[0]==0:
    count[0]+=1;last[0]=next(samples)
    if isinstance(last[0],BaseException):raise last[0]
    return last[0]
   v=next(samples)
   if isinstance(v,BaseException):raise v
   assert v in (0,1);count[0]+=1;return v
 m=types.ModuleType('machine');m.Pin=Pin
 t=types.ModuleType('time');t.ticks_ms=lambda:clock[0]%1024;t.ticks_diff=lambda a,b:((a-b+512)%1024)-512
 def sleep(n):assert n==5;events.append(('sleep',n));clock[0]+=n
 t.sleep_ms=sleep
 lines=[]
 def print_at(*args):lines.append((clock[0],' '.join(map(str,args))))
 with patch.dict(sys.modules,{'machine':m,'time':t}),patch('builtins.print',print_at):runpy.run_path(str(p/'main.py'),run_name='__main__')
 return lines,events

def states(o):return [(t,v) for t,v in o if v.startswith('state =')]
# Initial state also waits 50ms, then holds quietly.
o,ev=run([1]+[1]*101+[KeyboardInterrupt()]);assert states(o)==[(50,'state = 1 contact = OPEN')];assert o[-1][1]=='STOP'
o,_=run([0]+[0]*11+[KeyboardInterrupt()]);assert states(o)==[(50,'state = 0 contact = CLOSED')]
# 45ms does not pass the 50ms boundary.
o,_=run([1]+[1]*10+[KeyboardInterrupt()]);assert states(o)==[]
# Raw starts changing at 60,65,70ms; final 0 accepts at 120ms.
values=[1]+[1]*12+[0,1]+[0]*11+[KeyboardInterrupt()]
o,_=run(values);assert states(o)==[(50,'state = 1 contact = OPEN'),(120,'state = 0 contact = CLOSED')],o
# Tick counter rolls at 1024; comparison remains correct.
o,_=run([0]+[0]*11+[KeyboardInterrupt()],1000);assert states(o)==[(1050,'state = 0 contact = CLOSED')]
# A long stable hold is not reprinted after tick wrap; a new change restarts its own clock.
o,_=run([1]+[1]*300+[0]*11+[KeyboardInterrupt()]);assert states(o)==[(50,'state = 1 contact = OPEN'),(1550,'state = 0 contact = CLOSED')],o
# Short change rejected, then return to prior stable state emits nothing.
o,_=run([1]+[1]*12+[0]*9+[1]*12+[KeyboardInterrupt()]);assert len(states(o))==1
for samples in ([1,OSError('synthetic')],[OSError('synthetic')],[1,KeyboardInterrupt()]):
 o,_=run(samples);assert not states(o);assert o[-1][1].startswith(('PIN_ERROR:','STOP'))
e=json.loads((p/'episode.json').read_text(encoding='utf8')); assert e['caption'].count(e['repository'])==1;assert len(e['cards'])==10
assert '미시험' not in e['caption'] and '미검증' not in e['caption'];assert all('http' not in c.get('title','')+c.get('lead','')+c.get('note','') for c in e['cards'])
print('PASS exact2 nets/rotated SVG4 endpoints/README full code/Pin27 IN PULL_UP/startup50ms/45-50 boundary/bounce reset/no repeat/short pulse reject/tick wrap and long hold/Ctrl+C/read error; host synthetic only.')
