
import cv2
import time

static_back = None
video = cv2.VideoCapture('/home/colozz/Téléchargements/run2.MOV')
skip = 110

while video.isOpened():
    frame = video.read()[1]
    if frame is None:
        break

    if skip > 0:
        skip -= 1
        continue

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if static_back is None:
        static_back = gray
        continue

    diff_frame = cv2.absdiff(static_back, gray)
    thresh_frame = cv2.threshold(diff_frame, 20, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    contours = cv2.findContours(thresh_frame.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)[1]

    if len(contours) > 0:
        biggestContour = contours[0]

        for contour in contours:
            if cv2.contourArea(contour) > cv2.contourArea(biggestContour):
                biggestContour = contour

        if cv2.contourArea(biggestContour) > 10000:
            (x, y, w, h) = cv2.boundingRect(biggestContour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)

    cv2.imshow("Diff Frame", diff_frame)
    cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)

    key = cv2.waitKey(1)

    if key == ord('q'):
        break

    time.sleep(0.1)

video.release()
cv2.destroyAllWindows()