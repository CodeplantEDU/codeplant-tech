조이스틱의 두 축과 누름 읽기 · ESP32 MicroPython 버전

USB를 빼고 VRX→D34, VRY→D35, SW→D18, GND→GND를 연결하세요. SunFounder 모듈의 +5V 표기 핀에는 ESP32의 3V3를 공급합니다. ESP32 입력에 5V를 넣지 마세요.

Thonny Shell에서 한 축씩 움직여 X·Y 숫자를 비교하고, 누르고 떼면서 SW 표시가 바뀌는지 확인해 보세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/013-joystick

사진: SunFounder 공식 제품 자료. 별도 재배포 허락은 확인되지 않았습니다. 배선 도형: Wokwi(MIT).

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #조이스틱 #ADC #코딩교육