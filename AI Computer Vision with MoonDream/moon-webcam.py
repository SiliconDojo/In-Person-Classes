import time

import cv2 as cv

# Initialize webcam (0 = default camera)
cam = cv.VideoCapture(1)

time.sleep(0.5)
# Capture one frame
ret, frame = cam.read()

if ret:
    cv.imshow("Captured", frame)
    cv.imwrite("captured_image.png", frame)
    cv.waitKey(0)
    cv.destroyWindow("Captured")
else:
    print("Failed to capture image.")

cam.release()
