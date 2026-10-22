from pathlib import Path
import json,re,copy
p=Path(__file__).resolve().parent
e=json.loads((p/'episode.json').read_text(encoding='utf8')) if (p/'episode.json').exists() else None
d=json.loads((p/'diagram.json').read_text());s=(p/'sketch.ino').read_text();h=(p/'circuit_preview.html').read_text();r=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [('uno:2','ir:OUT'),('uno:GND.2','ir:GND'),('uno:5V','ir:VS')]}
def check(nets):
    assert len(nets)==3 and {frozenset(x) for x in nets}==expected
check(d['connections'])
for i in range(3):
    for j in range(3):
        if i==j:continue
        bad=copy.deepcopy(d['connections']);bad[i][1]=d['connections'][j][1]
        try:check(bad)
        except AssertionError:pass
        else:raise AssertionError('bad wiring accepted')
for pin,xy in d['sourcePinCoordinates'].items():
    part=next(x for x in d['parts'] if x['id']==pin.split(':')[0]);point=[part['left']+xy[0]*part['scale'],part['top']+xy[1]*part['scale']]
    assert all(str(round(v,1)).rstrip('0').rstrip('.') in h for v in point),(pin,point)
assert s.count('IrReceiver.resume();')==1 and 'delay(' not in s and 'return' not in s
assert s.index('IRDATA_FLAGS_WAS_OVERFLOW')<s.index('IRDATA_FLAGS_PARITY_FAILED')<s.index('protocol == UNKNOWN')<s.index('printIRResultShort')<s.index('IrReceiver.resume();')
assert 'IR_RECEIVE_PIN = 2' in s and 'Serial.begin(115200)' in s and 'DISABLE_LED_FEEDBACK' in s
assert '```cpp\n'+s+'```' in r
if e:
    assert len(e['cards'])==10 and len(e['cards'][0]['photos'])==2
    assert '미시험' not in e['caption'] and '미검증' not in e['caption'] and e['repository'] in e['caption']
    for c in e['cards']:
        assert 'http' not in c['title']+c['lead']+c.get('note','')
print('PASS: 3 exact nets; 6 invalid wiring mutations; photo/UNO anchor transforms; decode error guards/resume; README code equality; caption/card source checks. No hardware execution.')
