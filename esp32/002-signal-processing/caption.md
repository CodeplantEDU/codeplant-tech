CODEPLANT TECH | ESP32 02 · 입력부터 출력까지, 신호처리

Thonny에 보낸 문자 → 코드의 판단 → GPIO25의 PWM → 외부 LED 변화까지 연결해 봅니다. ADC가 전압을 숫자로 바꾸는 입력 과정과 PWM이 HIGH/LOW 비율을 바꾸는 출력 과정을 구분합니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), 빨간 5mm LED 1개(Adafruit #297 기준), 470Ω 저항 1개, 브레드보드·점퍼선·USB 데이터 케이블·Thonny.

USB를 빼고 D25→470Ω→LED A(+), LED C(−)→왼쪽 GND(VIN 바로 위)를 연결하세요. LED 두 다리는 서로 다른 연결 줄에 꽂습니다. 저항을 생략하지 않습니다. GPIO에 5V를 넣지 마세요. 이번 실습에서 GPIO34는 미연결이며 ADC를 읽지 않습니다.

MicroPython v1.29.0 기준 전체 코드를 실행하고 Shell의 duty> 뒤에 0·25·50·75·100 중 하나를 입력한 뒤 Enter를 누르세요. 주파수 요청은 1000Hz로 고정하고 듀티비를 바꿉니다. 25·50·75는 요청값 16384·32768·49151에 대응합니다. 밝기 비율·전압 측정값·회전수가 아닙니다. 다른 입력은 직전 상태를 유지하며 q 또는 Ctrl+C로 종료합니다. LED를 가까이서 똑바로 바라보지 마세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/002-signal-processing
유튜브: https://www.youtube.com/@codeplant2024

사진: SunFounder ESP32·Adafruit #297 공식 제품 사진(별도 자유 이용 라이선스 미확인). Thonny 공식 UI 참고 화면은 README에 구분해 수록합니다. 도형·핀 좌표: Wokwi(MIT). 파형은 CODEPLANT 설명용 이론 그림입니다. 출처·사용 조건은 README를 확인하세요.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #PWM #ADC #신호처리 #코딩교육