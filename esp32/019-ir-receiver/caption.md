리모컨 신호를 읽는 적외선 수신기 · ESP32 MicroPython

Vishay TSOP38238의 둥근 렌즈를 정면에 두세요. USB를 빼고 왼쪽 OUT→D18, 가운데 GND→GND, 오른쪽 VS→3V3를 연결합니다. ESP32 입력에 5V를 넣지 마세요.

NEC 8비트 주소 리모컨을 수신기에 향하게 한 뒤, 서로 다른 버튼의 ADDR·CMD를 비교하세요. 길게 눌렀을 때 REPEAT 또는 같은 명령이 이어지는지도 살펴보세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/019-ir-receiver

사진: SunFounder ESP32 및 Adafruit 제품 157 공식 사진. 별도 자유 이용 라이선스는 확인되지 않았으며 원권리자 조건이 적용됩니다. 배선도는 Adafruit 정면 사진에 핀 표기를 추가했습니다. ESP32 도형은 Wokwi(MIT)입니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #적외선 #리모컨 #NEC #센서실습