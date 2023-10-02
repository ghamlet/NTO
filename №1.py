import cv2
import numpy as np
i=0
cap = cv2.VideoCapture(0)
while(True):
    ret, frame= cap.read()
    frame = cv2.imread("C:/nto/images/1c3b4119-11ad-4f2f-9573-5e3afa5fdd09.png")
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()