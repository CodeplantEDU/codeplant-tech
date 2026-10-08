각도를 바꾸는 서보모터 · 아두이노 UNO 버전

댓글에 'git'을 남기면 전체 코드와 연결 방법이 있는 GitHub 링크를 DM으로 보내드려요.

SG90 Digital의 혼(축에 끼우는 팔)을 움직여 봅니다. 60 → 90 → 120 명령을 1초 간격으로 보내고, 시리얼 숫자와 실제 움직임을 비교하세요. 숫자는 보낸 명령이며 실제 측정 각도가 아닙니다.

준비물: UNO R3, TowerPro SG90 Digital과 혼, USB 데이터 케이블, 점퍼선·서보 연결핀, 정전압 5V 외부 전원(2A 이상 용량 권장).

보드는 USB로, 서보는 외부 5V로 전원을 공급합니다. 서보 신호선은 D9, 접지는 외부 전원의 −와 UNO GND에 함께 연결하세요. 외부 +5V는 UNO의 5V·3.3V·VIN에 연결하지 않습니다. 배선은 두 전원을 끈 상태에서 합니다.

전체 코드를 업로드하고 시리얼 모니터를 9600 baud로 엽니다. 연속 회전 서보에는 이 예제를 그대로 적용하지 않습니다. 실제 하드웨어 동작은 미시험입니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/005-servo-motor
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), TowerPro SG90 Digital 공식 제품 자료(별도 자유 이용 라이선스 미확인, 원본 워터마크 유지). 사진·회로 출처와 사용 조건은 저장소 README를 확인하세요.

#코드플랜트 #아두이노 #서보모터 #각도제어 #코딩교육
