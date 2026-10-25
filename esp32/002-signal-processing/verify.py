import ast, contextlib, copy, io, json, pathlib, runpy, sys, types
from unittest.mock import patch
p = pathlib.Path(__file__).resolve().parent
source = (p / "main.py").read_text(encoding="utf8")
ast.parse(source)
assert "```python\n" + source.rstrip() + "\n```" in (p / "README.md").read_text(encoding="utf8")
def check_diagram(d):
    assert d["version"] == 1 and d["editor"] == "wokwi"
    assert {v["id"]:v["type"] for v in d["parts"]} == {"esp":"wokwi-esp32-devkit-v1", "r":"wokwi-resistor", "led":"wokwi-led"}
    assert next(v for v in d["parts"] if v["id"] == "r")["attrs"]["value"] == "470"
    actual = {(frozenset((a,b)),color) for a,b,color,route in d["connections"]}
    expected = {(frozenset(("esp:D25","r:2")),"yellow"),(frozenset(("r:1","led:A")),"yellow"),(frozenset(("led:C","esp:GND.2")),"black")}
    assert actual == expected and len(d["connections"]) == 3
    assert all(len(v) == 4 for v in d["connections"])
d = json.loads((p / "diagram.json").read_text(encoding="utf8")); check_diagram(d)
for mode in ("gpio", "polarity", "resistance", "extra"):
    bad = copy.deepcopy(d)
    if mode == "gpio": bad["connections"][0][0] = "esp:D34"
    if mode == "polarity": bad["connections"][1][1] = "led:C"
    if mode == "resistance": bad["parts"][1]["attrs"]["value"] = "47"
    if mode == "extra": bad["connections"].append(["esp:VIN","led:A","red",[]])
    try: check_diagram(bad)
    except AssertionError: pass
    else: raise AssertionError("unsafe mutation accepted: " + mode)
def run(inputs):
    events=[]
    class Pin:
        OUT=1
        def __init__(self, number, mode=None, value=None):
            assert number == 25
            self.number=number; events.append(("pin",number,mode,value))
    class PWM:
        def __init__(self, pin, *, freq, duty_u16):
            assert pin.number == 25 and freq == 1000 and duty_u16 == 0
            events.append(("init",freq,duty_u16))
        def duty_u16(self, value):
            assert 0 <= value <= 65535; events.append(("duty",value))
        def deinit(self): events.append(("deinit",))
    machine=types.ModuleType("machine"); machine.Pin=Pin; machine.PWM=PWM
    out=io.StringIO()
    with patch.dict(sys.modules,{"machine":machine}),patch("builtins.input",side_effect=inputs),contextlib.redirect_stdout(out):
        runpy.run_path(str(p / "main.py"),run_name="__main__")
    assert events[-3:] == [("duty",0),("deinit",),("pin",25,1,0)]
    assert out.getvalue().splitlines()[-1] == "STOP"
    return events,out.getvalue()
events,out=run(["0","25","50","75","100","abc"," 50 ","q"])
assert [e[1] for e in events if e[0]=="duty"] == [0,16384,32768,49151,65535,32768,0]
assert out.count("USE:") == 1 and out.count("requested_u16 =") == 6
for inputs in ([KeyboardInterrupt()],[EOFError()],["q"]):run(inputs)
for value,ratio in [(16384,.25),(32768,.5),(49151,.75)]:assert abs(value/65535-ratio)<.00002
print("PASS: syntax, README agreement, exact LED nets + four unsafe mutations; mocked commands/invalid input/q/Ctrl+C/EOF cleanup; PWM ratios. No board/simulator execution.")
