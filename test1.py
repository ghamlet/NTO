import cv2
import numpy as np
import math

def distances(contour1, contour2):
    x1, y1, w1, h1 = cv2.boundingRect(contour1)
    x2, y2, w2, h2 = cv2.boundingRect(contour2)
    center1 = (x1 + w1 // 2, y1 + h1 // 2)
    center2 = (x2 + w2 // 2, y2 + h2 // 2)
    #cv2.line(my_photo, center1,center2,(255,255,255),3)
    distance = np.sqrt((center2[0] - center1[0])**2 + (center2[1] - center1[1])**2)
    return distance


my_photo = cv2.imread('C:/NTO/images/1c3b4119-11ad-4f2f-9573-5e3afa5fdd09.png')
img_grey =cv2.cvtColor(my_photo,cv2.COLOR_BGR2GRAY)
img_grey = cv2.Canny(my_photo,100,200)

thresh = 100

#get threshold image
ret,thresh_img = cv2.threshold(img_grey, thresh, 255, cv2.THRESH_BINARY)

#find contours
contours, hierarchy = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
contours = sorted(contours, key= cv2.contourArea,reverse=True)
#create an empty image for contours
img_contours = np.uint8(np.zeros((my_photo.shape[0],my_photo.shape[1])))

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
max_dist = 0
for i in range(len(contours)):
    for j in range(i+1, len(contours)):
        distance = distances(contours[i],contours[j])
        if distance> max_dist:
            max_dist = distance
            n = contours.index(contours[i])
            m = contours.index(contours[j])
print('ind1=',n)
print('ind2=',m)            
print('dist=',distance)
min_dist = 1000
x2, y2, w2, h2 = cv2.boundingRect(contours[n])
center1 = (x2 + w2 // 2, y2 + h2 // 2)
for h in contours[m]:
    x, y  = contours[m][h]
    cnt= (x,y)
    dist = cv2.pointPolygonTest (contours[n],cnt, True )
    cv2.line(my_photo,center1,h,(255,0,0),2)
    if dist< min_dist:
        min_dist= dist

distances = []
print('cnt=',h)
print(min_dist)
print(contours[m])
def clik(event, x, y, flags, params,):
    if event == cv2.EVENT_LBUTTONDOWN:
        b = my_photo[y,x,0]
        g = my_photo[y,x,1]
        r = my_photo[y,x,2]
        print(f'{x},{y}')
        print(f'{b},{g},{r}\n')
        dist =cv2.pointPolygonTest(contours[0],(x,y),True)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(my_photo, f'{x},{y}',(x,y), font,1,(0,0,0),2)
        cv2.imshow('my_photo', my_photo)
        print('dist',dist)
    if event == cv2.EVENT_RBUTTONDOWN:
        b = my_photo[y,x,0]
        g = my_photo[y,x,1]
        r = my_photo[y,x,2]
        print(f'{x},{y}')
        print(f'{b},{g},{r}\n')
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(my_photo, f'{b},{g},{r}',(x,y), font,1,(0,0,0),2)
        cv2.imshow('my_photo', my_photo)

cv2.drawContours(my_photo, contours[m], -1, (0,255,0), 3)
cv2.imshow('my_photo', my_photo) # выводим итоговое изображение в окно
cv2.imshow('res', img_contours) # выводим итоговое изображение в окно
cv2.setMouseCallback('my_photo',clik)    
cv2.waitKey()
cv2.destroyAllWindows()
  