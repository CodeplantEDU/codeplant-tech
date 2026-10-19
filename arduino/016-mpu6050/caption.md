기울기와 회전을 읽는 MPU6050 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

이번에는 파란색 GY-521 8핀 MPU6050을 사용합니다. 가속도 3축과 각속도 3축을 I²C로 읽고, Madgwick 필터로 롤(X축 회전)·피치(Y축 회전)·요(Z축 회전)를 계산합니다.

UNO A4는 SDA, A5는 SCL입니다. GY-521 VCC와 변환기 HV에는 5V, 변환기 LV에는 3.3V를 연결합니다. BSS138 양방향 변환기의 B1↔A1은 SDA, B2↔A2는 SCL입니다. GND는 함께 연결하고 AD0는 GND로 두어 주소 0x68을 씁니다. XDA·XCL·INT는 이번 실습에서 쓰지 않습니다. 전체 연결표를 보고 USB를 뺀 상태에서 배선하세요.

Wire와 Madgwick 1.2.0으로 전체 코드를 업로드한 뒤 시리얼 모니터를 115200 baud로 엽니다. 부품면이 위로 오도록 평평하게 놓고 CALIBRATING 동안 약 5초간 정지합니다. READY 뒤 한 축씩 천천히 기울이고 돌려 roll_deg, pitch_deg, yaw_rel_deg를 비교하세요.

롤·피치는 중력 방향으로 기울기를 보정합니다. 요는 북쪽이 아닌 시작 방향 기준이며 시간이 지나면 오차가 쌓일 수 있습니다. z를 전송하면 현재 요 방향을 다시 0°로 설정합니다. 피치 ±90° 부근, 급가속·진동에서는 자세각 해석에 주의하세요.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/016-mpu6050
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder 공식 GY-521 제품 사진(별도 자유 이용 라이선스 미확인, 축 안내 추가). 도형: Wokwi(MIT), Adafruit/andydoro Fritzing(CC BY-SA 3.0). 배선도와 회로 카드는 CC BY-SA 3.0. 상세 출처·사용 조건은 README에 있습니다.

#코드플랜트 #아두이노 #MPU6050 #롤피치요 #코딩교육
