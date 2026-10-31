08 · DHT22로 온도와 습도 읽기 · ESP32 MicroPython

공기의 온도와 습도를 DATA 한 선으로 받아 Thonny Shell에 표시합니다. 외부 10kΩ 풀업 저항이 하는 일과 요청·응답 순서도 함께 살펴보세요.

USB를 빼고 3V3·GND·D4를 연결하세요. 센서 3번 NC는 연결하지 않습니다. 전원과 풀업은 모두 3.3V 기준입니다. 5V·VIN으로 바꾸지 마세요.
시작 후와 매 회차 뒤 2.5초 기다립니다. 온도 °C와 상대습도 %RH를 기록하고 주변 공기에 변화를 준 뒤 비교해 보세요. 센서에 물을 뿌리거나 직접 입김을 불지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/008-dht22

#코드플랜트 #CODEPLANT #코딩교육 #ESP32 #MicroPython #DHT22 #온습도센서 #센서실습
사진: SunFounder ESP32 공식 제품 사진, Adafruit DHT22 제품 385 사진. 표시 크기 조절. 별도 자유 이용 라이선스 미확인, 원권리자 사용 조건 적용. 출처 주소는 위 README에 있습니다.