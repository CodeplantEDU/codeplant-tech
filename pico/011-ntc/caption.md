11 · 온도에 따라 저항이 바뀌는 NTC · Raspberry Pi Pico

따뜻해지면 NTC 저항이 줄고, 분압 접점 전압과 GP26의 ADC 값도 내려갑니다. 10번 읽은 정수 평균 raw_u16를 비교합니다. 숫자는 섭씨온도나 저항값이 아닙니다.

준비물: RP2040 Raspberry Pi Pico, Adafruit 372 2선 NTC(25°C에서10kΩ ±1%, B25/50=3950 ±1%), 고정10kΩ 저항(1%), 브레드보드·점퍼선·USB 데이터 케이블·Thonny.
USB를 빼고3V3 OUT(물리36)→고정10kΩ→접점→NTC→AGND(물리33)로 연결하고, 접점에 GP26/ADC0(물리31)을 연결하세요. NTC에는 극성이 없지만 두 저항의 위치를 바꾸면 값의 방향이 달라집니다. VBUS·VSYS는 쓰지 않습니다. GP26에5V를 넣지 마세요.

MicroPython v1.29.0 기준 전체 main.py를 F5로 실행하고 READY 뒤 raw_u16를 여러 줄 기록합니다. 센서 끝을 손으로 가볍게 감쌌다가 놓고 변화 방향을 비교하세요. 불·뜨거운 물·침수는 쓰지 않습니다.
Pico는12비트 ADC이며 read_u16()은0~65535로 늘려 반환합니다. 16비트 정확도나 °C를 뜻하지 않습니다. 개별 값에0·65535가 있으면 ADC_ENDPOINT를 표시합니다. USB를 빼고 배선·부품을 확인하세요. 1000ms와10회×10ms 대기에 처리 시간이 더해집니다. Ctrl+C는 STOP, 읽기 오류는 ADC_ERROR로 종료합니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/011-ntc

#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #NTC #서미스터 #ADC #코딩교육
사진: MicroPython 공식 Pico·Adafruit372 공식 사진. 출처를 표시하며 별도의 사진 재배포 허가는 확인되지 않았습니다. 출처와 사용 조건은 README를 확인하세요.