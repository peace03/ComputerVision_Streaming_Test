import cv2 #OpenCV: 영상 처리를 위한 라이브러리
from ultralytics import YOLO #YOLO: 물체를 인식하는 AI 모델
import winsound #윈도우용 소리 라이브러리
import math

#1. AI 모델 불러오기
#'yolov8n.pt'는 가장 가볍고 빠른 모델이다. 처음 실행 시 자동으로 다운로드 된다.
model = YOLO('yolov8n.pt')

#2. RTSP 주소 설정 (IP Webcam 앱에 뜬 주소로 변경)
#컴퓨터의 웹캠을 쓰고싶으면 rtsp_url = 0
rtsp_url = "rtsp://test:1234!!@172.30.1.98:8080/h264_ulaw.sdp"

#3. 영상 스트림 연결
cap = cv2.VideoCapture(rtsp_url)

# 클래스 이름들 (YOLO가 인식할 수 있는 물체들)
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]

print("CCTV 시스템 가동 시작...")

while True:
    #4. 영상 프레임 하나씩 읽어오기
    success, img = cap.read()

    #영상을 못읽어 왔으면 반복문 종료
    if not success:
        print("영상을 불러올 수 없습니다. RTSP 연결을 확인해 주세요.")
        break

    #5. AI에게 이미지 보여주고 분석 맡기기 (stream = True는 속도 최적화)
    results = model(img, stream=True)

    #6. 분석 결과 처리
    for r in results:
        boxes = r.boxes
        for box in boxes:
            #감지된 물체 종류(Class) 확인
            cls = int(box.cls[0])
            conf = math.ceil(box.conf[0] * 100) / 100 #정확도

            current_class = classNames[cls]

            #핵심기능: 'person'이 감지되면 경보 울리기!
            if current_class == "person" and conf>0.5:
                print(f"침입자 감지!! ({current_class})")

                #윈도우 비프음 (주파수 1000Hz, 0.5초 지속)
                winsound.Beep(1000, 200)

                #화면에 빨간 네모 그리기
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)
                cv2.putText(img, "INTRUDER!", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    #7. 화면에 결과 보여주기
    cv2.imshow('My AI CCTV', img)

    #'q'키를 누르면 좋료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

#종료 처리
cap.release()
cv2.destroyAllWindows()