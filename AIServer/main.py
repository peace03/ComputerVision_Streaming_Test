# main.py
import cv2  # OpenCV 라이브러리를 불러옵니다.

# 1. 영상 소스 연결 (수도관 연결)
# 웹캠인 경우 0, RTSP 주소인 경우 "rtsp://admin:1234@192.168.0.5..." 처럼 문자열로 입력
video_source = 0
cap = cv2.VideoCapture(video_source)

if not cap.isOpened():
    print("카메라를 열 수 없습니다. 연결을 확인해주세요!")
    exit()

print("영상 스트리밍 시작... (종료하려면 'q'를 누르세요)")

# 2. 무한 반복문을 통해 프레임 단위로 읽어오기
while True:
    # ret: 성공 여부(True/False), frame: 이미지 데이터
    ret, frame = cap.read()

    if not ret:
        print("더 이상 프레임을 가져올 수 없습니다.")
        break

    # (여기서 나중에 AI 분석 코드가 들어갈 예정입니다!)

    # 3. 화면에 보여주기 (Window 창 띄우기)
    cv2.imshow('CCTV Monitor', frame)

    # 'q' 키를 누르면 반복문 탈출 (종료)
    if cv2.waitKey(1) == ord('q'):
        break

# 4. 자원 해제 (수도관 잠그기)
cap.release()
cv2.destroyAllWindows()