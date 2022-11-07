import cv2
import os
import webbrowser

print(cv2.__version__)
print(cv2.version.opencv_version)

RTSP_URL = 'rtsp://admin:admin@192.168.0.8:8554/live'

os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;udp'

cap = cv2.VideoCapture(RTSP_URL, cv2.CAP_FFMPEG)

if not cap.isOpened():
    print('Cannot open RTSP stream')
    exit(-1)

bardet = cv2.barcode.BarcodeDetector()
#img = cv2.imread("mailing.drawio.png")
#ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(img)

#print(ok, decoded_info, decoded_type, corners)

while True:
    _, frame = cap.read()
    #cv2.imshow('RTSP stream', frame)
    ok, decoded_info, decoded_type, corners = bardet.detectAndDecode(frame)

    if ok:
        print(decoded_info[0])

        url = "https://barcode-list.ru/barcode/RU/%D0%9F%D0%BE%D0%B8%D1%81%D0%BA.htm?barcode=" + decoded_info[0]
        webbrowser.open(url, new=0, autoraise=True)
        break


    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()