11 · 온도에 따라 저항이 바뀌는 NTC · ESP32 MicroPython

따뜻해지면 NTC 저항이 줄고, 분압 접점 전압과 GPIO34의 ADC 값도 내려갑니다. 10번 읽은 정수 평균 raw_u16를 비교합니다. 숫자는 섭씨온도·저항·밝기 %가 아닙니다.

준비물: ESP32 DevKit v1(ESP-WROOM-32 30핀), Adafruit 372 2선 NTC(25°C에서 10kΩ, B25/50=3950), 고정 10kΩ 저항(1%), 브레드보드·점퍼선·USB 데이터 케이블·Thonny.
USB를 빼고 3V3→고정 10kΩ→접점→NTC→GND로 연결하고 접점에 D34(GPIO34)를 연결하세요. NTC 자체에는 극성이 없지만 두 저항의 위치를 바꾸면 값의 방향이 달라집니다. VIN·5V는 쓰지 않습니다. GPIO에 5V를 넣지 마세요.

MicroPython v1.29.0 기준 전체 main.py를 실행하고 READY 뒤 raw_u16를 기록합니다. 센서 끝을 손으로 가볍게 감쌌다가 놓고 여러 줄의 변화 방향을 비교하세요. 불·뜨거운 물·침수는 쓰지 않습니다.
read_u16의 0~65535는 반환 범위입니다. ATTN_11DB에서도 일반 ESP32의 근사 선형 범위는 약 0.15~2.45V입니다. 전원 3.3V 전체의 정확도나 16비트 정확도를 뜻하지 않습니다. 개별 값에 0·65535가 있으면 ADC_ENDPOINT를 표시합니다. USB를 빼고 배선·접점·부품을 확인하세요. 1초 대기와 10회 대기·처리 시간이 더해집니다. Ctrl+C로 종료하며 ADC_ERROR면 멈춥니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/011-ntc

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #NTC #서미스터 #ADC #코딩교육
사진: SunFounder ESP32·Adafruit 372 공식 사진(별도 자유 이용·재배포 허가 미확인). NTC 회로 도형: Fritzing / Brendan Howell(CC BY-SA 3.0). 회로 이미지·배선 HTML·3번 회로 카드도 CC BY-SA 3.0. Wokwi 보드·저항 MIT. 출처와 조건은 README를 확인하세요.