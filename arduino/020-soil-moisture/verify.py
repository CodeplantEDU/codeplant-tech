from pathlib import Path
import json,copy
p=Path(__file__).resolve().parent;d=json.loads((p/'diagram.json').read_text());s=(p/'sketch.ino').read_text();r=(p/'README.md').read_text(encoding='utf8');h=(p/'circuit_preview.html').read_text()
expected={frozenset(x) for x in [('uno:5V','soil:VCC'),('uno:GND.2','soil:GND'),('uno:A0','soil:Signal')]}
def check(n):assert len(n)==3 and {frozenset(x) for x in n}==expected
check(d['connections'])
for i in range(3):
 for j in range(3):
  if i==j:continue
  bad=copy.deepcopy(d['connections']);bad[i][1]=d['connections'][j][1]
  try:check(bad)
  except AssertionError:pass
  else:raise AssertionError('bad wiring accepted')
for key,(x,y) in d['sensorSourceCoordinates'].items():
 assert d['pins']['soil:'+key]==[650+(x-325)*1.6,round(200+(y-60)*1.6,1)]
for name,(x,y) in d['pins'].items():assert str(x).rstrip('0').rstrip('.') in h and str(y).rstrip('0').rstrip('.') in h
assert 'DRY_RAW = -1' in s and 'WET_RAW = -1' in s and 'DRY_RAW <= WET_RAW' in s and s.index('DRY_RAW <= WET_RAW')<s.index('/ (DRY_RAW - WET_RAW)')
assert 'Q620 533 628 550' in h and d['insulatedBridge']['center']==[620,550]
assert '100L' in s and 'constrain(indexUnclamped, 0L, 100L)' in s and 'OUTSIDE_CAL' in s
assert '```cpp\n'+s+'```' in r
# Synthetic reference cases; these are not sensor measurements.
def calc(raw,dry,wet):
 if not (0<=wet<dry<=1023):return None
 return max(0,min(100,int((dry-raw)*100/(dry-wet))))
assert [calc(x,600,300) for x in [600,450,300,700,200]]==[0,50,100,0,100]
assert all(calc(450,a,b) is None for a,b in [(-1,-1),(300,300),(200,600),(1024,300)])
def state(index,on):return True if index<=30 else False if index>=40 else on
on=False;seen=[]
for x in [35,30,35,39,40,35,0,100]:on=state(x,on);seen.append(on)
assert seen==[False,True,True,True,False,False,True,False]
print('PASS: 3 nets / 6 bad wiring mutations; manufacturer anchors/insulated bridge; calibration guards, synthetic index and hysteresis boundary cases; README full-code match. No hardware test.')
