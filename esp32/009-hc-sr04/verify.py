"""Synthetic host checks; no sensor, firmware or physical voltage test."""
from pathlib import Path
import ast, contextlib, io, json, sys, types, copy
p=Path(__file__).resolve().parent
source=(p/'main.py').read_text(encoding='utf-8')
ast.parse(source)
d=json.loads((p/'diagram.json').read_text(encoding='utf-8'))
def check_nets(data):
    expected=[('supply:V+','sonar:VCC'),('supply:GND','sonar:GND'),('esp:GND.2','supply:GND'),('esp:D25','sonar:TRIG'),('sonar:ECHO','r1:1'),('r1:2','r2:1'),('r1:2','esp:D26'),('r2:2','supply:GND')]
    assert len(data['connections'])==8
    assert {frozenset(c[:2]) for c in data['connections']}=={frozenset(c) for c in expected}
    parts={x['id']:x for x in data['parts']}
    assert parts['r1']['attrs']['value']=='2200' and parts['r2']['attrs']['value']=='3300'
check_nets(d)
for i,pin in [(4,'esp:D26'),(0,'esp:VIN'),(2,'esp:3V3')]:
    bad=copy.deepcopy(d); bad['connections'][i][0]=pin
    try: check_nets(bad)
    except AssertionError: pass
    else: raise AssertionError('unsafe wiring accepted')
bad=copy.deepcopy(d); bad['parts'][2]['attrs']['value']='3300'
try: check_nets(bad)
except AssertionError: pass
else: raise AssertionError('wrong divider accepted')
preview=(p/'circuit_preview.html').read_text(encoding='utf-8')
for route in d['previewRoutes'].values(): assert 'd="'+route+'"' in preview
assert abs(5*3300/5500-3)<1e-9
low=4.75*(3300*.95)/(2200*1.05+3300*.95)
high=5.25*(3300*1.05)/(2200*.95+3300*1.05)
assert 2.73<low<2.75 and 3.26<high<3.3

def run(events, interrupt_sleep=False):
    log=[]; values={}; frames=iter(events)
    class Pin:
        OUT=1; IN=0
        def __init__(self,n,mode,value=None):
            assert (n,mode) in [(25,1),(26,0)]; self.n=n
            if value is not None: values[n]=value
        def value(self,v): values[self.n]=v; log.append(('pin',self.n,v))
    def sleep_ms(ms):
        assert ms==100; log.append(('ms',ms))
        if interrupt_sleep: raise KeyboardInterrupt
    def sleep_us(us): assert us in [2,10]; log.append(('us',us))
    def pulse(pin,level,timeout):
        assert pin.n==26 and level==1 and timeout==30000
        assert log[-6:]==[('ms',100),('pin',25,0),('us',2),('pin',25,1),('us',10),('pin',25,0)]
        log.append(('pulse',26,1,30000)); event=next(frames)
        if isinstance(event,BaseException): raise event
        return event
    mocks={'machine':types.SimpleNamespace(Pin=Pin,time_pulse_us=pulse),'time':types.SimpleNamespace(sleep_ms=sleep_ms,sleep_us=sleep_us)}
    saved={k:sys.modules.get(k) for k in mocks}; sys.modules.update(mocks)
    out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out): exec(compile(source,str(p/'main.py'),'exec'),{})
    finally:
        for k,v in saved.items():
            if v is None: sys.modules.pop(k,None)
            else: sys.modules[k]=v
    assert values[25]==0 and log[-1]==('pin',25,0)
    return out.getvalue(),log
out,log=run([1160,5800,116,23200,115,23201,-2,-1,0,OSError('timeout'),1160,KeyboardInterrupt()])
assert out.count('distance_cm =')==5 and out.count('OUT_OF_RANGE')==2
assert out.count('NO_ECHO:')==3 and out.count('SENSOR_ERROR:')==1
for text in ['distance_cm = 20.0','distance_cm = 100.0','distance_cm = 2.0','distance_cm = 400.0']: assert text in out
assert out.endswith('STOP\n') and sum(x[0]=='ms' for x in log)==12
out,log=run([],True); assert 'STOP' in out and not any(x[0]=='pulse' for x in log)
assert source in (p/'README.md').read_text(encoding='utf-8')
e=json.loads((p/'episode.json').read_text(encoding='utf-8'))
assert len(e['cards'])==10 and e['repository'].endswith('/esp32/009-hc-sr04')
assert not any(t in e['caption'] for t in ['미시험','미검증','검증 완료','댓글에'])
for card in e['cards']: assert 'http' not in card['title']+card.get('lead','')+card.get('note','')
print('PASS: exact 8 nets; unsafe pin/divider mutations rejected; divider tolerance; code syntax/README parity; synthetic pulse conversion/boundaries/timeout/error recovery/100ms wait/Trig timing/Ctrl+C LOW cleanup. Hardware NOT tested.')
