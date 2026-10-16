두 방향의 입력을 읽는 조이스틱 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

손잡이를 기울여 X·Y 값을, 위에서 가볍게 눌러 SW 값을 읽어 봅니다. SunFounder의 GND·+5V·VRX·VRY·SW 5핀 모듈 기준입니다.

준비물: UNO R3, 5핀 조이스틱, 점퍼선 5개, USB 데이터 케이블, 필요하면 브레드보드. USB를 빼고 +5V→5V, GND→UNO 위쪽 GND, VRX→A0, VRY→A1, SW→D2로 연결하세요. 사진과 Wokwi 공통 도형의 핀 배열은 다릅니다. 도형의 VCC=+5V, HORZ=VRX, VERT=VRY, SEL=SW이므로 핀 이름으로 확인합니다.

Arduino IDE에서 전체 코드를 업로드하고 시리얼 모니터를 9600 baud로 엽니다. 추가 라이브러리는 필요 없습니다. x=숫자 y=숫자 sw=숫자가 반복해서 나옵니다. X·Y는 기본 ADC 값 0~1023이며 각도나 거리가 아닙니다. 가운데는 약 512지만 실제 중앙값과 변화 방향은 직접 기록하세요.

D2는 INPUT_PULLUP입니다. SW는 놓으면 1, 누르면 0이며 이 연결에서는 외부 풀업 저항이 필요 없습니다. 이번 코드는 상태 관찰용입니다. 한 번 눌러 한 번 동작시키는 버튼 기능에는 별도 디바운싱이 필요합니다. 이 5V 배선을 ESP32·Pico에 그대로 적용하지 마세요.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/013-joystick
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder 공식 제품 사진(별도 자유 이용 라이선스 미확인). 도형: wokwi-elements(MIT). 출처와 사용 조건은 README에 있습니다.

#코드플랜트 #아두이노 #조이스틱 #아날로그입력 #코딩교육
