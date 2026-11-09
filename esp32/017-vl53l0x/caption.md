17 · 빛의 왕복으로 거리를 읽는 VL53L0X · ESP32 MicroPython

USB를 빼고 Adafruit #3317의 VIN→3V3, GND→GND, SDA→D21, SCL→D22를 연결하세요. GPIO·XSHUT는 비워 둡니다. README의 고정 버전 드라이버를 ESP32의 vl53l0x.py로 저장하고 main.py를 실행합니다.

큰 평평한 물체를 100·300·500mm 등으로 옮기며 자의 거리와 Shell 출력을 비교하세요. 실습 코드의 50~1000mm 범위 밖이면 CHECK_TARGET이 나옵니다. 물체의 색·기울기·주변 빛에 따라 결과가 달라질 수 있습니다. 센서 창을 가리거나 개조하지 마세요. 오류가 나면 전원을 끄고 연결을 확인하세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/017-vl53l0x

사진: SunFounder ESP32 및 Adafruit #3317 공식 제품 사진. 표시 크기 조절, 별도 자유 이용 라이선스 미확인으로 원권리자 사용 조건 적용. 센서 도형: Adafruit Fritzing / kattni(CC BY-SA 3.0). 파생 회로·HTML·3번 회로 카드도 CC BY-SA 3.0. Wokwi 보드 MIT. 상세 출처는 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #VL53L0X #ToF #거리센서 #코딩교육