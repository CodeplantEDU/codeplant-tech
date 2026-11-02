10 · 적외선 변화로 움직임을 감지하는 PIR · ESP32 MicroPython

HC-SR501의 OUT을 GPIO27로 읽고 상태가 바뀔 때 Shell에 표시합니다. HIGH 유지 시간과 코드의 읽기 간격을 나누어 관찰해 보세요. 거리·체온·사람 수를 재는 센서는 아닙니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), SunFounder HC-SR501, 외부 정전압 5V, 저전압 단자·브레드보드·점퍼선, USB 데이터 케이블·Thonny.
USB와 외부 전원을 모두 끄고 센서 VCC→외부 +5V, OUT/DO→D27을 연결합니다. 외부 −·센서 GND·ESP32 GND는 함께 연결하세요. 외부 +5V는 ESP32 VIN·3V3에 연결하지 않습니다. 이 모델의 OUT HIGH는 약 3.3V입니다. 다른 부품의 출력 조건을 확인하고 GPIO에 5V를 넣지 마세요.

MicroPython v1.29.0 기준 전체 코드를 실행하고 WAIT_60S 뒤 READY를 기다립니다. 센서 앞을 천천히 가로질러 움직였다가 멈추며 pir=1/HIGH와 pir=0/LOW 변화를 기록하세요. 처음 상태도 출력하며 같은 상태의 줄은 반복하지 않습니다. LOW만으로 사람이 없다고 확정하지 않습니다.
H 모드는 재감지로 유지가 늘고 L 모드는 유지 중 재연장하지 않습니다. LOW 뒤 차단 구간도 있습니다. 조절 전 두 전원을 끄고 실물 표시를 확인하세요. 매번 읽은 뒤 50ms 대기하며 처리 시간이 더해집니다. 모듈 지연과 별개입니다. Ctrl+C로 멈추고, 배선 수정은 두 전원을 모두 끈 뒤 합니다. OUT으로 LED·모터·릴레이를 직접 구동하지 않습니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/010-pir

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #PIR #HCSR501 #디지털입력 #코딩교육
사진: SunFounder 공식 ESP32·HC-SR501 제품 사진. 별도 자유 이용·재배포 허가 미확인, 원권리자 사용 조건 적용. 뒷면 설명 그림은 실제 사진과 구분해 README에 수록합니다. Wokwi 부품 도형 MIT. 상세 출처와 조건은 위 README를 확인하세요.