손잡이로 입력 전압을 바꾸는 가변저항 · ESP32 MicroPython 버전

3핀 10kΩ 선형 가변저항의 양끝에 3.3V와 GND를 연결하면, 손잡이에 따라 가운데 접점의 전압이 바뀝니다. GPIO34의 ADC로 읽고 Thonny Shell에서 숫자를 비교합니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), Adafruit 562 10kΩ 선형 가변저항, 점퍼선 3개·브레드보드·USB 데이터 케이블·Thonny.

USB를 빼고 양끝 한쪽→3V3, 반대쪽→GND(오른쪽 3V3 바로 위), 가운데 접점→D34(GPIO34)를 연결하세요. 세 다리는 서로 다른 연결 줄에 꽂습니다. 5V·VIN은 쓰지 않습니다. 양끝 전원을 바꾸면 증가 방향이 반대가 됩니다.

MicroPython v1.29.0 일반 ESP32 기준 전체 main.py를 실행합니다. READY 뒤 raw_u16 = 숫자가 반복됩니다. read_u16()의 0~65535는 12비트 변환값을 늘린 표현이며 전압·저항·각도가 아닙니다. 16비트 측정 정밀도를 뜻하지 않습니다.

ATTN_11DB의 근사 선형 범위는 약 0.15~2.45V입니다. 회로의 가운데 전압은 이론상 0~3.3V라 일부 구간은 포화될 수 있습니다. 가운데가 꼭 32768이거나 끝에서 정확한 전압을 읽는다고 가정하지 마세요. 끝값에 멈춰도 전원을 높이지 않습니다.

손잡이를 천천히 한쪽 끝·가운데·반대쪽 끝으로 옮겨 멈추고 여러 줄을 기록하세요. 100ms 대기는 정확한 10Hz 타이머가 아닙니다. Ctrl+C로 종료한 뒤 PRINT_MS를 100에서 500으로 바꾸어 표시 간격도 비교해 보세요. 배선 수정은 USB를 빼고 합니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/007-potentiometer
유튜브: https://www.youtube.com/@codeplant2024

사진: SunFounder ESP32·Adafruit 562 공식 제품 자료(별도 자유 이용 라이선스 미확인). 배선 도형: Wokwi(MIT). 신호 흐름도는 CODEPLANT 설명용 그림입니다. 상세 출처·사용 조건은 README를 확인하세요.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #가변저항 #ADC #코딩교육
