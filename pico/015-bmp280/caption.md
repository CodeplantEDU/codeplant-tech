15 · 공기의 압력과 온도를 읽는 BMP280 · Raspberry Pi Pico

BMP280에서 온도와 기압 원시값을 읽고, 센서의 보정 계수를 적용해 Thonny Shell에 °C와 hPa를 표시합니다. 같은 자리에서 기압을 여러 번 적어 변동 폭을 확인해 보세요.

USB를 뺀 상태에서 Pico 3V3 OUT→VIN, GND→GND, GP4→SDI, GP5→SCK를 연결하세요. Adafruit #2651 STEMMA QT 핀 헤더 기준이며 3Vo·SDO·CS와 QT 커넥터는 비워 둡니다. Pico 신호 핀에 5V를 넣지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/015-bmp280

사진은 MicroPython 공식 Pico 배포 페이지와 Adafruit #2651 제품 페이지에서 가져왔습니다. 표시 크기를 조정했으며 원권리자의 사용 조건을 따릅니다.

#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #BMP280 #기압센서 #센서실습