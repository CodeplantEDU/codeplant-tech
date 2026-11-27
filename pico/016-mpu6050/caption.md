16 · 기울기와 상대 회전을 읽는 MPU6050 · Raspberry Pi Pico

센서를 평평하게 놓고 정지 보정이 끝나면, 한 축씩 천천히 움직여 Thonny Shell의 R·P·Yrel을 기록하세요. 요각은 시작 방향을 기준으로 표시합니다. 자이로의 작은 오차가 쌓이면 시간이 지나며 값이 달라질 수 있습니다.

USB를 빼고 Pico 3V3 OUT을 GY-521 VCC와 BSS138의 HV·LV에 나눠 연결하세요. GND는 공통으로 연결하고 AD0는 GND에 묶습니다. GP4는 B1→A1→SDA, GP5는 B2→A2→SCL 경로를 따릅니다. Pico GPIO에 5V를 넣지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/016-mpu6050

사진은 MicroPython 공식 Pico 배포 페이지와 SunFounder GY-521 제품 자료에서 가져왔습니다. 표지에서 표시 크기를 조정했고 GY-521 사진에 축 안내를 덧붙였습니다. 원권리자의 사용 조건을 따릅니다.

#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #MPU6050 #GY521 #센서실습