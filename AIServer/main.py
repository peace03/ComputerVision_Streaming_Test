# main.py 수정
import cv2  # OpenCV 라이브러리를 불러옵니다.
from ultralytics import YOLO  # 1. YOLO 라이브러리 불러오기

# 미리 학습된 YOLO 모델을 불러옵니다. (처음 실행 시 자동으로 파일을 다운로드합니다)
# 'yolov8n.pt'는 가장 가볍고 빠른 버전입니다.
model = YOLO('yolov8n.pt')

# 영상 소스 연결 (수도관 연결)
# 웹캠인 경우 0, RTSP 주소인 경우 "rtsp://admin:1234@192.168.0.5..." 처럼 문자열로 입력
video_source = 0
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 연결을 확인해주세요!")
    exit()

print("영상 스트리밍 시작... (종료하려면 'q'를 누르세요)")

# 무한 반복문을 통해 프레임 단위로 읽어오기
while True:
    # ret: 성공 여부(True/False), frame: 이미지 데이터
    ret, frame = cap.read()

    if not ret:
        print("더 이상 프레임을 가져올 수 없습니다.")
        break

    # 2. AI에게 프레임(사진)을 던져서 분석 시키기
    # results 안에 감지된 물체의 종류, 위치 정보가 다 들어갑니다.
    results = model(frame)

    # 3. 분석 결과를 화면에 그리기
    # plot() 함수는 사람, 의자 등을 네모 박스로 표시해 줍니다.
    annotated_frame = results[0].plot()

    # 4. AI가 그림을 그려준 화면(annotated_frame)을 띄우기
    cv2.imshow('AI CCTV', annotated_frame)

    if cv2.waitKey(1) == ord('q'):
        break

    # 화면에 보여주기 (Window 창 띄우기) 영상만 스트리밍할 때
    #cv2.imshow('CCTV Monitor', frame)

    # 'q' 키를 누르면 반복문 탈출 (종료)
    if cv2.waitKey(1) == ord('q'):
        break

# 4. 자원 해제 (수도관 잠그기)
cap.release()
cv2.destroyAllWindows()