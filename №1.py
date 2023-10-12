import cv2
import numpy as np
i=0

while(True):
    frame = cv2.imread("C:/NTO/images/d3961930-b0cd-4532-b983-4134559eea46.png")
    gray = cv2.Canny(frame,10,250)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    shapes = []
    frame = cv2.drawContours(frame,contours,-1,(0,255,0),3)
    for cnt in contours:
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        if len(approx) == 3:
            shapes.append("triangle")
        elif len(approx) == 4:
            shapes.append("rectangle")
        else:
            shapes.append("circle")

    # нахождение расстояний между фигурами
    k = 3 # количество соседей для алгоритма k-ближайших соседей
    distances = np.zeros((len(contours), len(contours)))
    for i in range(len(contours)):
        for j in range(i+1, len(contours)):
            dist = cv2.matchShapes(contours[i], contours[j], 1, 0.0)
            distances[i][j] = dist
            distances[j][i] = dist
    cv2.imshow('contours', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
print("Количество фигур:", len(contours))
print("Типы фигур:", shapes)
print("Расстояния между фигурами:")
for i in range(len(contours)):
    for j in range(i+1, len(contours)):
        print("- между", shapes[i], "и", shapes[j], ":", distances[i][j], "пикселей")