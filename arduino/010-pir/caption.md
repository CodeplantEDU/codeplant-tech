움직임을 감지하는 PIR 센서 · 아두이노 UNO 버전

전체 코드와 연결 방법은 아래 GitHub 주소에서 확인하세요.

HC-SR501 앞을 가로질러 움직이고, D2 신호와 UNO 내장 L LED를 비교합니다. PIR은 적외선의 변화로 움직임을 감지합니다. 거리·체온·사람 수를 재는 센서는 아닙니다.

준비물: UNO R3, HC-SR501, 점퍼선 3개, USB 데이터 케이블, 필요하면 브레드보드. USB를 빼고 5V→VCC, 위쪽 GND→GND, D2←OUT(DO)을 연결하세요. 앞뒤 방향에 따라 핀 순서가 달라 보이므로 실물 표시를 확인합니다. 외부 LED·저항·추가 라이브러리는 필요 없습니다.

전체 코드 업로드 후 시리얼 모니터 9600 baud. WAIT_60S 동안 60초 기다리고 READY 뒤 관찰하세요. pir=1이면 L LED가 켜지고 pir=0이면 꺼집니다. 처음 상태와 바뀐 상태만 출력합니다.

멈춰도 지연 설정 때문에 HIGH가 유지될 수 있습니다. H 모드는 추가 움직임으로 유지 시간이 늘어나고 L 모드는 정해진 시간이 지나면 LOW로 돌아옵니다. LOW를 사람이 없다는 뜻으로 단정하지 않습니다. 실제 하드웨어 동작은 미시험입니다.

전체 코드와 연결 방법: https://github.com/CodeplantEDU/codeplant-tech/tree/main/arduino/010-pir
유튜브: https://www.youtube.com/@codeplant2024

사진: SparkFun(CC BY 2.0), SunFounder HC-SR501 공식 사진(별도 자유 이용 라이선스 미확인). 회로 도형은 Wokwi. 사진·그림의 출처와 사용 조건은 README에 있습니다.

#코드플랜트 #아두이노 #PIR센서 #움직임감지 #코딩교육
