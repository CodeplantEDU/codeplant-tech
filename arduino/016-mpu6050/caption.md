가속도와 회전을 읽는 MPU6050 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

가속도와 각속도를 X·Y·Z 세 축으로 읽습니다. 가속도에는 중력이 포함되며, 각속도는 돌아가는 빠르기입니다. 회전 각도·위치·방위를 바로 출력하는 예제가 아닙니다.

준비물: UNO R3, 5V 전원·신호를 지원하는 Adafruit 제품번호 3886 STEMMA QT, 점퍼선 4개, 연결용 헤더·브레드보드, USB 데이터 케이블. USB를 빼고 UNO 5V→모듈 VIN, 아래쪽 GND→GND, A4→SDA, A5→SCL을 연결하세요. 3Vo·INT·AD0 및 위쪽 보조 핀은 비워 둡니다. UNO VIN은 쓰지 않습니다. GY-521에는 이 핀 배열과 전압 조건을 그대로 적용하지 마세요.

Arduino IDE에서 Adafruit MPU6050(2.2.9)과 요청되는 의존성을 설치한 뒤 전체 코드를 업로드합니다. 시리얼 모니터 115200 baud. 기본 주소 0x68을 사용합니다. 초기화 실패 시 MPU6050_NOT_FOUND, 반복 중 주소 응답 실패 시 I2C_ACK 오류를 확인하세요.

READY 다음 acc_ms2=X,Y,Z gyro_rads=X,Y,Z를 출력합니다. 가속도 단위는 m/s², 각속도 단위는 rad/s입니다. 센서를 가만히 두고, 천천히 기울이고, 돌렸다 멈추며 비교하세요. 정지해도 중력 때문에 가속도는 모두 0이 아닙니다. 정지 각속도에도 보정 전 오차가 있을 수 있습니다. 전체 코드는 매회 500ms 대기를 더합니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/016-mpu6050
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). MPU6050 도형: Adafruit / bs, CC BY-SA 3.0. 배선도·3번 회로 카드도 CC BY-SA 3.0. 출처·조건은 README에 있습니다.

#코드플랜트 #아두이노 #MPU6050 #가속도센서 #코딩교육
