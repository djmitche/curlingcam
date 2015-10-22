import numpy as np
import cv2
import cv
import sys

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv.CV_FOURCC(*'MJPG')
out = cv2.VideoWriter(sys.argv[1], fourcc, 15.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret:
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()
