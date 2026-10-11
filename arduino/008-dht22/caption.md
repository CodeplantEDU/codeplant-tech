온도와 습도를 읽는 DHT22 · 아두이노 UNO 버전

댓글에 'git'을 남기면 전체 코드와 연결 방법이 있는 GitHub 링크를 DM으로 보내드려요.

방 안의 온도와 상대습도를 한 센서로 읽어 봅니다. DHT22 4핀 원소자를 사용하며, 통풍구 앞면에서 왼쪽부터 1번 VCC → 5V, 2번 DATA → D2, 3번 NC → 미사용, 4번 GND → UNO 위쪽 GND로 연결합니다. DATA와 5V 사이에 10kΩ 풀업 저항을 넣으세요. USB를 빼고 배선합니다. 3핀 모듈은 이 연결표와 다를 수 있습니다.

준비물: UNO R3, DHT22 4핀, 10kΩ 저항, 브레드보드, 점퍼선, USB 데이터 케이블. Arduino IDE에서 DHT sensor library by Adafruit와 Adafruit Unified Sensor를 설치합니다.

시리얼 모니터는 9600 baud. 약 2.5초마다 temp_C=섭씨온도 humidity_pct=상대습도가 나옵니다. ERROR: DHT22는 읽기 실패 안내이며, 그 줄에는 측정값을 출력하지 않습니다. 센서에 물이 닿지 않게 하고 주변 공기의 변화를 관찰하세요.

실제 보드·센서 동작과 측정값은 미시험입니다.
전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/008-dht22
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). 출처와 사용 조건은 저장소 README에 있습니다.

#코드플랜트 #아두이노 #DHT22 #온습도센서 #코딩교육
