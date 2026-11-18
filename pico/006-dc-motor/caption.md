Pico로 DC모터의 방향과 구동 비율을 바꿔 보세요. GP16(21번)→ENA, GP17(22번)→IN1, GP18(24번)→IN2를 연결합니다. SunFounder L298N의 5V-EN·ENA·ENB 점퍼를 제거하고, 모터 전원 6V와 별도 논리 전원 5V의 GND를 Pico GND(23번)와 공유하세요. 외부 양전원을 Pico에 연결하지 마세요.

모터를 고정하고 바퀴와 부하를 뺀 뒤 Thonny Shell에 run을 입력하세요. A/B 방향과 70%·90% 명령에서 변화를 관찰해 보세요. 발열·막힘·심한 소음이 있으면 외부 전원을 끄세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/006-dc-motor

사진 출처와 사용 조건: Pico 보드는 Raspberry Pi Foundation / MicroPython 공식 자료, L298N은 SunFounder, TT모터 #3777은 Adafruit 공식 제품 사진입니다. 크기 조절과 배선 표시를 추가했습니다. 별도 자유 이용·재배포 허가는 확인되지 않았으며 원권리자 조건이 적용됩니다.

#코드플랜트 #CODEPLANT #라즈베리파이피코 #MicroPython #DC모터 #L298N #PWM
