08 · DHT22로 온도와 습도 읽기 · Pico MicroPython

공기의 온도와 습도를 DATA 한 선으로 받아 Thonny Shell에 표시합니다. 외부 10kΩ 풀업 저항이 하는 일과 요청·응답 순서도 함께 살펴보세요.

USB를 빼고 Pico 3V3(OUT, 물리 36번)→센서 1번 VCC, GP16(21번)→2번 DATA, GND(38번)→4번 GND를 연결하세요. DATA와 3V3 사이에는 10kΩ 저항을 넣고 센서 3번 NC는 비워 둡니다. VBUS·VSYS·5V는 연결하지 마세요.
시작 후와 매 회차 뒤 2.5초 기다립니다. 온도 °C와 상대습도 %RH를 여러 줄 기록하고 주변 공기에 변화를 준 뒤 비교하세요. 센서에 물을 뿌리거나 직접 입김을 불지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/008-dht22

사진: Raspberry Pi Foundation / MicroPython 공식 Pico 사진, Adafruit 제품 385 DHT22 사진. 비율 유지·표시 크기 조절. 별도 재배포 허가 표기는 확인되지 않았으며 원권리자 조건이 적용됩니다. 도형: Wokwi(MIT). 상세 출처는 README에 있습니다.

#코드플랜트 #CODEPLANT #RaspberryPiPico #MicroPython #DHT22 #온습도센서 #센서실습
