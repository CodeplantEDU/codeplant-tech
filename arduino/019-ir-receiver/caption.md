리모컨의 빛 신호를 IR 수신기로 읽기 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

38kHz 반송파와 수신기의 HIGH/LOW 펄스, 라이브러리가 해석한 버튼 명령을 구분합니다. 리모컨의 빛 묶음 → 전기 펄스 → 프로토콜 해석 → 시리얼 표시 순서로 살펴보세요.

준비물: UNO R3, TSOP38238(Adafruit 157), 호환 38kHz IR 리모컨, 브레드보드, 점퍼선 3개, USB 데이터 케이블.
USB를 빼고 둥근 렌즈가 보이는 앞면 기준 왼쪽 OUT(1)→D2, 가운데 GND(2)→GND, 오른쪽 VS(3)→5V를 연결합니다. 다른 제품의 핀 순서를 그대로 쓰지 마세요.

Arduino IDE에서 IRremote 4.7.1을 설치하고 전체 코드를 업로드합니다. 시리얼 모니터는 115200 baud. IR_READY 뒤 같은 버튼·다른 버튼·길게 누르기를 비교하고 Protocol·Address·Command를 직접 기록하세요. Command는 단위 없는 명령 번호이며 회전수·거리·밝기가 아닙니다. UNKNOWN·OVERFLOW·PARITY_ERROR가 나오면 방향·배선·주변 빛을 확인합니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/019-ir-receiver
유튜브: https://www.youtube.com/@codeplant2024

사진: UNO SparkFun(CC BY 2.0), TSOP38238 Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). UNO 도형 Wokwi(MIT). 사진·도형 출처와 사용 조건은 README를 확인하세요.

#코드플랜트 #CODEPLANT #아두이노 #적외선 #IR수신기 #TSOP38238 #리모컨 #코딩교육
