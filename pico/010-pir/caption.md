10 · 적외선의 변화로 움직임을 감지하는 PIR · Pico MicroPython

SunFounder HC-SR501의 OUT을 GP16 입력으로 읽고, 상태가 바뀔 때만 Thonny Shell에 0·1을 표시합니다. 센서 앞을 가로질러 움직인 뒤 멈추고 HIGH 유지와 LOW 복귀를 기록하세요. H/L 모드와 코드의 50ms 대기도 구분해 봅니다.

USB를 빼고 VBUS(물리 40번)→센서 VCC, GP16(21번)→OUT/DO, GND(38번)→GND를 연결하세요. USB 전원 하나만 쓰고 외부 전원은 추가하지 않습니다. 이 모델은 전원 5V, OUT HIGH 약 3.3V입니다. 다른 모델은 출력 조건부터 확인하고 Pico GPIO에 5V를 넣지 마세요.
시작 후 60초 기다립니다. LOW만으로 사람이 없음을 판단하지 마세요. 조절기·H/L 점퍼·배선을 바꾸기 전 USB를 빼고 열원·직사광·바람을 피합니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/010-pir

사진: MicroPython 공식 Pico 사진, SunFounder HC-SR501 공식 사진. 비율 유지·표시 크기 조절. 별도 사진 재배포 허가 표기는 확인되지 않았으며 원권리자 조건이 적용됩니다. 도형: Wokwi(MIT). 상세 출처는 README.

#코드플랜트 #CODEPLANT #RaspberryPiPico #MicroPython #PIR #HCSR501 #움직임감지 #센서실습
