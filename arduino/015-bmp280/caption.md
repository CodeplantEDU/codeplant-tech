기압과 온도를 읽는 BMP280 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

BMP280으로 센서의 온도와 그 위치의 기압을 읽습니다. 이번 부품은 5V 전원·신호를 지원하는 Adafruit 제품번호 2651 STEMMA QT입니다. 습도 센서 BME280과 구분하세요.

준비물: UNO R3, 해당 모듈, 점퍼선 4개, 연결용 헤더·브레드보드, USB 데이터 케이블. USB를 빼고 UNO 5V→모듈 VIN, 아래쪽 GND→GND, A4(SDA)→SDI, A5(SCL)→SCK를 연결합니다. 3Vo·SDO·CS는 연결하지 않습니다. UNO VIN과 모듈 VIN을 연결하는 것이 아닙니다. 다른 3.3V 전용 보드에는 그대로 적용하지 마세요.

Arduino IDE에서 Adafruit BMP280 Library(3.0.0), Adafruit Unified Sensor, Adafruit BusIO를 설치하고 전체 코드를 업로드합니다. 시리얼 모니터 9600 baud. 주소는 0x77, 실패하면 0x76을 확인합니다. 두 주소 모두 실패하면 BMP280_NOT_FOUND 오류 후 멈춥니다.

READY 다음 약 1초마다 temp_C=섭씨온도 pressure_hPa=기압을 출력합니다. Pa를 100으로 나누어 hPa로 표시합니다. 센서를 같은 자리에 두고 여러 줄을 비교하세요. 날씨 앱의 해면기압과 바로 같아야 하는 값은 아닙니다. 소수점 자릿수는 정확도 보장이 아닙니다. 물을 묻히거나 압력 구멍을 막지 않습니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/015-bmp280
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). BMP280 도형: Adafruit / kattni, CC BY-SA 3.0. 배선도와 3번 회로 카드도 CC BY-SA 3.0. 출처·조건은 README에 있습니다.

#코드플랜트 #아두이노 #BMP280 #기압센서 #코딩교육
