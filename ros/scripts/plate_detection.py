#!/usr/bin/env python

import cv2
import numpy as np
from matplotlib import pyplot as plt

def getMatch(kp_template, des_template, img_target):
    # Convert target image to grayscale
    gray = cv2.cvtColor(img_target,cv2.COLOR_BGR2GRAY)
    
    # Extract features with surf
    surf = cv2.xfeatures2d.SURF_create()

    # Get the keypoints and descriptors from the target
    kp_target, des_target = surf.detectAndCompute(gray,None)
    
    # Match template and target
    bf = cv2.BFMatcher()

    matches = bf.knnMatch(des_template, des_target, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.6*n.distance:
            good.append([m])

    # Check if we found enough good matches
    if len(good) < 15:
         return 'not found'+str(len(good))
    good = sorted(matches, key = lambda x:x[0].distance)
    sum = 0.0
    for i in range(0,15):
        sum += float(good[i][0].distance)

    sum /= float(15)

    if sum < 0.1:
        return 'found '+str(sum) + ' ' + str(len(good))
    return 'not found '+str(sum) + ' ' + str(len(good))
