14 · 회전 방향을 읽는 로터리 엔코더 · ESP32 MicroPython

손잡이를 돌리면 CLK와 DT가 시간차를 두고 바뀝니다. ESP32는 바뀐 순서로 회전 방향을 구분합니다. Thonny Shell에서 한 방향씩 돌려 pos가 어떻게 바뀌는지 보고, 손잡이를 눌렀다 놓아 sw를 확인하세요.

USB를 빼고 CLK→D18, DT→D19, SW→D21, +→3V3, GND→GND를 연결하세요. 모듈 전원을 5V나 VIN에 연결하지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/014-rotary-encoder

사진: SunFounder 공식 제품 자료(ESP32 DevKit v1, HW-040). 별도 자유 이용 라이선스 미확인, 원권리자 사용 조건 적용. 도형: Wokwi(MIT).

#코드플랜트 #CODEPLANT #코딩교육 #ESP32 #MicroPython #로터리엔코더 #센서실습