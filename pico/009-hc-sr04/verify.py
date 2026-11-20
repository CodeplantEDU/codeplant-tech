"""Synthetic host checks only; hardware/firmware untested."""
from pathlib import Path
import ast,copy,contextlib,io,json,runpy,sys,types
p=Path(__file__).resolve().parent
source=(p/"main.py").read_text(encoding="utf-8");ast.parse(source)
d=json.loads((p/"diagram.json").read_text(encoding="utf-8"))
expected={frozenset(e) for e in [("pico:VBUS","sonar:VCC"),("pico:GP16","sonar:TRIG"),("sonar:ECHO","r1:1"),("r1:2","r2:1"),("pico:GP17","r2:1"),("r2:2","pico:GND"),("sonar:GND","r2:2")]}
def check(data):
 assert len(data["connections"])==7 and {frozenset(c[:2]) for c in data["connections"]}==expected
 parts={x["id"]:x for x in data["parts"]}
 assert all(parts[x]["attrs"]["value"]=="10000" for x in ["r1","r2"])
 assert parts["pico"]["physicalPins"]=={"VBUS":40,"GP16":21,"GP17":22,"GND":38}
 assert parts["sonar"]["pins"]=={"VCC":[71.3,94.5],"TRIG":[81.3,94.5],"ECHO":[91.3,94.5],"GND":[101.3,94.5]}
check(d)
for n in range(3):
 bad=copy.deepcopy(d)
 if n==0:bad["connections"][2][1]="pico:GP17"
 elif n==1:bad["connections"][0][0]="pico:3V3"
 else:bad["parts"][2]["attrs"]["value"]="0"
 try:check(bad)
 except AssertionError:pass
 else:raise AssertionError("unsafe mutation accepted")
waits=[];events=[]
class Pin:
 OUT=1;IN=0
 def __init__(self,gp,mode,value=None):self.gp=gp;events.append(("pin",gp,mode,value))
 def value(self,v):events.append((self.gp,v))
pulses=iter([580,1160,-2,-1,0,58,23258,23200])
def pulse(pin,level,timeout):
 assert pin.gp==17 and level==1 and timeout==30000
 events.append(("pulse",))
 try:return next(pulses)
 except StopIteration:raise KeyboardInterrupt
machine=types.ModuleType("machine");machine.Pin=Pin;machine.time_pulse_us=pulse
time=types.ModuleType("time");time.sleep_us=lambda n:events.append(("us",n));time.sleep_ms=lambda n:waits.append(n)
old={k:sys.modules.get(k) for k in ["machine","time"]};sys.modules.update(machine=machine,time=time);out=io.StringIO()
try:
 with contextlib.redirect_stdout(out):runpy.run_path(str(p/"main.py"))
finally:
 for k,v in old.items():
  if v is None:sys.modules.pop(k,None)
  else:sys.modules[k]=v
text=out.getvalue()
assert all(x in text for x in ["distance_cm=10.0","distance_cm=20.0","distance_cm=400.0","STOP"])
assert text.count("NO_READING")==5 and waits==[100]*9 and events[-1]==(16,0)
assert ("pin",16,1,0) in events and ("pin",17,0,None) in events
for i,e in enumerate(events):
 if e==("pulse",):assert events[i-5:i]==[(16,0),("us",2),(16,1),("us",10),(16,0)]
assert source.strip() in (p/"README.md").read_text(encoding="utf-8")
print("PASS: 7 wiring edges, divider mutations, 8 synthetic pulse cases, trigger order, wait intervals, Ctrl+C cleanup, README code match. Hardware untested.")
