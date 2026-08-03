import cv2
import time

def detect_fatigue():

    face = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

    eye = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_eye.xml"
    )

    cam = cv2.VideoCapture(0)

    closed_count = 0
    fatigue = False

    start_time = time.time()

    while True:

        ret, frame = cam.read()

        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face.detectMultiScale(gray,1.3,5)

        for (x,y,w,h) in faces:

            roi = gray[y:y+h, x:x+w]

            eyes = eye.detectMultiScale(roi)

            if len(eyes) == 0:
                closed_count += 1

        cv2.imshow("Face Scan", frame)

        # scan for 10 seconds
        if time.time() - start_time > 10:
            break

        if cv2.waitKey(1) == 27:
            break

    cam.release()
    cv2.destroyAllWindows()

    # fatigue decision
    if closed_count > 10:
        fatigue = True

    return fatigue
