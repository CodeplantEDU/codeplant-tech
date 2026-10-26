CODEPLANT TECH | ESP32 03 · 빛의 변화를 조도센서 AO로 읽기

빛이 달라지면 LDR의 저항과 모듈의 AO 전압이 달라집니다. GPIO34의 ADC로 읽은 숫자 8개를 평균 내고, 소프트웨어 기준과 비교해 Shell에 표시합니다. 원시값을 lux나 밝기 %라고 읽지 않습니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), 3.3V 지원 SunFounder 4핀 조도센서 모듈, 점퍼선 3개·브레드보드·USB 데이터 케이블·Thonny.

USB를 빼고 3V3→VCC, GND→GND, D34(GPIO34)→AO를 연결하세요. DO는 비워 둡니다. 모듈 VCC를 VIN·5V에 연결하지 마세요. 다른 모듈은 자체 전압 조건과 핀 이름을 확인합니다.

MicroPython v1.29.0 기준 전체 코드를 실행하고 READY 뒤 raw_u16와 band를 확인합니다. 이 모듈은 밝을수록 AO 값이 낮아집니다. 같은 자리에서 LDR만 가렸다 떼며 평균값을 여러 줄 비교하세요. 32768은 숫자 비교용 기준이며 특정 lux나 낮/밤 기준이 아닙니다. 모듈 가변저항은 DO 기준을 바꾸므로 이번 AO 코드의 THRESHOLD와 구분합니다.

ATTN_11DB에서도 일반 ESP32의 근사 선형 범위는 약0.15~2.45V입니다. 3.3V 전원이라고 전체 범위가 정확히 측정되는 것은 아닙니다. 끝값 부근의 포화는 평균으로 해결되지 않습니다. Ctrl+C로 종료하며 오류나 배선 의심 시 USB를 빼고 확인하세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/003-cds-ao
유튜브: https://www.youtube.com/@codeplant2024

사진: SunFounder 공식 ESP32·조도센서 자료(별도 자유 이용 라이선스 미확인). 도형·핀 좌표: Wokwi(MIT). 출처·사용 조건은 README를 확인하세요.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #조도센서 #LDR #ADC #코딩교육