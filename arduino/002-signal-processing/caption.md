입력부터 출력까지, 아두이노 신호처리 · UNO R3 버전

보드는 입력을 받고, 코드에 따라 판단한 뒤 출력을 바꿉니다.
오늘은 센서 없이 UNO R3와 데이터용 USB-B 케이블로 시작합니다.

전체 코드를 업로드하고 시리얼 모니터를 9600 baud로 열어 보세요.
1을 보내면 L LED가 켜지고 LED ON, 0을 보내면 꺼지고 LED OFF가 나옵니다.
다른 문자와 줄바꿈은 LED 상태를 바꾸지 않습니다.
이 입력은 PC가 보낸 문자이며 센서 핀에서 읽은 값은 아닙니다.

UNO R3의 ADC는 기본 설정에서 0~1023으로 입력 전압을 읽습니다.
PWM은 HIGH/LOW를 빠르게 바꾸며, 0~255로 켜져 있는 비율을 정합니다.
PWM 핀은 3·5·6·9·10·11입니다. 내장 LED의 13번 핀은 PWM 핀이 아닙니다.
ADC·PWM은 이번 편에서 개념을 구분하며 실제 아날로그 입력은 다음 조도센서 편에서 확인합니다.

전체 코드·USB 연결표·실행 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/002-signal-processing
코드플랜트 유튜브: https://www.youtube.com/@codeplant2024

보드 사진: SparkFun Electronics, CC BY 2.0 (표시 크기만 조절).
IDE 참고 화면: Arduino Documentation / Karl Söderby, CC BY-SA 4.0.
표지 카드는 CC BY-SA 4.0. 원본·사용 조건·기술 출처는 저장소 README에 있습니다.
실제 UNO 업로드·하드웨어 실행은 미시험입니다.

#코드플랜트 #CODEPLANT #아두이노 #ArduinoUNO #코딩교육 #신호처리 #디지털 #아날로그 #ADC #PWM
