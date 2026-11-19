Pico로 손잡이 위치에 따라 바뀌는 가변저항 값을 읽어 보세요. USB를 빼고 10kΩ 선형 가변저항의 양끝을 3V3(OUT, 36번)와 AGND(33번), 가운데 접점을 GP26(31번)에 연결하세요. 각 다리는 브레드보드의 서로 다른 줄에 꽂고 5V는 연결하지 마세요.

Thonny Shell에서 한쪽 끝·가운데·반대쪽 끝의 raw_u16 값을 여러 줄 비교하세요. PRINT_MS를 100에서 500으로 바꿔 출력 간격도 살펴보세요.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/pico/007-potentiometer

사진 출처와 사용 조건: Pico는 Raspberry Pi Foundation / MicroPython 공식 사진, 가변저항은 Adafruit #562 공식 제품 사진입니다. 비율을 유지해 크기를 조절했습니다. 별도 재배포 허가 표기는 확인되지 않았으며 원권리자 조건이 적용됩니다. 가변저항 도형은 Wokwi(MIT)입니다.

#코드플랜트 #CODEPLANT #라즈베리파이피코 #MicroPython #가변저항 #ADC #센서실습
