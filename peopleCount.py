from collections import deque
import numpy as np
import cv2
import imutils
import argparse
import datetime
import time
import math
import sys
import requests
import json
import datetime
from requests.auth import HTTPBasicAuth 


'''class Point:
    def_init_(self,x,y):
        self.x = x
        self.y = y'''

class Person:
    #init should have two underscore after & before it but its working atm anyway cos i declare points list as empty later 
    def __init__(self):
        self.points = []
        self.assigned = True
        #id?
        #directionTravelling


class TrackingInfo:
    def __init__(self,distance,center,personPoint):
        self.distance = distance
        self.center = center
        self.personPoint = personPoint
        #perswonPoint is the last known coordinate of a person (prev frame) - acts as id for that person
        

def distance(p0, p1):
    return math.sqrt((p0[0]-p1[0])**2 +(p0[1]-p1[1])**2)

headers = {
    'Content-Type': 'application/json',
}



cap = cv2.VideoCapture('attic2.avi')
fgbg = cv2.BackgroundSubtractorMOG()
kernel = np.ones((5,5),np.uint8)
peopleList = []
personIn = 0
personOut = 0

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
    center = None #is this needed?
    temp = []
    tempPeopleList = []
    oldContours = []
    print "people list has length of %d" % len(peopleList)
    for c in contours:
        #print "should start here!"
        #print contourId
        
        area = cv2.contourArea(c)
        if area < 1200:
            continue
            #print cv2.contourArea(c)
    
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        (x,y,w,h) = cv2.boundingRect(c)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        cv2.circle(frame, center, 5, (0, 0, 255), -1)
        #print "people list has length of %d" % len(peopleList)
        #if len(peopleList) > 1:
            #sys.exit("error message ")
        
        #if there are no people currently being tracked, e.g for first view frames                   
        if not peopleList:
            #print "first person"
            p = Person()
            p.points = []
            p.points.append(center)
            p.assigned = True
            #print p.points[0]
            peopleList.append(p)
                        
        else:
            print "already people"
            for person in peopleList:
                p.assigned = False
                #print "here is a point"
                #print person.points[-1]
                #get distance between contour center and the last coordinate of each person currently being tracked
                #print center
                #print person.points[-1]
                d = distance(center, person.points[-1])
                #print d
                #threshold over which the objects in the 2 frames are too far apart to be the same object
                #add to temp if under
                if d < 35:
                    #print "less than 15"
                    t = TrackingInfo(d,center,person.points[-1])
                    temp.append(t)
                    #oldContours keeps track of contours which are linked to people from a previous frame
                    #print (c not in oldContours).all()
                    #if any(item not in oldContours for item in c):
                    if any(c in s for s in oldContours):
                    #if c not in oldContours:
                        pass
                    else:
                        oldContours.append(c)
                    

                
                
                    
    #is the contour did not make the oldContours list, it means they are not close enough to contours in previous frames to be considered the same people and thus must be a new person!
    #print "old contours = "
    #print oldContours
    for c in contours:
        area = cv2.contourArea(c)
        M = cv2.moments(c)
        center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
        if area < 1200:
            continue
        if any(c in s for s in oldContours):
            pass
        else:
            #print "while"
           #print c
            #print "not in old contours"
            p2 = Person()
            p2.points = []
            #doesnt have centre down here 
            p2.points.append(center)
            p2.assigned = True
            tempPeopleList.append(p2)
            
            #calculate distance between center and the last element of each array in arrayofarrays - find smallest - take note of which object  it is closest to - by array index & also the distance & center coordinate -
            #stores this info in temp array which is used below - temp.append() - maybe info should be heldf in object structure
            #if this distance is not below a certain threshold, create new - arrayofarrays.append([center])
            #Go through the temp array and starting by lowest distance, append each center to the array in arrayofarrays which it corresponds with
            #Will need a way to clean up objects which have left the frame - look at screenshot about greedy algorithm
    taken=[]

    #sort temp by smallest distance and match the contours with the people - starting with shortest distance
    sorted(temp, key=lambda trackingInfo: trackingInfo.distance)
    newTemp = temp
    count = 0
    while True:
        print "matching contours with people"
        exitFlag = False
        oldCount = count
        temp = newTemp
        for te in temp:
            if exitFlag == True:
                break
            #print te.distance
            #find the corresponding person to append their new coordinates to
            for p in peopleList:
                if te.personPoint == p.points[-1] :
                    p.points.append(te.center)
                    p.assigned = True
                    count += 1
                    print "count is %d" % count
                    print count
                    for i in xrange(len(newTemp) -1, -1, -1):
                        if newTemp[i].personPoint == p.points[-1] or te.center == newTemp[i].center:
                            del newTemp[i]
                        
                    print "cool"
                    exitFlag = True
                    break
                    #remove rremaining insatnces from newTemp that have same contour (center) or personPoint as the te that has just been appended to a person - might get tricky with loops here UNDERSTAND FULLY//
                    #need way of getting up to while true: in order to reassign newTemp to temp
        if count == oldCount:
            break

    #temp now just contains people who got no match (meaning they have left screen) & contours (represented by centroids) that have not been linked to previous person, meaning they are a new person! 
    
        
    
    for p2 in tempPeopleList:
        print "assigning temp people to actual peoplList"
        peopleList.append(p2)

    tempPeopleList = []
    #gets rid of people who have left the frame
    print "getting rid of people who have left the frame"
    tempPeopleList = [p for p in peopleList if p.assigned == True]
    peopleList = tempPeopleList

    #IDK if there's still people left in temp at the end of loop that need to be dealt with?? factor to keep in mind if things don't work as they should        

    #Now to determine the if a person has crossed the line and if so - in what direction: in or out
    for person in peopleList:
        #check if the person has been in more than one frame
        if len(person.points) > 1:
            #get last coordinate of person
            x, y = person.points[-1]
            #get coordinate of person in frame before that
            x1, y1 = person.points[-2]
            #determines whether the person has crossed the line using their last 2 coordinates and in what direction they are travelling
            if y < 75 and y1 > 75:
                personIn +=1
                timeStamp = str(datetime.datetime.now().isoformat())
                dataIn = {"timestamp" : timeStamp, "peopleIn" : "1", "peopleOut" : "0", "venue" : "http://ccwebapp-env.eu-west-1.elasticbeanstalk.com/venues/6"}
                payload = json.dumps(dataIn)
                requests.post('http://ccwebapp-env.eu-west-1.elasticbeanstalk.com/timestamps', headers = headers, data = payload, auth=HTTPBasicAuth('qharryq@hotmail.com', 'sdsd'))
            elif y > 75 and y1 < 75:
                personOut+=1
                timeStamp = str(datetime.datetime.now().isoformat())
                dataOut = {"timestamp" : timeStamp, "peopleIn" : "0", "peopleOut" : "1", "venue" : "http://ccwebapp-env.eu-west-1.elasticbeanstalk.com/venues/6"}
                payload = json.dumps(dataOut)
                requests.post('http://ccwebapp-env.eu-west-1.elasticbeanstalk.com/timestamps', headers = headers, data = payload, auth=HTTPBasicAuth('qharryq@hotmail.com', 'sdsd'))
                
    personInStr = str(personIn)
    personOutStr = str(personOut)
   
    #img =cv2.drawContours(frame,contours,-1, (0,255,0), 3)
    #draw line intersecting frame, this is the line a person must cross for them to register as entering/exiting
    cv2.line(frame, (0,75), (300,75), (255,255,255))
    #print num people in and out to screen
    cv2.putText(frame,personInStr,(30,50),cv2.FONT_HERSHEY_SIMPLEX,2,255)
    cv2.putText(frame,personOutStr,(30,200),cv2.FONT_HERSHEY_SIMPLEX,2,255)
    cv2.imshow('frame', fgmask)
    cv2.imshow('frame2', frame)
    
    #print pts[0]
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()
