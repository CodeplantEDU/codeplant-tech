기울기로 접점을 바꾸는 2핀 볼 스위치 · ESP32 MicroPython 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

스위치를 기울이면 내부 금속 공이 접점을 붙이거나 뗍니다. GPIO27의 내부 풀업으로 열린 접점은 1(HIGH), 닫혀 GND로 이어진 접점은 0(LOW)으로 읽습니다. 각도(°)를 재는 센서는 아닙니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀 Micro-USB), Adafruit 173 형태의 2핀 볼 기울기 스위치, 브레드보드, 점퍼선 2개, USB 데이터 케이블, Thonny. USB를 빼고 D27→한쪽 다리, 왼쪽 VIN 바로 위 GND→다른 다리를 연결합니다. 다리는 서로 다른 브레드보드 연결 줄에 꽂습니다. 3V3·VIN·5V 센서 전원선은 연결하지 않습니다. 3핀 모듈에는 이 회로를 그대로 쓰지 마세요.

MicroPython v1.29.0 일반 ESP32 기준입니다. Thonny에서 MicroPython(ESP32)와 실제 COM 포트를 선택해 전체 main.py를 실행합니다. READY 뒤 처음 상태도 50ms 조건을 거쳐 state와 contact를 표시합니다. 이후 안정된 상태가 바뀔 때만 새 줄이 나옵니다. 접점 닫힘은 CLOSED·0, 열림은 OPEN·1입니다. 내장 LED는 제어하지 않습니다.

raw가 바뀔 때마다 시간을 다시 잡고 50ms 동안 같은 값이 읽히면 확정합니다. sleep_ms(5)는 최소 대기이므로 정확한 5ms 주기가 아니며 샘플 사이의 짧은 변화는 놓칩니다. 천천히 기울여 멈추기와 살짝 흔들기를 비교하고, DEBOUNCE_MS를 50에서 100으로 바꿔 반응 지연도 관찰하세요. 특정 각도나 움직임 횟수의 측정값으로 읽지 않습니다.

항상 0이면 같은 연결 줄·직결, 항상 1이면 빠진 선·접점 방향을 확인합니다. Ctrl+C로 종료합니다. 배선 수정은 USB를 빼고 하며 GPIO27을 출력으로 바꾸거나 5V를 넣지 마세요.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/004-tilt
유튜브: https://www.youtube.com/@codeplant2024

사진: SunFounder ESP32 공식 제품 사진(별도 자유 이용 라이선스 미확인), lady ada / Adafruit 2핀 스위치(CC BY-SA 3.0). 도형: Wokwi(MIT), Fritzing / Lionel Michel(CC BY-SA 3.0). 회로 이미지와 이를 담은 카드는 CC BY-SA 3.0. 상세 출처·사용 조건은 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #기울기센서 #풀업 #디바운싱 #코딩교육
