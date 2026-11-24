13 · 조이스틱의 두 축과 누름 읽기 · Raspberry Pi Pico

두 가변저항의 접점 전압을 GP26·GP27에서 읽고 별도 SW 접점을 GP16으로 확인합니다. Thonny Shell에서 X·Y·pressed/released를 비교하세요.

준비물: RP2040 Pico, SunFounder VRX/VRY/SW 조이스틱(3.3~5V 급전 지원형), 외부10kΩ 저항, 브레드보드·점퍼선·USB 데이터 케이블·Thonny.
USB를 빼고 +5V 표기핀→3V3 OUT(물리36), GND→GND(물리38), VRX→GP26(물리31), VRY→GP27(물리32), SW→GP16(물리21)을 연결하세요. 10kΩ은 SW와3V3 OUT 사이입니다. VBUS·VSYS는 미연결이며 입력에5V를 넣지 않습니다.

전체 main.py를 F5로 실행하고 중앙의 변동 범위, 한 축씩 움직일 때 달라지는 값, 누름 상태를 직접 기록하세요. Pico의12비트 ADC를 read_u16()이0~65535로 늘려 표현하며16비트 정확도·각도·정확한 전압을 뜻하지 않습니다. 중앙값과 방향은 실제 부품·장착 방향에 따라 다릅니다.
SW는 외부 풀업으로 놓으면1, 누르면0입니다. 150ms 대기와 처리 시간이 더해지며 빠른 누름을 놓칠 수 있습니다. 누름 횟수 세기·디바운싱은 구현하지 않습니다. 값이 고정되거나 발열하면 USB를 빼고 연결과 저항을 확인하세요. 값 때문에 전압을 높이지 않습니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/013-joystick

사진: MicroPython 공식 Pico·SunFounder 공식 조이스틱 사진. 출처를 표시하며 별도 사진 재배포 허가는 확인되지 않았습니다. 조건은 README를 확인하세요.
#코드플랜트 #CODEPLANT #RaspberryPiPico #RP2040 #MicroPython #조이스틱 #ADC #코딩교육