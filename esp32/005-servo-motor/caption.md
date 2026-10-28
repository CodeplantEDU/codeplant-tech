펄스 폭으로 위치를 명령하는 서보모터 · ESP32 MicroPython 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

GPIO18에서 50Hz 신호를 만들고, HIGH가 유지되는 펄스 폭을 바꿔 SG90 Digital 위치 제어형 서보에 목표 위치를 명령합니다. 20ms 주기에서 1400·1500·1600µs는 각각 7·7.5·8%입니다. 50Hz는 회전수가 아니며 command_us는 실제 각도 측정값이 아닙니다.

ESP32 DevKit v1(ESP-WROOM-32 30핀), TowerPro SG90 Digital 위치형, SN74AHCT125N DIP14, 100nF 세라믹, 10kΩ 저항, 외부 정전압 5V·2A 이상(실습 권장), 브레드보드·점퍼선·USB 데이터 케이블·Thonny를 준비하세요. SG90의 3.3V 입력 기준이 명시되지 않아 AHCT 버퍼로 신호를 5V 수준으로 변환합니다. HC125로 대체하지 마세요.

두 전원 OFF에서 D18→IC2(1A), IC3(1Y)→서보 신호. 외부+5V→서보V+·IC14 및 4/10/13, 공통GND→보드GND·서보GND·IC1/7 및 5/9/12. IC6/8/11은 미연결. 100nF는14↔7 가까이, 10kΩ은2↔GND. 외부+5V를 보드3V3/VIN/GPIO에 연결하지 않습니다. 서보 케이블 역할·IC 홈 방향을 원본 핀표로 대조하세요.

외부 전원을 끄고 부하·장애물을 제거합니다. USB 연결→MicroPython v1.29.0 ESP32에서 전체 main.py 실행→READY 확인→외부 전원 ON. 처음 COMPARE=False로1500µs만 확인합니다. 이상이 없을 때 전원을 끄고 COMPARE=True로 바꿔 재실행하면1500→1400→1500→1600µs를2초 이상 간격으로 비교합니다. STEP_US=50으로 폭을 줄이거나 HOLD_MS=3000으로 관찰 시간을 늘려 보세요.

1500µs는 중앙 부근 시작점이며90° 보장이 아닙니다. 직접 본 방향·위치·떨림을 기록합니다. 심한 소음·막힘·발열이면 외부 전원을 즉시 끄세요. Ctrl+C는 신호를 끄며 전력을 차단하지 않습니다. 재실행·리셋·배선 수정 전에는 외부 전원을 먼저 끕니다.

https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/005-servo-motor
유튜브: https://www.youtube.com/@codeplant2024

사진: SunFounder ESP32 공식 제품 사진, TowerPro SG90 Digital 공식 제품 사진. 두 사진의 별도 자유 이용·재배포 허락은 미확인으로 원본 권리를 유지합니다. 도형 Wokwi MIT. 상세 출처·사용 조건은 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #서보모터 #PWM #펄스폭 #코딩교육
