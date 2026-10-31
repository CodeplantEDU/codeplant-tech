"""Host-only synthetic tests. No physical sensor or firmware execution."""
from pathlib import Path
import ast, contextlib, io, json, sys, types, copy
p = Path(__file__).resolve().parent
source = (p / "main.py").read_text(encoding="utf-8")
ast.parse(source)
d = json.loads((p / "diagram.json").read_text(encoding="utf-8"))
def check_nets(data):
    edges = {frozenset(c[:2]) for c in data["connections"]}
    expected = {frozenset(e) for e in [("esp:3V3", "dht:VCC"), ("esp:GND.1", "dht:GND"), ("esp:D4", "dht:SDA"), ("r1:1", "dht:SDA"), ("r1:2", "dht:VCC")]}
    assert len(data["connections"]) == 5 and edges == expected
    assert not any("dht:NC" in e for e in edges)
    assert next(x for x in data["parts"] if x["id"] == "r1")["attrs"]["value"] == "10000"
check_nets(d)
for badpin in ["esp:VIN", "esp:D34", "esp:D2"]:
    bad = copy.deepcopy(d)
    bad["connections"][0 if badpin == "esp:VIN" else 2][0] = badpin
    try: check_nets(bad)
    except AssertionError: pass
    else: raise AssertionError("unsafe mutation accepted")
assert d["parts"][0]["pins"] == {"D4": [101.3,120], "3V3": [101.3,158.5], "GND.1": [101.3,149]}
preview = (p / "circuit_preview.html").read_text(encoding="utf-8")
for route in d["previewRoutes"].values(): assert 'd="' + route + '"' in preview
for endpoint in ["442.86 518.7", "442.86 497.8", "442.86 434", "895 V504.7", "923.5 V504.7", "981.4 V504.7", "771.525 570", "771.525 658.2"]: assert endpoint in preview

def run(events, interrupt_sleep=None):
    log = []; sleeps = []; frames = iter(events)
    class Pin:
        def __init__(self, n): assert n == 4
    class Sensor:
        def __init__(self, pin): pass
        def measure(self):
            log.append("measure")
            event = next(frames)
            if isinstance(event, BaseException): raise event
            self.frame = event
        def temperature(self): log.append("temperature"); return self.frame[0]
        def humidity(self): log.append("humidity"); return self.frame[1]
    def sleep(ms):
        assert ms == 2500
        sleeps.append(ms); log.append("sleep")
        if len(sleeps) == interrupt_sleep: raise KeyboardInterrupt
    mocks = {"machine": types.SimpleNamespace(Pin=Pin), "dht": types.SimpleNamespace(DHT22=Sensor), "time": types.SimpleNamespace(sleep_ms=sleep)}
    saved = {k: sys.modules.get(k) for k in mocks}; sys.modules.update(mocks)
    out = io.StringIO()
    try:
        with contextlib.redirect_stdout(out): exec(compile(source, str(p/"main.py"), "exec"), {})
    finally:
        for k,v in saved.items():
            if v is None: sys.modules.pop(k,None)
            else: sys.modules[k]=v
    return out.getvalue(), log, sleeps
out,log,sleeps = run([(23.4,56.7),(-2.5,40.0),KeyboardInterrupt()])
assert "T = 23.4 C, RH = 56.7 %" in out and "T = -2.5 C, RH = 40.0 %" in out and out.endswith("STOP\n")
assert log == ["sleep","measure","temperature","humidity","sleep","measure","temperature","humidity","sleep","measure"]
assert len(sleeps)==3
out,log,sleeps=run([OSError("timeout"),(20.0,50.0),KeyboardInterrupt()])
assert out.count("DHT_ERROR:")==1 and out.count("T =")==1
assert log[:4]==["sleep","measure","sleep","measure"]
out,log,sleeps=run([],interrupt_sleep=1)
assert "STOP" in out and "measure" not in log
readme=(p/"README.md").read_text(encoding="utf-8")
assert source in readme
cards=json.loads((p/"episode.json").read_text(encoding="utf-8"))
assert cards["category"]=="other-sensors" and len(cards["cards"])==10
assert cards["repository"].endswith("/esp32/008-dht22")
assert not any(t in cards["caption"] for t in ["미시험", "미검증", "검증 완료", "댓글에"])
assert all("http" not in c["title"]+c["lead"]+c.get("note","") for c in cards["cards"])
print("PASS: syntax, 5 exact connections, unsafe mutations, 8 endpoint coordinates, README parity, GPIO4, synthetic readings/order/2500ms/error recovery/Ctrl+C. Hardware NOT tested.")
