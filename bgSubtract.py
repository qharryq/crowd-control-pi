import numpy as np
import cv2
import imutils


cap = cv2.VideoCapture('example.avi')

fgbg = cv2.BackgroundSubtractorMOG()
kernel = np.ones((5,5),np.uint8)

while(1):
    ret, frame = cap.read()
    #frame = imutils.resize(frame, width=500)
    #fgmask = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    fgmask = fgbg.apply(frame, learningRate=.5)
    
    #fgmask = cv2.adaptiveThreshold(fgmask, 255
#, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    #fgmask = cv2.adaptiveThreshold(fgmask, 255
#, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
   # fgmask = cv2.threshold(fgmask,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

    #fgmask = cv2.blur(fgmask,(5,5))
    #fgmask = cv2.GaussianBlur(fgmask,(5,5),0)
    #fgmask = cv2.medianBlur(fgmask,5)

    #fgmask = cv2.erode(fgmask,kernel,iterations=1)
    #fgmask = cv2.dilate(fgmask,kernel,iterations=1)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

    img = fgmask
    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img =cv2.drawContours(frame,contours,-1, (0,255,0), 3)
    print len(contours)
    cv2.imshow('frame', fgmask)
    cv2.imshow('frame2', frame)
    #cv2.imshow('frame3', img)


    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
