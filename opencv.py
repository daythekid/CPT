import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier("face.xml")

camera = cv2.VideoCapture(0)

while True:
    ret,img = camera.read()
    #Converts video feed to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)

    for (x,y,w,h) in faces:
        position = x+(w/2)
        print(position)

camera.release()
cv2.distoryAllWindows()
