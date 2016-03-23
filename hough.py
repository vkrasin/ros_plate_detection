import cv2
import numpy as np
import math

def dist(circle1, circle2):
    x1 = float(circle1[0])
    y1 = float(circle1[1])
    x2 = float(circle2[0])
    y2 = float(circle2[1])
    return math.sqrt( (x1-x2) ** 2 + (y1-y2) ** 2)
    #return math.sqrt( (circle1[0] - circle2[0])*(circle1[0]-circle2[0])  + (circle1[1] - circle2[1])*(circle1[1] - circle2[1]) )

def ratio(circle1, circle2):
    return circle2[2] / float(circle1[2])

img = cv2.imread('cam_test5.jpg',0)
#img = cv2.medianBlur(img,5)
img = cv2.blur(img, (3,3))
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
img = cv2.Canny(img,40,60)

circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,2,40,param1=50,param2=45,minRadius=4,maxRadius=170)

if circles == None:
    print 'no circles found'



circles = np.uint16(np.around(circles))
print type(circles)
print type(circles[0][0])
good = np.array([[[1,2,3]]])
good = []
print type(good)

match_number_1 = 0
match_number_2 = 0
match_number_3 = 0
for i in range(0,len(circles[0])):
    small_match = 0
    big_match = 0
    for j in range(i+1,len(circles[0])):
        c1 = circles[0][i]
        c2 = circles[0][j]
        if (c1[2] > c2[2]):
            circle1 = c2
            circle2 = c1
        else:
            circle1 = c1
            circle2 = c2
        #print 'distance = %f' % dist(circle1, circle2)
        distance = dist(circle1,circle2)/float(circle1[2])
        circle_ratio = ratio(circle1, circle2)
        # Check if we found a match between the big circle and an outer circle
        if (circle_ratio < 7 and circle_ratio > 4 and distance < 18 and distance > 12):
            match_number_1 += 1
            #print 'Possible match 1 found'
            #print circle1
            #print circle2

            #print 'distance = %f' % distance
            #print 'distance2 = %f' % dist(circle1,circle2)
        if (circle_ratio < 7 and circle_ratio > 4 and distance < 9 and distance > 6):
            match_number_2 += 1
            #print 'Possible match 2 found'
            #print circle1
            #print circle2

            #print 'distance = %f' % distance
            #print 'distance2 = %f' % dist(circle1,circle2)
        if (circle1[2] < 20 and circle_ratio < 1.2 and circle_ratio > 0 and distance < 25 and distance > 10):
            match_number_3 += 1
            small_match += 1
            #print 'Possible match 3 found'
            #print circle1
            #print circle2

            #print 'distance = %f' % distance
            #print 'distance2 = %f' % dist(circle1,circle2)

    if (small_match > 1):
        print 'small matches for this circle = %d' % small_match
        print circles[0][i]





for i in circles[0,:]:
    # draw the outer circle
    cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

"""
print circles
for c in circles[0]:
    print "x %d y %d r %d" % (c[0], c[1], c[2])
"""

#print "circles " + str(len(good[0]))
print len(circles[0])
print 'Number of possible matches_1 %d' % match_number_1
print 'Number of possible matches_2 %d' % match_number_2
print 'Number of possible matches_3 %d' % match_number_3

cv2.imshow('detected circles',img)
cv2.imwrite('circles1.jpg',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
