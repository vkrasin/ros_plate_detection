#!/usr/bin/env python

import cv2
import numpy as np
from matplotlib import pyplot as plt

def getMatch(kp_template, desc_template, img_target):
    # Convert target image to grayscale
    gray = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
    
    # Extract features with surf
    surf = cv2.xfeatures2d.SURF_create()

    # Get the keypoints and descriptors from the target
    kp_target, desc_target = surf.detectAndCompute(gray)
    
    # Match template and target
    bf = cv2.BFMatcher()

    matches = bf.knnMatch(des1, des2, k=2)
    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append([m])

    # Check if we found enough good matches
    if len(good) < 15:
         return 'not found'
    good = sorted(matches, key = lambda x:x[0].distance)
    sum = 0.0
    for g in range(0,15):
        sum += float(g[0].distance)

    sum /= float(15)

    if sum < 0.1:
        return 'found'
    return 'not found'
