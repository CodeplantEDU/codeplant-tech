14 · 회전 방향을 읽는 로터리 인코더 · Raspberry Pi Pico

손잡이를 돌리면 CLK와 DT가 시간차를 두고 바뀝니다. Thonny Shell에서 한 방향씩 천천히 돌려 pos가 어떻게 달라지는지 기록하고, 손잡이를 눌렀다 놓아 sw가 0과 1로 바뀌는지 확인하세요.

USB를 빼고 CLK→GP18, DT→GP19, SW→GP20, +→3V3 OUT, GND→GND를 연결하세요. VBUS·VSYS는 비워 두고 Pico 입력과 모듈 +에는 5V를 넣지 마세요. pos는 상대 카운트입니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/014-rotary-encoder

사진은 MicroPython 공식 Pico 배포 페이지와 SunFounder HW-040 제품 자료에서 가져왔습니다. 표시 크기를 조정했으며 원권리자의 사용 조건을 따릅니다.

#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #로터리인코더 #센서실습