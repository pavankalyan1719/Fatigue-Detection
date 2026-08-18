import cv2
import numpy as np


def detect_fatigue_from_image(image_bytes):

    # Convert uploaded image bytes into a NumPy array
    image_array = np.frombuffer(
        image_bytes,
        np.uint8
    )

    # Convert NumPy array into OpenCV image
    frame = cv2.imdecode(
        image_array,
        cv2.IMREAD_COLOR
    )

    if frame is None:
        return False

    # Load face and eye classifiers
    face = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_frontalface_default.xml"
    )

    eye = cv2.CascadeClassifier(
        cv2.data.haarcascades +
        "haarcascade_eye.xml"
    )

    # Convert image to grayscale
    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    # Detect faces
    faces = face.detectMultiScale(
        gray,
        1.3,
        5
    )

    closed_count = 0

    # Detect eyes
    for (x, y, w, h) in faces:

        roi = gray[
            y:y+h,
            x:x+w
        ]

        eyes = eye.detectMultiScale(roi)

        if len(eyes) == 0:
            closed_count += 1

    # Fatigue decision
    if closed_count > 0:
        return True

    return False
