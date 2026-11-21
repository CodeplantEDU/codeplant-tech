"""Host synthetic checks only; no physical sensor or firmware execution."""
from pathlib import Path
import ast,copy,json,re,types,sys,io,contextlib,runpy
p=Path(__file__).resolve().parent
src=(p/"main.py").read_text(encoding="utf-8");ast.parse(src)
d=json.loads((p/"diagram.json").read_text(encoding="utf-8"))
expected={frozenset(x) for x in [("pico:VBUS","pir:VCC"),("pico:GP16","pir:OUT"),("pico:GND","pir:GND")]}
def wiring(data):
 assert len(data["connections"])==3 and {frozenset(c[:2]) for c in data["connections"]}==expected
 assert data["parts"][0]["physicalPins"]=={"VBUS":40,"GP16":21,"GND":38}
 assert data["parts"][1]["pins"]=={"VCC":[36.178,92],"OUT":[45.9175,92],"GND":[55.6415,92]}
wiring(d)
for endpoint in ["pico:3V3","pico:GP17"]:
 bad=copy.deepcopy(d);bad["connections"][0 if endpoint.endswith("3V3") else 1][0]=endpoint
 try:wiring(bad)
 except AssertionError:pass
 else:raise AssertionError("wrong board pin accepted")
html=(p/"circuit_preview.html").read_text(encoding="utf-8")
for key,route in d["previewRoutes"].items():assert f'data-net="{key}" d="{route}"' in html
for key,pin in [("pico:VBUS","VCC"),("pico:GP16","OUT"),("pico:GND","GND")]:
 xy=d["parts"][1]["pins"][pin];end=[720+3.2*xy[0],120+3.2*xy[1]]
 nums=[float(x) for x in re.findall(r"[0-9.]+",d["previewRoutes"][key])]
 assert abs(nums[-2]-end[0])<0.01 and abs(nums[-1]-end[1])<0.01
# Three final route endpoints at the official sensor pinInfo coordinates.
def scenario(states,stop_warmup=False,read_error=False):
 waits=[];reads=[];vals=iter(states)
 class Pin:
  IN=0
  def __init__(self,gp,mode,pull):assert (gp,mode,pull)==(16,0,None)
  def value(self):
   assert waits and waits[0]==60000
   if read_error:raise OSError("synthetic disconnected input")
   try:v=next(vals)
   except StopIteration:raise KeyboardInterrupt
   reads.append(v);return v
 def sleep_ms(n):
  waits.append(n)
  if stop_warmup and n==60000:raise KeyboardInterrupt
 machine=types.ModuleType("machine");machine.Pin=Pin
 time=types.ModuleType("time");time.sleep_ms=sleep_ms
 old={k:sys.modules.get(k) for k in ["machine","time"]};sys.modules.update(machine=machine,time=time);out=io.StringIO();error=None
 try:
  with contextlib.redirect_stdout(out):runpy.run_path(str(p/"main.py"))
 except OSError as e:error=e
 finally:
  for k,v in old.items():
   if v is None:sys.modules.pop(k,None)
   else:sys.modules[k]=v
 return out.getvalue(),waits,reads,error
a,w,r,error=scenario([0,0,1,1,0]);assert error is None and r==[0,0,1,1,0]
assert a.count("pir = 0, level = LOW")==2 and a.count("pir = 1, level = HIGH")==1 and "STOP" in a
assert w==[60000]+[50]*5
for values in [[0,0,0],[1,1,1],[]]:
 a,w,r,error=scenario(values);assert a.count("pir =")==bool(values) and w==[60000]+[50]*len(values)
a,w,r,error=scenario([1],True);assert "STOP" in a and "READY" not in a and not r and w==[60000]
a,w,r,error=scenario([],read_error=True);assert isinstance(error,OSError) and "STOP" not in a
assert src.strip() in (p/"README.md").read_text(encoding="utf-8")
e=json.loads((p/"episode.json").read_text(encoding="utf-8"));assert len(e["cards"])==10
assert not any(x in json.dumps(e["cards"],ensure_ascii=False) for x in ["ESP32","GPIO27","D27","두 전원","외부 5V"])
print("PASS: 3 wiring nets and official endpoints, unsafe pin mutations, initial/changed-only values, unchanged values, 60s warmup, 50ms waits, Ctrl+C during warmup/read, propagated GPIO error, README code match. Hardware untested.")
