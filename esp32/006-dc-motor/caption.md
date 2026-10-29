드라이버로 방향과 출력을 바꾸는 DC모터 · ESP32 MicroPython 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

GPIO26·27이 방향을 고르고 GPIO25의1000Hz PWM이 L298N ENA를 제어합니다. 주기1ms에서70·90%는 HIGH 약0.7·0.9ms, duty_u16 요청45875·58982입니다. 비율 명령은 실제 RPM·전압·토크가 아닙니다.

ESP32 DevKit v1(ESP-WROOM-32 30핀), SunFounder L298N, Adafruit #3777 TT모터(3~6V) 한 개, 10kΩ, 브레드보드·배선·접지 분기 단자, USB 데이터 케이블·Thonny를 준비하세요. 모터용 정전압6V·2A 이상과 별도 논리용 정전압5V·0.5A를 실습 권장으로 사용합니다. 보드는 USB 전원만 씁니다.

모든 전원OFF에서5V-EN·ENA·ENB 점퍼를 제거합니다. +6V→12V 표시 단자, 별도+5V→+5V 단자. 모든 전원−·보드 GND(3V3 바로 위)→L298N GND. D25→ENA, D26→IN1, D27→IN2, TT모터 두 선→OUT1·OUT2. ENA↔GND에10kΩ 풀다운. 미사용 ENB·IN3·IN4는GND, OUT3·OUT4는미연결. 외부+5V·+6V를 보드 VIN·3V3·GPIO에 넣지 마세요. 사진은 점퍼 제거 전 참고입니다.

MicroPython v1.29.0 전체 main.py를 실행하고 READY를 확인한 뒤 논리5V→모터6V 순서로 켭니다. 모터를 고정하고 바퀴·부하·손을 뗀 채 Shell에 run을 입력하세요. 정지→A70→A90→정지→B70→B90→정지를 최소2초 간격으로 한 번 실행하고 입력을 기다립니다. q는 입력 대기 중 종료, Ctrl+C는 실행 중 중단입니다.

ENA=0은 구동 해제·관성 정지이며 강제 브레이크가 아닙니다. 방향 전환 전에 축이 아직 돌면 전원을 끄고 STOP_MS를 늘립니다. 코드는 실제 정지를 감지하지 못합니다. 출력값과 직접 본 방향·변화·소음을 기록하세요. 모터 선을 바꾸면 A/B가 뒤집힙니다. 심한 소음·발열·냄새·축 막힘이면 즉시 외부 전원을 끄세요. 리셋·재실행·배선 수정 전에도 외부 전원을 먼저 끕니다.

https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/006-dc-motor
유튜브: https://www.youtube.com/@codeplant2024
사진: SunFounder ESP32·L298N, Adafruit #3777 공식 제품 사진(별도 자유 이용·재배포 허락 미확인). 도형 Wokwi(MIT). 출처·사용 조건은 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #DC모터 #L298N #PWM #코딩교육
