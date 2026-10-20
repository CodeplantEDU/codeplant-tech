빛으로 거리를 읽는 VL53L0X 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

VL53L0X는 빛이 물체까지 갔다 돌아오는 시간을 이용해 거리를 구하는 ToF 센서입니다. 센서 앞에 넓고 평평한 종이를 놓고 천천히 움직여 봅니다. 밝기값이 아닌 거리(mm)를 읽습니다.

준비물: UNO R3, Adafruit 제품번호 3317 STEMMA QT, 점퍼선 4개, 연결용 헤더·브레드보드, USB 데이터 케이블, 자와 넓은 종이. USB를 빼고 UNO 5V→VIN, 아래쪽 GND→GND, A4→SDA, A5→SCL을 연결하세요. GPIO·XSHUT와 QT 커넥터는 비워 둡니다. 전압 조정·I²C 신호 변환이 있는 이 모듈 기준이며 다른 모듈에는 전원 조건을 그대로 적용하지 않습니다.

Arduino IDE에서 Adafruit_VL53L0X 1.2.5와 요청되는 의존성을 설치한 뒤 전체 코드를 업로드합니다. 시리얼 모니터는 115200 baud, 센서 한 개의 기본 주소는 0x29입니다. READY 뒤 종이를 광학창 정면의 10·20·30cm에 놓고 distance_mm와 distance_cm를 자 눈금과 비교하세요. 10mm=1cm입니다.

통신 시간 초과·API 오류·유효하지 않은 측정 상태를 먼저 구분합니다. RangeStatus=0일 때만 거리를 출력하며 RANGE_INVALID는 0mm가 아닙니다. 검은 물체·비스듬한 면·주변 빛 때문에 결과가 달라질 수 있으니 같은 자리에서 여러 번 읽어 보세요. 광학창을 가리지 마세요. 매회 측정 시간 외에 250ms 대기를 더합니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/017-vl53l0x
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). 도형: Wokwi(MIT), Adafruit Fritzing/kattni(CC BY-SA 3.0). 배선도와 3번 회로 카드도 CC BY-SA 3.0. 출처와 조건은 README에 있습니다.

#코드플랜트 #아두이노 #VL53L0X #거리센서 #코딩교육
