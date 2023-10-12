import cv2
import numpy as np
import math

my_photo = cv2.imread('C:/NTO/images/d3961930-b0cd-4532-b983-4134559eea46.png')
img_grey =cv2.cvtColor(my_photo,cv2.COLOR_BGR2GRAY)
img_grey = cv2.Canny(my_photo,100,200)

thresh = 100

#get threshold image
ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

#find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = sorted(contours, key= cv2.contourArea,reverse=True)
#create an empty image for contours
img_contours = np.uint8(np.zeros((my_photo.shape[0],my_photo.shape[1])))

cv2.drawContours(my_photo, contours, -1, (0,255,0), 3)
cv2.imshow('origin', my_photo) # выводим итоговое изображение в окно
cv2.imshow('res', img_contours) # выводим итоговое изображение в окно

shapes = []
for cnt in contours:
    approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
    if len(approx) == 3:
        shapes.append("triangle")
    elif len(approx) == 4:
        x,y,w,h = cv2.boundingRect(cnt)
        if abs(w-h) <= 10:
            shapes.append("square")
        else:
            shapes.append("rectangle")
    elif len(approx) > 4 and len(approx) <= 6:
        shapes.append("polygon")
    else:
        shapes.append("circle")

num_shapes = len(shapes)

print("Количество фигур: ", num_shapes)
print("Типы фигур: ", shapes)
distances = []
for i in range(num_shapes):
    for j in range(i+1, num_shapes):
        cnt1 = contours[i]
        cnt2 = contours[j]
        cv2.line(my_photo, cnt1[0][0],cnt2[0][0], (0,255,0), 3)
        dist = math.sqrt((cnt1[0][0][0]-cnt2[0][0][0])**2 + (cnt1[0][0][1]-cnt2[0][0][1])**2)
        distances.append((shapes[i], shapes[j], dist))

# вывод результатов
print("Расстояния между фигурами:")
for d in distances:
    print("- между", d[0], "и", d[1], ":", round(d[2], 2), "пикселей")
cv2.waitKey()
cv2.destroyAllWindows()
  