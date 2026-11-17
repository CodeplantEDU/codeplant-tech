펄스 폭으로 위치를 명령하는 서보모터 · Raspberry Pi Pico MicroPython

GP18(물리 24번)의 펄스를 SN74AHCT125N 버퍼를 거쳐 SG90 Digital 위치 제어형에 보냅니다. Pico는 USB로, 서보와 버퍼는 외부 정전압 5V로 공급하고 GND를 공유하세요. 외부 +5V를 Pico에 연결하지 마세요. 배선할 때 양쪽 전원을 분리하고 서보 팔이 움직일 공간을 비우세요.

50 Hz에서 1500 µs로 시작해 팔 위치를 살펴보세요. 이상이 없으면 1400 µs와 1600 µs도 비교해 보세요. 실제 위치는 제품과 팔의 장착 방향에 따라 달라집니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/005-servo-motor

사진: MicroPython 공식 Pico 보드 페이지, TowerPro SG90 Digital 제품 페이지. 표시 크기 조절. 별도 재사용 허가 표기는 확인되지 않았으며 원권리자 조건이 적용됩니다. 서보 도형: Wokwi(MIT).

#코드플랜트 #CODEPLANT #라즈베리파이피코 #MicroPython #서보모터 #SG90 #PWM
