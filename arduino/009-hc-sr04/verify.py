"""python verify.py: static circuit/code/content checks, not hardware execution."""
from pathlib import Path
import json,re,math,copy
p=Path(__file__).parent
d=json.loads((p/'diagram.json').read_text(encoding='utf8'))
e=json.loads((p/'episode.json').read_text(encoding='utf8')) if (p/'episode.json').exists() else None
html=(p/'circuit_preview.html').read_text(encoding='utf8')
code=(p/'sketch.ino').read_text(encoding='utf8')
readme=(p/'README.md').read_text(encoding='utf8')
def check_nets(diagram):
    groups=[]
    for a,b,_,_ in diagram['connections']:
        merge=[g for g in groups if a in g or b in g];group={a,b}
        for g in merge:group.update(g);groups.remove(g)
        groups.append(group)
    assert {frozenset(g) for g in groups}=={
        frozenset(['uno:5V','sonar:VCC']),frozenset(['uno:GND.1','sonar:GND']),
        frozenset(['uno:9','sonar:TRIG']),frozenset(['uno:10','sonar:ECHO'])},'Power/GND/Trig/Echo net error'
check_nets(d)
for a,b in [('uno:5V','uno:GND.1'),('sonar:TRIG','sonar:ECHO'),('sonar:ECHO','uno:5V')]:
    bad=copy.deepcopy(d);bad['connections'].append([a,b,'yellow',[]])
    try:check_nets(bad)
    except AssertionError:pass
    else:raise AssertionError('Unsafe net mutation was not rejected')
parts={v['id']:v for v in d['parts']};assert len(parts)==2 and len(d['connections'])==4
assert parts['uno']['pins']=={'9':[163,9],'10':[153.5,9],'5V':[160,191.5],'GND.1':[115.5,9]}
assert parts['sonar']['pins']=={'VCC':[71.3,94.5],'TRIG':[81.3,94.5],'ECHO':[91.3,94.5],'GND':[101.3,94.5]}
def xy(endpoint):
    part,pin=endpoint.split(':');v=parts[part]
    return v['left']+v['pins'][pin][0]*v['scale'],v['top']+v['pins'][pin][1]*v['scale']
for a,b,c,_ in d['connections']:
    assert c==('red' if a=='uno:5V' else 'black' if a=='uno:GND.1' else 'yellow')
    route=d['previewRoutes'][a];assert f'data-net="{a}"' in html and f'd="{route}"' in html
    nums=re.findall(r'[-+]?\d+(?:\.\d+)?',route)
    assert all(math.isclose(float(n),v,abs_tol=1e-6) for n,v in zip(nums[:2],xy(a)))
    assert all(math.isclose(n,v,abs_tol=1e-6) for n,v in zip((float(re.findall(r'H([\d.]+)',route)[-1]),float(re.findall(r'V([\d.]+)',route)[-1])),xy(b)))
    for ep in (a,b):
        x,y=xy(ep);assert f'cx="{x:g}" cy="{y:g}"' in html
for line in ['const byte TRIG_PIN = 9;','const byte ECHO_PIN = 10;','const unsigned long ECHO_TIMEOUT_US = 30000UL;','const unsigned long MEASURE_MS = 100;','pinMode(TRIG_PIN, OUTPUT);','pinMode(ECHO_PIN, INPUT);','Serial.begin(9600);','pulseIn(ECHO_PIN, HIGH, ECHO_TIMEOUT_US)']:assert line in code,line
loop=code.split('void loop() {',1)[1]
assert loop.index('delay(MEASURE_MS);')<loop.index('digitalWrite(TRIG_PIN, HIGH);')
assert 'digitalWrite(TRIG_PIN, HIGH);\n  delayMicroseconds(10);\n  digitalWrite(TRIG_PIN, LOW);' in loop
no_echo=re.search(r'if \(echoUs == 0\) \{(.*?)\}',loop,re.S).group(1)
assert 'Serial.println("NO_ECHO");' in no_echo and 'return;' in no_echo
out=re.search(r'if \(cm < MIN_CM \|\| cm > MAX_CM\) \{(.*?)\}',loop,re.S).group(1)
assert 'Serial.println("OUT_OF_RANGE");' in out and 'return;' in out
assert loop.index('float cm = echoUs / US_PER_CM;')>loop.index('return;')
assert loop.index('cm > MAX_CM')<loop.index('Serial.print("distance_cm=")')
coefficient=float(re.search(r'US_PER_CM = ([\d.]+)f',code).group(1));assert coefficient==58.0
assert math.isclose(5800/coefficient,100.0) and math.isclose(23200/coefficient,400.0)
assert 23200<30000 and 'MIN_CM = 2.0f;' in code and 'MAX_CM = 400.0f;' in code
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
assert '| D9 | Trig |' in readme and '| D10 | Echo |' in readme and '| 위쪽 GND | GND |' in readme
caption=(p/'caption.md').read_text(encoding='utf8')
repo='https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/009-hc-sr04'
assert caption.count(repo)==1 and len(caption)<=2200
assert len(re.findall(r'(?<!\S)#[^\s#]+',caption))==5
for name in ['uno-r3-photo.jpg','hc-sr04-photo.jpg','arduino_uno_hcsr04.png','ide-uno-port-screen.png','ide-buttons-screen.png','ide-serial-screen.png']:assert (p/name).is_file(),name
if e is not None:
    assert e['review']['hardwareTested'] is False and e['caption']==caption and e['repository']==repo
    for src in e['documentationImages']+[c['image'] for c in e['cards'] if c.get('image')]+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file(),src
print('PASS: 4 separate nets / 3 unsafe mutations rejected / official UNO-HCSR04 pin endpoints / D9 OUT D10 IN / 10us pulse 100ms wait 30ms timeout / zero and range guards / conversion units / README-caption-photos')
