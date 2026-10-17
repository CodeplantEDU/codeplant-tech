회전 방향을 읽는 로터리 인코더 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

KY-040 계열 5핀 모듈의 손잡이를 천천히 돌리고, 반대로 돌렸을 때 카운트가 어떻게 바뀌는지 비교합니다. CLK·DT는 회전 신호 두 개, SW는 누름 스위치입니다. 표지의 실제 모듈은 SunFounder HW-040입니다.

준비물: UNO R3, CLK·DT·SW·+·GND 5핀 모듈, 점퍼선 5개, USB 데이터 케이블. USB를 빼고 CLK→D2, DT→D3, SW→D4, +/VCC→5V, GND→UNO 위쪽 GND로 연결하세요. 세 신호는 INPUT_PULLUP입니다. 이 5V 연결을 ESP32·Pico에 그대로 적용하지 않습니다.

Arduino IDE에서 RotaryEncoder by Matthias Hertel(1.6.0)을 설치하고 전체 코드를 업로드합니다. 시리얼 모니터는 115200 baud. 시작 안내 뒤 pos=상대카운트 sw=0또는1이 바뀔 때 출력됩니다. pos는 절대 각도나 RPM이 아니며 다시 시작하면 0입니다.

버튼은 50ms 동안 같은 상태가 유지된 뒤 반영합니다. 누르면 sw=0과 내장 L LED 켜짐, 놓으면 sw=1과 꺼짐을 확인하세요. 누름은 카운트를 초기화하지 않습니다. 회전 신호를 놓치지 않도록 loop에서 자주 읽으며 긴 delay를 넣지 않습니다. 실제 증가 방향과 걸림 한 칸당 카운트는 천천히 돌리며 확인하세요.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/014-rotary-encoder
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder 공식 제품 사진(별도 자유 이용 라이선스 미확인). 도형: wokwi-elements(MIT). 출처·사용 조건·FOUR3 설정 점검은 README에 있습니다.

#코드플랜트 #아두이노 #로터리인코더 #디지털입력 #코딩교육
