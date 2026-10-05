빛을 감지하는 조도센서 · 아두이노 UNO 버전

센서를 가렸을 때와 손을 뗐을 때, 시리얼 모니터의 숫자가 어떻게 달라지는지 비교해 보세요.

준비물은 Arduino UNO R3, 5V 지원 4핀 조도센서 모듈, 점퍼선 3개입니다. USB를 빼고 5V↔VCC, GND↔GND, A0↔AO를 연결합니다. DO는 연결하지 않습니다. 모듈마다 핀 위치가 다르니 인쇄된 이름을 확인하세요.

전체 코드를 업로드하고 시리얼 모니터를 9600 baud로 열면 0.5초마다 값이 나옵니다. 이 값은 밝기 변화의 참고값이며 lux(럭스)는 아닙니다. 값이 커지는지 작아지는지는 실제 센서로 확인합니다.

전체 코드와 실행 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/001-cds-ao

사진: SparkFun Electronics(CC BY 2.0) / SunFounder 공식 자료. 자세한 출처는 저장소 README에 있습니다.
다음 편: 디지털센서의 0과 1 읽기.

#코드플랜트 #CODEPLANT #아두이노 #Arduino #조도센서 #센서활용 #피지컬컴퓨팅 #코딩교육
