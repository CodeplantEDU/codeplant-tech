방향과 속도를 바꾸는 DC모터 · 아두이노 UNO 버전

댓글에 'git'을 남기면 전체 코드와 연결 방법이 있는 GitHub 링크를 DM으로 보내드려요.

L298N과 TT모터 한 개로 방향·출력을 바꿉니다. A 방향에서 PWM 180 → 230, 정지 후 B 방향에서도 같은 순서를 확인하세요. 숫자는 속도 측정값(RPM)이 아닌 PWM 명령입니다.

준비물: UNO R3, SunFounder L298N, Adafruit 제품번호 3777 TT모터(3~6V), USB 데이터 케이블, 점퍼선·접지 분기 단자, 드라이버, 정전압 6V 외부 전원(2A 용량 권장).

5V-EN·ENA·ENB 점퍼를 빼세요. 외부 +6V→12V 표시 단자, UNO 5V→모듈 +5V, 두 전원의 GND는 함께 연결합니다. D9→ENA, D8→IN1, D7→IN2, 모터 두 선→OUT1·OUT2. 미사용 ENB·IN3·IN4는 GND에 연결합니다.

모터에 12V를 쓰거나 UNO 핀에서 모터 전원을 공급하지 않습니다. 배선은 두 전원을 끈 상태에서 하세요. 시리얼 모니터 9600 baud. 실제 회전·온도·전류는 미시험입니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/006-dc-motor
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder·Adafruit 공식 제품 자료(별도 자유 이용 라이선스 미확인). 원본과 사용 조건·기술 근거는 README를 확인하세요.

#코드플랜트 #아두이노 #DC모터 #모터드라이버 #코딩교육
