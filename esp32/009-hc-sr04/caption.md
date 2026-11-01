09 · HC-SR04로 초음파 거리 읽기 · ESP32 MicroPython

Trig로 요청한 뒤 Echo의 HIGH 시간을 읽고 cm로 계산합니다. Echo의 5V 신호는 2.2kΩ·3.3kΩ 저항으로 분압해 GPIO26으로 보냅니다. 전압을 낮추는 일과 왕복 시간을 거리로 바꾸는 일을 구분해 보세요.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), 5V HC-SR04(Adafruit 3942 기준), 외부 정전압 5V ±5%, 2.2kΩ·3.3kΩ 저항 각1개(±5% 이하), 브레드보드·점퍼선·USB 데이터 케이블·Thonny.
두 전원을 끄고 VCC→외부5V, Trig→D25, Echo→R1→분압 접점→D26, R2→GND를 연결하세요. 센서·외부전원·ESP32 GND는 공통입니다. 외부 +5V를 ESP32 VIN·3V3에 연결하지 말고 Echo를 GPIO에 직결하지 마세요.

전체 코드를 실행하고 큰 평평한 물체를 20·40·60cm 등으로 옮겨 자의 거리와 출력을 비교하세요. 1160µs→20cm는 계산 예시입니다. NO_ECHO는 0cm가 아니며 배선과 반사 조건을 점검합니다. 매 회차 먼저100ms 대기, Ctrl+C로 종료합니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/009-hc-sr04

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #HCSR04 #초음파센서 #분압 #코딩교육
사진: SunFounder ESP32 공식 제품 사진, Adafruit 제품3942 HC-SR04 공식 사진. 표시 크기 조절. 별도 자유 이용·재배포 허가 미확인, 원권리자 사용 조건 적용. Wokwi 부품 도형 MIT. 상세 출처와 사용 조건은 위 README를 확인하세요.