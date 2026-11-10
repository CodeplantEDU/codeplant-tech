18 · 로드셀의 작은 변화를 무게 숫자로 읽기 · ESP32 MicroPython

SparkFun HX711 SEN-13879와 TAL220B 5kg을 사용합니다. 두 전원을 끄고 VDD→ESP32 3V3, VCC→외부 안정화 5V, DAT→D19, CLK→D23을 연결하세요. ESP32·HX711·외부 전원의 GND는 공통입니다. 외부 +5V를 ESP32 VIN·3V3에 넣거나 VCC·VDD를 서로 연결하지 마세요. GPIO18은 비워 둡니다.

로드셀 한쪽 끝과 받침판을 올바르게 고정하고 총 하중 5kg 이내에서 사용하세요. 빨강→RED, 검정→BLK, 초록→GRN, 흰색→WHT입니다. README의 드라이버를 저장하고 빈 판에서 영점을 잡은 다음, 질량이 확인된 추로 보정하세요. 추를 내려 0 근처로 돌아오는지, 같은 추와 다른 추에서 어떻게 달라지는지 기록해 보세요. 소수 한 자리 출력이 정확도를 보장하지는 않습니다.

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.
https://github.com/CodeplantEDU/codeplant-tech/tree/main/esp32/018-hx711

사진: SunFounder ESP32, SparkFun HX711·TAL220B 공식 제품 사진. 표시 크기 조절. 별도 자유 이용 라이선스 미확인으로 원권리자 사용 조건 적용. HX711 도형: SparkFun/tonicorinne CC BY-SA 4.0. 파생 회로·HTML·3·5번 배선 카드의 도형·배선 기여분도 같은 조건. 사진·상표는 별도 권리. Wokwi 보드 MIT. 상세 출처는 README에 있습니다.

#코드플랜트 #CODEPLANT #ESP32 #MicroPython #HX711 #로드셀 #무게센서 #코딩교육