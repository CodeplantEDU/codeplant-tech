import ast, contextlib, io, json, pathlib, runpy, sys, types
from unittest.mock import patch
p=pathlib.Path(__file__).resolve().parent
source=(p/"main.py").read_text(encoding="utf8");ast.parse(source)
assert "```python\n"+source.rstrip()+"\n```" in (p/"README.md").read_text(encoding="utf8")
d=json.loads((p/"diagram.json").read_text(encoding="utf8"))
assert len(d["connections"])==3
assert {(a,b,c) for a,b,c,_ in d["connections"]}=={("esp:3V3","cds:VCC","red"),("esp:GND.1","cds:GND","black"),("esp:D34","cds:AO","yellow")}
def run(values):
    events=[]; values=iter(values)
    class Pin:
        def __init__(self,n):assert n==34; self.number=n
    class ADC:
        ATTN_11DB=11; WIDTH_12BIT=12
        def __init__(self,pin,*,atten):assert pin.number==34 and atten==11
        def width(self,bits):assert bits==12;events.append(("width",bits))
        def read_u16(self):
            v=next(values)
            if isinstance(v,BaseException):raise v
            assert 0<=v<=65535;events.append(("read",v));return v
        def deinit(self):events.append(("deinit",))
    m=types.ModuleType("machine");m.Pin=Pin;m.ADC=ADC
    t=types.ModuleType("time");t.sleep_ms=lambda n:events.append(("sleep",n))
    out=io.StringIO()
    with patch.dict(sys.modules,{"machine":m,"time":t}),contextlib.redirect_stdout(out):runpy.run_path(str(p/"main.py"),run_name="__main__")
    assert events[-1]==("deinit",)
    return events,out.getvalue().splitlines()
values=[0]*8+[32767]*8+[32768]*8+[65535]*8+[1,2,3,4,5,6,7,8]+[KeyboardInterrupt()]
e,o=run(values)
assert o[1:]==["raw_u16 = 0 band = BELOW","raw_u16 = 32767 band = BELOW","raw_u16 = 32768 band = AT_OR_ABOVE","raw_u16 = 65535 band = AT_OR_ABOVE","raw_u16 = 4 band = BELOW","STOP"]
assert [v for k,*rest in e if k=="sleep" for v in rest]==[25]*40
for values in ([OSError("synthetic")],[123,OSError("synthetic")]):
 e,o=run(values);assert o[-1]=="ADC_ERROR: synthetic";assert not any(x.startswith("raw_u16") for x in o)
e,o=run([KeyboardInterrupt()]);assert o[-1]=="STOP"
print("PASS: exact3 nets; host syntax/README/8-sample integer mean/32767-32768 boundary/25ms requests/interrupt/error cleanup. Synthetic samples only; no board execution.")
