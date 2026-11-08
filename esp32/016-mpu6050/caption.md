16 · 기울기와 회전의 변화를 읽는 MPU6050 · ESP32 MicroPython

USB를 빼고 SunFounder GY-521의 VCC→3V3, GND→GND, SDA→D21, SCL→D22, AD0→GND를 연결하세요. INT·XDA·XCL은 비워 둡니다. 다른 모듈은 전원 사양을 먼저 확인하고 ESP32 GPIO에 5V를 넣지 마세요.

Thonny에서 실행하고 가만히 놓기, 천천히 기울이기, 한 축으로 돌리기를 비교하세요. 가속도는 g, 회전 속도는 °/s로 표시합니다. 정지 상태에서도 중력의 영향과 자이로의 오차가 남을 수 있어 여러 줄을 기록해 살펴봅니다. Ctrl+C로 멈춥니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/016-mpu6050

사진: SunFounder ESP32 및 GY-521 공식 제품 사진. 표시 크기 조절. 별도 자유 이용 라이선스 미확인으로 원권리자 사용 조건 적용. 도형: Wokwi(MIT). 상세 출처는 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #MPU6050 #가속도센서 #자이로 #코딩교육