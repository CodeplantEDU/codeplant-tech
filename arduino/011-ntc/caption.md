온도에 따라 저항이 바뀌는 NTC 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

따뜻해질수록 저항이 줄어드는 2선 NTC로 온도를 계산합니다. 이번 제품은 Adafruit 372, 25°C에서 10kΩ, B25/50=3950입니다. 다른 NTC의 계수를 그대로 섞어 쓰지 마세요.

준비물: UNO R3, 해당 NTC, 고정 10kΩ 저항(1% 권장), 브레드보드, 점퍼선, USB 데이터 케이블. USB를 빼고 5V→고정 저항→NTC→위쪽 GND를 연결합니다. 두 부품 사이의 접점에 A0도 연결하세요. NTC는 극성이 없고 AREF·VIN은 쓰지 않습니다.

전체 코드 업로드 후 시리얼 모니터 9600 baud. 약 1초마다 raw=입력값 temp_C=계산한 섭씨 온도가 나옵니다. 센서 끝을 손으로 가볍게 감싸고 놓으며 비교하세요. 이 배선에서는 따뜻해질수록 raw가 내려가고 계산 온도는 올라갑니다. 0 또는 1023이면 ERROR: ADC_ENDPOINT를 출력합니다. 이 오류만으로 단선 위치를 확정하지는 않습니다.

온도는 B 계수로 계산한 근사값이며 소수점 자릿수가 정확도는 아닙니다. 불·뜨거운 물을 쓰지 않습니다. 실제 보드·센서·온도 측정은 미시험입니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/011-ntc
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), Adafruit 공식 제품 사진(별도 자유 이용 라이선스 미확인). 회로 NTC 도형: Fritzing / Brendan Howell, CC BY-SA 3.0; 회로 이미지 및 3번 회로 카드도 CC BY-SA 3.0. 출처·조건은 README에 있습니다.

#코드플랜트 #아두이노 #NTC #온도센서 #코딩교육
