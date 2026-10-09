"""python verify.py: static lesson/net/pin/content checks; no hardware proof."""
import json
import re
from pathlib import Path

p = Path(__file__).parent
d = json.loads((p/'diagram.json').read_text(encoding='utf8'))
e = json.loads((p/'episode.json').read_text(encoding='utf8'))
code = (p/'sketch.ino').read_text(encoding='utf8')
readme = (p/'README.md').read_text(encoding='utf8')
expected = {('uno:9','driver:ENA','yellow'),('uno:8','driver:IN1','blue'),
 ('uno:7','driver:IN2','green'),('uno:5V','driver:5V','red'),
 ('uno:GND.2','driver:GND','black'),('ext6v:VCC','driver:12V','red'),
 ('extgnd:GND','driver:GND','black'),('driver:OUT1','motor:1','orange'),
 ('driver:OUT2','motor:2','purple'),('driver:ENB','driver:GND','black'),
 ('driver:IN3','driver:GND','black'),('driver:IN4','driver:GND','black')}
assert {(a,b,c) for a,b,c,_ in d['connections']} == expected
assert len(d['connections']) == len(expected)
parent = {}
def find(a):
    parent.setdefault(a,a)
    if parent[a] != a: parent[a]=find(parent[a])
    return parent[a]
for a,b,_,_ in d['connections']: parent[find(a)]=find(b)
assert find('uno:GND.2') == find('extgnd:GND') == find('driver:GND')
assert find('uno:5V') != find('ext6v:VCC') != find('driver:GND')
assert find('motor:1') != find('motor:2')
attrs = next(v['attrs'] for v in d['parts'] if v['id']=='driver')
assert all(attrs[k]=='removed' for k in ('5V-EN','ENA-jumper','ENB-jumper'))
assert d['simulationSupported'] is False
for name,pin in [('ENA_PIN',9),('IN1_PIN',8),('IN2_PIN',7)]:
    assert re.search(rf'{name}\s*=\s*{pin};',code)
assert 'Serial.begin(9600)' in code
stop = re.search(r'void stopMotor\(\)\s*\{(.*?)\n\}',code,re.S).group(1)
assert stop.index('analogWrite(ENA_PIN, 0)') < stop.index('delay(STOP_MS)')
loop = re.search(r'void loop\(\)\s*\{(.*?)\n\}',code,re.S).group(1)
assert re.findall(r'(runMotor\([^;]+|stopMotor\(\));',loop) == [
 'runMotor(true, PWM_LOW)','runMotor(true, PWM_HIGH)','stopMotor()',
 'runMotor(false, PWM_LOW)','runMotor(false, PWM_HIGH)','stopMotor()']
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
# Official Wokwi UNO local pin coordinates and the two preview transforms.
uno = {'9':(163,9),'8':(173,9),'7':(189,9),'5V':(160,191.5),'GND.2':(169.5,191.5)}
for pin,x in [('9',879.3),('8',890.3),('7',907.9)]:
    assert abs(700+uno[pin][0]*1.1-x)<.001
assert abs(430+9*1.1-439.9)<.001
assert abs(80+160*1.2-272)<.001 and abs(120+191.5*1.2-349.8)<.001
assert abs(80+169.5*1.2-283.4)<.001
for filename,key in [('circuit_preview.html','powerPaths'),('circuit_preview_control.html','controlPaths')]:
    html=(p/filename).read_text(encoding='utf8')
    for name,color,path in e['circuit'][key]:
        assert f'data-net="{name}"' in html and f'd="{path}"' in html
for pin,left,top,width,preview in [('ENA',100,60,450,'circuit_preview_control.html'),('IN1',100,60,450,'circuit_preview_control.html'),('IN2',100,60,450,'circuit_preview_control.html'),('OUT1',100,60,450,'circuit_preview_control.html'),('OUT2',100,60,450,'circuit_preview_control.html'),('12V',600,70,500,'circuit_preview.html'),('GND',600,70,500,'circuit_preview.html'),('5V',600,70,500,'circuit_preview.html')]:
    x,y=e['circuit']['photoPinCenters'][pin]
    html=(p/preview).read_text(encoding='utf8')
    assert f'cx="{round(left+x*width/851,3)}" cy="{round(top+y*width/851,3)}"' in html
assert e['review']['hardwareTested'] is False
assert e['caption'].count(e['repository'])==1
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5
for src in e['documentationImages']+[c.get('image') for c in e['cards'] if c.get('image')]+[v['src'] for v in e['cards'][0]['photos']]:
    assert (p/Path(src).name).is_file(),src
assert 'circuit_preview_control.html' in (p.parents[1]/'produce.mjs').read_text(encoding='utf8') if (p.parents[1]/'produce.mjs').exists() else True
print('PASS: 12 nets, separate 6V/5V, common GND, three removed jumpers, D9/D8/D7, stop-before-reverse, photo/UNO endpoints, README and caption assets')
