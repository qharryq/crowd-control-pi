from collections import deque
import numpy as np
import cv2
import imutils
import argparse
import datetime
import time


cap = cv2.VideoCapture('attic2.avi')
fgbg = cv2.BackgroundSubtractorMOG()
kernel = np.ones((5,5),np.uint8)
arrayofarrays = []
while(1):
    ret, frame = cap.read()
    width, height = frame.shape[:2]

    fgmask = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

    #frame = imutils.resize(frame, width=500)
    #fgmask = cv2.threshold(fgmask, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1] Look at otsu thresholding if you have time! might be more accurate
    fgmask = fgbg.apply(fgmask)
    #add leaningRate flag above if you're getting things in background which shouldnt be - but it makes people less solid

    #fgmask = cv2.threshold(fgmask, 1, 255, cv2.THRESH_BINARY)[1]
    #fgmask = cv2.adaptiveThreshold(fgmask,255
#,cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY,11,2)
    #fgmask = cv2.adaptiveThreshold(fgmask, 255
#, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,11,2)
    #ret, fgmask = cv2.threshold(fgmask,127,255,0)
    fgmask = cv2.GaussianBlur(fgmask,(5,5),0)

    fgmask = cv2.erode(fgmask,None,iterations=2)
    #fgmask = cv2.erode(fgmask,kernel,iterations=1)
    fgmask = cv2.dilate(fgmask,None,iterations=2)
    #fgmask = cv2.blur(fgmask,+-(5,5))
    #fgmask = cv2.medianBlur(fgmask,5)
    #fgmask = cv2.dilate(fgmask,kernel,iterations=1)

    
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_OPEN, kernel)
    #fgmask = cv2.morphologyEx(fgmask, cv2.MORPH_CLOSE, kernel)

    #fgmask = cv2.Canny(fgmask, 225, 250)

    #img = fgmask
    contours, hierarchy = cv2.findContours(fgmask.copy(),cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    #this array handles if there are multiple contours in the first frame containing contours
    center = None
    if len(contours) > 0:
        if not arrayofarrays:
            for c in contours:
                area = cv2.contourArea(c)
                if area < 1000:
                    continue
                    #print cv2.contourArea(c)
        
                M = cv2.moments(c)
                center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                arrayofarrays.append([center])
                print arrayofarrays
        else:
            temp = []
            for c in contours:
                area = cv2.contourArea(c)
                if area < 1000:
                    continue
                    #print cv2.contourArea(c)
        
                M = cv2.moments(c)
                center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
                #calculate distance between center and the last element of each array in arrayofarrays - find smallest - take note of which object  it is closest to - by array index & also the distance & center coordinate -
                #stores this info in temp array which is used below - temp.append() - maybe info should be heldf in object structure
                #if this distance is not below a certain threshold, create new - arrayofarrays.append([center])
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
            #Go through the temp array and starting by lowest distance, append each center to the array in arrayofarrays which it corresponds with
            #Will need a way to clean up objects which have left the frame - look at screenshot about greedy algorithm
        #img =cv2.drawContours(frame,contours,-1, (0,255,0), 3)
    cv2.line(frame, (0,75), (300,75), (255,255,255))
    cv2.imshow('frame', fgmask)
    cv2.imshow('frame2', frame)
    
    #print pts[0]
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
