03 · 빛의 변화를 읽는 조도센서 · Pico MicroPython

USB를 빼고 SunFounder 조도 모듈의 VCC→3V3(OUT), GND→AGND, AO→GP26을 연결하세요. DO는 비워 두고 Pico 입력에 5 V를 넣지 마세요. Thonny에서 코드를 실행한 뒤 센서를 가리기 전과 후의 AO raw 숫자를 비교해 보세요. 핀은 만지지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/003-cds-ao

Pico 사진: MicroPython 공식 배포 페이지. 조도 모듈 사진: SunFounder 공식 자료. 표시 크기를 조정했으며 별도 재배포 라이선스는 확인되지 않았습니다.

#코드플랜트 #CODEPLANT #코딩교육 #아날로그센서 #조도센서 #RaspberryPiPico #MicroPython #ADC