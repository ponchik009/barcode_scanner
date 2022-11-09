import cv2
import os
import webbrowser
import time

print(cv2.__version__)
print(cv2.version.opencv_version)

# RTSP_URL = 'rtsp://admin:admin@192.168.0.8:8554/live'
RTSP_URL = 'rtsp://admin:admin@10.70.133.90:8554/live'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_ANY)

if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

bardet = cv2.barcode.BarcodeDetector()

def rotation(img):
    (h, w) = img.shape[:2]
    center = (int(w / 2), int(h / 2))
    rotation_matrix = cv2.getRotationMatrix2D(center, -90, 1)
    rotated = cv2.warpAffine(img, rotation_matrix, (w, h))
    return rotated

while True:
    print(1)
    _, frame = cap.read()

    if frame is None:
        print(frame)
        continue

    rotated = rotation(frame)
    resized = cv2.resize(rotated, (400, 400), cv2.INTER_NEAREST)
    cv2.imshow('RTSP stream', resized)
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(resized)

    if ok:
        print(decoded_info[0])

        url = "https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=" + decoded_info[0]
        webbrowser.open(url, new=0, autoraise=True)
        break
    else:
        print(ok)

    if cv2.waitKey(1) == 27:
        break
    
    #time.sleep(0.5)

cap.release()
cv2.destroyAllWindows()