12 · 온도를 디지털로 읽는 DS18B20 · Raspberry Pi Pico

TO-92 센서 몸체의 온도 변화가 디지털 값이 되어 GP16의 1-Wire 데이터선으로 돌아옵니다. 변환 요청 뒤750ms를 기다려 섭씨를 읽습니다.

준비물: RP2040 Pico, DS18B20 TO-92 한 개, 4.7kΩ 저항, 브레드보드·점퍼선·USB 데이터 케이블·Thonny.
USB를 빼고 평평한 앞면·다리 아래 기준 왼쪽1 GND→Pico GND(물리38), 가운데2 DQ→GP16(물리21), 오른쪽3 VDD→3V3 OUT(물리36)을 연결합니다. DQ와3V3 OUT 사이에4.7kΩ 풀업을 넣으세요. VBUS·VSYS는 쓰지 않으며 GP16에5V를 넣지 않습니다. 기생 전원 대신 VDD로 공급합니다. 방수 프로브·모듈은 제품별 핀표를 확인하세요.

Thonny에서 MicroPython (Raspberry Pi Pico)와 실제 COM 포트를 선택하고 전체 main.py를 F5로 실행하세요. 0x28 계열 한 개일 때만 표시합니다. 손으로 감싸기 전·후·손을 뗀 뒤 값을 여러 줄 기록합니다. 센서 반응 시간을 고려하고 불·뜨거운 물·침수는 쓰지 마세요.
두 자리 표시는0.01°C 정확도를 뜻하지 않습니다. 12비트 간격은0.0625°C이며 제조사 ±0.5°C는-10~85°C 조건입니다. 750ms와1000ms 대기·통신 시간이 더해집니다. Ctrl+C는 STOP입니다. 센서 수·1-Wire 오류가 반복되면 USB를 빼고 연결·풀업을 확인하세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/012-ds18b20

사진: MicroPython 공식 Pico·Adafruit374 공식 사진. 별도 재배포 허가는 확인되지 않았으며 원권리자 조건을 따릅니다. DS18B20 도형: Wokwi boards / Ariella Eliassaf, 별도 이용 조건 미확인. 출처는 README를 확인하세요.
#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #DS18B20 #온도센서 #코딩교육