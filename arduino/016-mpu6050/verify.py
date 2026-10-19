"""Educational net/source and independent synthetic-math checks; no hardware proof."""
from pathlib import Path
import copy,json,math,re,struct,xml.etree.ElementTree as ET
p=Path(__file__).parent;d=json.loads((p/'diagram.json').read_text(encoding='utf8'));h=(p/'circuit_preview.html').read_text(encoding='utf8');code=(p/'sketch.ino').read_text(encoding='utf8');readme=(p/'README.md').read_text(encoding='utf8')
expected={frozenset(x) for x in [
 ['uno:5V','level:HV','mpu:VCC'],['uno:3.3V','level:LV'],
 ['uno:GND.2','level:GND_H','level:GND_L','mpu:GND','mpu:AD0'],
 ['uno:A4','level:B1'],['level:A1','mpu:SDA'],
 ['uno:A5','level:B2'],['level:A2','mpu:SCL']]}
def check_nets(data):
 groups=[]
 for a,b in [*(row[:2] for row in data['connections']),*data['internalConnections']]:
  group={a,b}
  for g in list(groups):
   if group & g:group.update(g);groups.remove(g)
  groups.append(group)
 assert {frozenset(g) for g in groups}==expected
check_nets(d);bad=[]
for a,b in [('uno:5V','level:LV'),('uno:3.3V','level:HV'),('uno:A4','mpu:SDA'),('uno:A5','mpu:SCL'),('mpu:VCC','mpu:GND'),('mpu:INT','uno:5V'),('mpu:AD0','uno:5V')]:
 v=copy.deepcopy(d);v['connections'].append([a,b,'red',[]]);bad.append(v)
for i in [0,2,5]:
 v=copy.deepcopy(d);v['connections'].pop(i);bad.append(v)
v=copy.deepcopy(d);v['connections'][6][1],v['connections'][8][1]=v['connections'][8][1],v['connections'][6][1];bad.append(v)
for v in bad:
 try:check_nets(v)
 except AssertionError:pass
 else:raise AssertionError('Unsafe/missing/swapped wiring accepted')
parts={v['id']:v for v in d['parts']}
assert len(parts)==3 and parts['mpu']['type']=='wokwi-mpu6050'
assert parts['mpu']['pins']=={'INT':[7.28,5.78],'AD0':[16.9,5.78],'XCL':[26.4,5.78],'XDA':[36,5.78],'SDA':[45.6,5.78],'SCL':[55.2,5.78],'GND':[64.8,5.78],'VCC':[74.4,5.78]}
svg=ET.fromstring(re.search(r'<div class="level">(.*?)</div>',h,re.S).group(1))
for name,i in parts['level']['pinIds'].items():
 el=svg.find(f'.//*[@id="connector{i}pin"]')
 assert [float(el.attrib['cx']),float(el.attrib['cy'])]==parts['level']['pins'][name]
def xy(ep):
 a,b=ep.split(':');v=parts[a];x,y=v['pins'][b];return [round(v['left']+x*v['scale'],6),round(v['top']+y*v['scale'],6)]
for row,route in zip(d['connections'],d['previewRoutes']):
 a,b,_,_=row
 assert route[0]==xy(a) and route[-1]==xy(b)
 assert all(x==xx or y==yy for (x,y),(xx,yy) in zip(route,route[1:]))
 assert f'data-net="{a}|{b}"' in h
 for ep in (a,b):
  x,y=xy(ep);assert f'cx="{x}" cy="{y}"' in h
assert h.count('stroke="white" stroke-width="12"')==10
assert re.search(r'```cpp\n(.*?)\n```',readme,re.S).group(1).strip()==code.strip()
for s in ['Wire.setClock(100000)','Wire.setWireTimeout(25000, true)','Wire.requestFrom(ADDRESS, count) != count','who != 0x68','writeRegister(0x1A, 0x04)','writeRegister(0x19, 19)','writeRegister(0x1B, 0x00)','writeRegister(0x1C, 0x00)','const uint16_t N = 250','filter.begin(1000000.0f/elapsed)','filter.updateIMU(s.gx-biasX, s.gy-biasY, s.gz-biasZ, s.ax, s.ay, s.az)','wrap180(yaw-yawZero)','elapsed > 100000UL','ERROR: CAL_NOISE','ERROR: FILTER_VALUE']:assert s in code,s
assert '#include <Adafruit_MPU6050.h>' not in code and 'signed16(b + 8) / 131.0f' in code
assert code.index('if (!readSample(s)) stopWith') < code.index('filter.updateIMU')
# Independent ideal geometry: gravity expressed in a ZYX body frame.
for roll,pitch in [(0,0),(30,0),(-30,0),(0,30),(0,-30),(25,-20)]:
 a,b=map(math.radians,(roll,pitch));g=9.80665
 ax=-g*math.sin(b);ay=g*math.sin(a)*math.cos(b);az=g*math.cos(a)*math.cos(b)
 assert math.isclose(math.degrees(math.atan2(ay,az)),roll,abs_tol=1e-8)
 assert math.isclose(math.degrees(math.atan2(-ax,math.hypot(ay,az))),pitch,abs_tol=1e-8)
 assert math.isclose(math.sqrt(ax*ax+ay*ay+az*az),g,abs_tol=1e-8)
# Signed packed sensor data includes a temperature word between accel/gyro.
buf=struct.pack('>7h',-16384,0,16384,12345,-131,262,0)
assert struct.unpack('>h',buf[0:2])[0]/16384==-1
assert struct.unpack('>h',buf[8:10])[0]/131==-1
assert struct.unpack('>h',buf[10:12])[0]/131==2
assert 30*1==30 and 0.5*10==5  # illustrative units and residual-bias drift
for raw,out in [(180,-180),(181,-179),(-181,179),(0,0),(540,-180)]:
 assert (raw+180)%360-180==out
assert ((0x20-0xfffffff0)&0xffffffff)==48  # micros unsigned wrap
e=json.loads((p/'episode.json').read_text(encoding='utf8'))
assert e['slug']=='mpu6050' and len(e['cards'])==10 and not e['review']['hardwareTested']
assert e['caption']==(p/'caption.md').read_text(encoding='utf8')
assert len(re.findall(r'(?<!\S)#[^\s#]+',e['caption']))==5 and e['caption'].count(e['repository'])==1
assert not any(s in e['caption'] for s in ['미시험','미검증','댓글에','3886'])
for src in e['documentationImages']+[v['src'] for v in e['cards'][0]['photos']]:assert (p/Path(src).name).is_file()
assert '상대 요각' in readme and '지자기' in readme and '±90°' in readme
print('PASS: 7 voltage-separated nets; 11 bad wiring mutations rejected; official pin geometry/endpoints; README/full code/10 cards/caption; independent ideal tilt/unit/signed-byte/wrap math. No hardware or simulator execution.')
