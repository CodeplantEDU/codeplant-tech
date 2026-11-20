09 · HC-SR04로 거리 읽기 · Pico MicroPython

초음파가 물체까지 다녀오는 시간을 재고 Thonny Shell에 cm로 표시합니다. 10·20·30cm에 넓은 평면 물체를 두고 자의 값과 비교하세요.

USB를 빼고 연결합니다. HC-SR04 VCC는 VBUS(물리 40번)의 USB 5V, TRIG는 GP16(21번), GND는 공통 GND(38번)입니다. Echo는 10kΩ 두 개로 분압하고 두 저항 사이를 GP17(22번)에 연결하세요. 5V Echo를 Pico GPIO에 직접 넣지 마세요. 외부 전원은 추가하지 않습니다.
응답 실패는 NO_READING으로 표시하며 거리 0cm가 아닙니다. 매 회차 뒤 100ms 기다립니다. 이 예제는 3.3V TRIG를 받는 Adafruit #3942 기준입니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/009-hc-sr04

사진: MicroPython 공식 Pico 사진, Adafruit #3942 HC-SR04 공식 사진. 비율 유지·표시 크기 조절. 별도 사진 재배포 허가 표기는 확인되지 않았으며 원권리자 조건이 적용됩니다. 도형: Wokwi(MIT). 상세 출처는 README.

#코드플랜트 #CODEPLANT #RaspberryPiPico #MicroPython #HCSR04 #초음파센서 #분압 #센서실습
