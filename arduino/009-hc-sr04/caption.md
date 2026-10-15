초음파로 거리를 재는 HC-SR04 · 아두이노 UNO 버전

댓글에 'git'을 남기면 전체 코드와 연결 방법이 있는 GitHub 링크를 DM으로 보내드려요.

소리가 물체까지 갔다 돌아오는 시간을 거리로 바꿉니다. 이번 편은 classic HC-SR04 5V 모듈과 UNO R3를 사용합니다. 준비물: UNO R3, HC-SR04, 브레드보드, 점퍼선 4개, USB 데이터 케이블, 자와 큰 평평한 반사면.

USB를 빼고 연결하세요. 센서 앞면에서 왼쪽부터 VCC → UNO 5V, Trig → D9, Echo → D10, GND → UNO 위쪽 GND입니다. Trig는 측정을 시작하는 출력, Echo는 돌아온 시간을 읽는 입력입니다. 이 모듈의 Echo는 5V이므로 이 직결 배선을 ESP32·Pico에 그대로 쓰지 않습니다.

Arduino IDE에서 전체 코드를 업로드하고 시리얼 모니터를 9600 baud로 엽니다. 추가 라이브러리는 필요 없습니다. Trig HIGH 10μs → Echo HIGH 시간 읽기 → 시간÷58로 cm 환산 → 다음 회차 전 100ms 대기 순서입니다.

distance_cm=숫자를 벽이나 큰 평평한 판까지 자로 잰 거리와 비교하세요. NO_ECHO는 제한 시간 안에 펄스를 읽지 못한 상태이며 0cm가 아닙니다. OUT_OF_RANGE는 계산 결과가 2~400cm 밖이라는 안내입니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/009-hc-sr04
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). 출처·사진 사용 조건·시간 환산 계수 조정 방법은 저장소 README에 있습니다.

#코드플랜트 #아두이노 #초음파센서 #HCSR04 #코딩교육
