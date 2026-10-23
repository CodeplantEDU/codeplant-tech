흙의 변화를 읽는 정전용량식 수분 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

DFRobot SEN0193의 아날로그 전압을 A0로 읽고, 직접 기록한 건조·젖음 기준으로 상대 수분 지수를 계산합니다. raw 0~1023과 wet_index 0~100을 구분하세요. 상대 지수는 토양 수분 함량 %가 아닙니다.

준비물: UNO R3, SEN0193과 3핀 연결 케이블, 점퍼선, USB 데이터 케이블, 비교할 흙과 물. USB를 빼고 빨강 VCC→5V, 검정 GND→GND, 노랑 Signal→A0를 연결합니다. UNO VIN에 연결하지 않습니다. 다른 모듈은 자체 핀표를 확인하세요.

이 모델은 전체 방수가 아닙니다. 제조사 경계선 아래 프로브만 넣고 상단 회로·커넥터를 젖히지 마세요. 토양 종류·삽입 깊이·다짐 정도도 값에 영향을 줍니다.

Arduino IDE에서 전체 코드를 업로드하고 시리얼 모니터 9600 baud로 엽니다. 처음에는 raw와 CALIBRATE_FIRST가 나옵니다. 공기 중 값과 물에 프로브만 넣은 값을 직접 기록해 DRY_RAW·WET_RAW의 -1을 바꾸고 다시 업로드합니다. DRY_RAW > WET_RAW인지 확인하세요.

10회 평균으로 원시값을 읽습니다. 보정 뒤 wet_index≤30이면 L LED가 켜지고 ≥40이면 꺼지며 사이에서는 직전 상태를 유지합니다. OUTSIDE_CAL은 보정 범위 밖이라는 안내입니다. 30·40은 비교 실습 기준으로, 식물별 물주기 처방이 아닙니다. 펌프는 연결하지 않습니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/020-soil-moisture
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun UNO(CC BY 2.0), DFRobot SEN0193 공식 제품 사진·부품 그림·삽입 한계 자료(별도 자유 이용 라이선스 미확인). UNO 도형 Wokwi(MIT). 출처와 사용 조건은 README에 있습니다.

#코드플랜트 #CODEPLANT #아두이노 #토양수분센서 #SEN0193 #ADC #코딩교육
