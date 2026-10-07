빛을 감지하는 조도센서 · 아두이노 UNO 버전

댓글에 'git'을 남기면 전체 코드와 연결 방법이 있는 GitHub 링크를 DM으로 보내드려요.

이번에는 아날로그와 디지털 입력을 함께 배웁니다.
① AO를 A0에 연결해 밝기 변화를 0~1023으로 읽기
② USB를 빼고 AO 선을 DO→D2로 옮겨 0·1 읽기
③ 모듈의 조절기로 기준을 바꾸고 보드의 L LED 확인하기

UNO R3, 5V 지원 4핀 조도센서 모듈, 점퍼선 3개와 USB 데이터 케이블을 준비하세요. 전원은 5V↔VCC, GND↔GND입니다. 모듈의 인쇄된 핀 이름을 확인하세요.

AO 실습은 sketch.ino, DO 실습은 sketch-do.ino를 각각 업로드합니다. 시리얼 모니터는 둘 다 9600 baud입니다. AO의 숫자는 lux(럭스)가 아닙니다. SunFounder 예시 모듈은 기준보다 밝으면 DO가 0이고 L LED가 켜집니다. 다른 모듈은 출력 방향을 실제로 확인하세요.

전체 코드와 두 회로: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/001-cds-ao
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder 공식 제품 자료(별도 자유 이용 라이선스 미확인). 원본·사용 조건·기술 출처는 저장소 README에 있습니다. 실제 하드웨어 동작은 미시험입니다.

#코드플랜트 #아두이노 #조도센서 #디지털입력 #코딩교육
