무게를 숫자로 읽는 HX711과 로드셀 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

로드셀의 미세한 변화를 HX711으로 읽고, 빈 받침판의 영점을 맞춘 뒤 기준 추로 g 단위를 보정합니다. 원시값을 바로 무게라고 읽지 않습니다.

준비물: UNO R3, SparkFun HX711 SEN-13879, TAL220B 5kg SEN-14729, 고정용 받침·받침판·나사·간격재, 질량이 확인된 기준 추, 배선·헤더·USB 데이터 케이블.

USB를 빼고 UNO 5V→VCC·VDD, GND→GND, D3→DAT, D2→CLK(SCK)을 연결합니다. 이 조합의 로드셀은 빨강→RED(E+), 검정→BLK(E−), 초록→GRN(A+), 흰색→WHT(A−)입니다. 선 색과 함께 신호 이름도 확인하세요. YLW와 B 입력은 비워 둡니다. 다른 모듈에 이 조건을 그대로 적용하지 마세요.

로드셀 한쪽은 아래 받침, 반대쪽은 위 받침판에 고정하고 간격재로 휘어질 공간을 만듭니다. 받침판과 물체를 합쳐 정격 5kg을 넘기거나 충격을 주지 않습니다.

Arduino IDE에서 HX711 Arduino Library 0.7.5를 설치합니다. KNOWN_MASS_G의 0을 가진 기준 추의 실제 g값으로 바꾸고 전체 코드를 업로드하세요. 시리얼 모니터 115200 baud에서 빈 판으로 t, 기준 추를 올리고 안정된 뒤 c를 보냅니다. CAL_OK 이후 mass_g를 확인합니다. 리셋 또는 t 뒤에는 다시 보정합니다.

각 10회 평균을 사용하며 시간 초과나 ADC 한계값에서는 해당 회차의 무게를 출력하지 않습니다. 0.1g 표시는 측정 정확도 보장이 아닙니다. 추를 내리고 다시 올려 반복성을 비교해 보세요.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/018-hx711
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun UNO(CC BY 2.0), HX711·TAL220B 공식 제품 사진(별도 자유 이용 라이선스 미확인). 도형: SparkFun/tonicorinne(CC BY-SA 4.0), Wokwi(MIT). 도형을 조합한 배선도와 3·5번 회로 카드는 CC BY-SA 4.0. 출처·변경·사용 조건은 README에 있습니다.

#코드플랜트 #CODEPLANT #아두이노 #HX711 #로드셀 #무게센서 #코딩교육
