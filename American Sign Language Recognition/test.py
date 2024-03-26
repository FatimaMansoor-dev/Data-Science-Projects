import math
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
import time
from cvzone.ClassificationModule import Classifier

imgSize = 300
offset = 20  ## the cropped image was not taking complete hand, so adding the area
cap = cv2.VideoCapture(0)  # webcam
detector = HandDetector(maxHands=1)
classifier = Classifier("Model/keras_model.h5", 'Model/labels.txt')
label =['A', 'B', 'C', 'D', 'E']

while True:  #continuosly takes video input
    success, img = cap.read()

    imgOutput = img.copy()

    hands, img = detector.findHands(img) # hands is a list with either 1 hand, or no hand
    # if hand detected
    if hands:
        hand = hands[0] # now hand is a dict storing information about hand
        x,y,w,h = hand['bbox'] # bbox = bounding box

        imgwhite = np.ones((imgSize,imgSize,3),np.uint8)*255  # make a matrix of all ones, size 300x300x3. this is for images. *255 for white
        imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]

        imgcrop_shape = imgCrop.shape # returns h,w,channel

        aspect_ratio = h/w # checking what is greater

        if aspect_ratio>1:
            k = imgSize/h ## k is basically a number that we multiply h and w with to make h=300
            w = math.ceil(k*w)
            imgResize = cv2.resize(imgCrop, (w,imgSize)) # w=new width, h=300
            imgResizeShape = imgResize.shape

            # to set image in centre horizontally
            marginleft = math.ceil((imgSize-w)/2)   # total width me se imgwidth ko minus kaardo. jo bachay woh gap hai tw usko half krdo.

            # fitting cropped img inside wite img
            imgwhite[:, marginleft:w+marginleft] = imgResize  # height full 300, w ko margin se start kro aur w+margin tak lekr jao. so it is centered
            prediction, index = classifier.getPrediction(imgwhite)
            print(prediction, index)
        else:
            k = imgSize/w
            h = math.ceil(k*h)
            imgResize = cv2.resize(imgCrop, (imgSize,h))  # w,h
            imgResizeShape = imgResize.shape

            # to set image in centre vertically
            margintop = math.ceil((imgSize-h)/2)   # total width me se imgheightko minus kaardo. jo bachay woh gap hai tw usko half krdo.

            # fitting cropped img inside wite img
            imgwhite[margintop:h+margintop, :] = imgResize

            prediction, index = classifier.getPrediction(imgwhite)
            print(prediction, index)

        cv2.putText(imgOutput, label[index], (x,y-offset), cv2.FONT_HERSHEY_COMPLEX,2, (255,0,255),2)
        cv2.imshow("ImageCrop", imgOutput)
        cv2.imshow("ImageWhite", imgwhite)

    cv2.imshow("image",img)
    cv2.waitKey(1)

