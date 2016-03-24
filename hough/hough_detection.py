import cv2
import numpy as np
import math

# Calculates the euclidian distance between two circles
def dist(circle1, circle2):
    x1 = float(circle1[0])
    y1 = float(circle1[1])
    x2 = float(circle2[0])
    y2 = float(circle2[1])
    return math.sqrt( (x1-x2) ** 2 + (y1-y2) ** 2)

# Calculates the ratio between to values, output always > 1
def ratio(val1, val2):
    if val1 > val2:
        return float(val1) / val2
    else:
        return float(val2) / val1

# Calculates the ratio between the radii of two circles, output always > 1
def ratio2(circle1, circle2):
    return ratio(circle1[2], circle2[2])

# Calculates the ratios between the radii of three circles
# will output the biggest ratio, output always > 1
def ratio3(circle1, circle2, circle3):
    r1 = ratio2(circle1,circle2)
    r2 = ratio2(circle1,circle3)
    r3 = ratio2(circle2,circle3)
    ratios = sorted([r1,r2,r3])
    return ratios[2]

# Extracts the circles out of an image
def extract_circles(target_img):
    target_img = cv2.blur(target_img, (3,3))
    target_img = cv2.Canny(target_img,40,60)
    circles = cv2.HoughCircles(target_img,cv2.HOUGH_GRADIENT,2,80,param1=60,param2=50,minRadius=4,maxRadius=170)
    return circles

def forms_triangle(c1,c2,c3,distance_treshold):
    dist1 = dist(c1, c2)
    dist2 = dist(c1, c3)
    dist3 = dist(c2, c3)
    distance_treshold2 = 1.04
    if (ratio(dist1,dist2) < distance_treshold and ratio((dist3 / math.sqrt(2.0)),dist1) < distance_treshold):
        if ratio(math.sqrt(dist1 ** 2 + dist2 ** 2), dist3) < distance_treshold2:
            print math.sqrt(dist1 ** 2 + dist2 ** 2), '=', dist3
            return True, 1 
    if (ratio(dist1,dist3) < distance_treshold and ratio((dist2 / math.sqrt(2.0)),dist1) < distance_treshold):
        if ratio(math.sqrt(dist1 ** 2 + dist3 ** 2), dist2) < distance_treshold2:
            print math.sqrt(dist1 ** 2 + dist3 ** 2), '=', dist2
            return True, 2 
    if (ratio(dist2,dist3) < distance_treshold and ratio((dist1 / math.sqrt(2.0)),dist2) < distance_treshold):
        if ratio(math.sqrt(dist2 ** 2 + dist3 ** 2), dist1) < distance_treshold2:
            print math.sqrt(dist2 ** 2 + dist3 ** 2), '=', dist1
            return True, 2 

    return False, 0

# Finds right-angled triangles where the end points are circles with similar radii
def find_triangles(circles, radius_treshold, distance_treshold):
    circles = np.uint16(np.around(circles))

    triangles = []

    for i in range(0,len(circles[0])):
        for j in range(i+1,len(circles[0])):
            c1 = circles[0][i]
            c2 = circles[0][j]
            # Check if both circles have the same radius and do not intersect
            if ratio2(c1,c2) < radius_treshold and dist(c1,c2) > 2*c2[2]:
                for k in range(j+1,len(circles[0])):
                    c3 = circles[0][k]
                    # Check if the third circle has the same radius
                    ratio1 = ratio3(c1,c2,c3)
                    if ratio1 < radius_treshold and ratio > (1.0 / radius_treshold):
                        # Check if the circles form a right-angled triangle
                        b, triangle_type = forms_triangle(c1,c2,c3,distance_treshold)
                        if (b):
                            good_triangle = (triangle_type == 2 or triangle_type == 1) and (16 > ratio(dist(c1,c2),c1[2]) > 10 or 28 > ratio(dist(c1,c2),c1[2]) > 19)
                            good_triangle = good_triangle or triangle_type == 3 and (16 > ratio(dist(c2,c3),c1[2]) > 10 or 28 > ratio(dist(c2,c3),c1[2]) > 19)
                            
                                
                            print 'triangle found, type = %d' % triangle_type
                            print 'good triangle ?', good_triangle
                            print c1, c2, c3

                            # Add the triangle to our possible matches
                            if good_triangle:
                                triangle = [c1, c2, c3]
                                triangles.append(triangle)

    triangles = sorted(triangles, key=lambda x:x[0][2])
    return triangles


    


# Test the functions and display the result
img = cv2.imread('cam_test4.jpg',0)
cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

circles = extract_circles(img)

if circles == None:
    print 'no circles found'




circles = np.uint16(np.around(circles))

# By how much radii and distances can differ
radius_treshold = 1.5
distance_treshold = 1.5

matches = find_triangles(circles, radius_treshold, distance_treshold)


for i in circles[0,:]:
    # draw the outer circle
    #cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)


# Draw all matches in dark red
for triangle in matches:
    for c in triangle:
        cv2.circle(cimg,(c[0],c[1]),c[2],(0,0,100),2)

for tri in matches:
    cv2.line(cimg,(tri[0][0], tri[0][1]),(tri[1][0],tri[1][1]),(0,255,0),1)
    cv2.line(cimg,(tri[2][0], tri[2][1]),(tri[1][0],tri[1][1]),(0,255,0),1)
    cv2.line(cimg,(tri[0][0], tri[0][1]),(tri[2][0],tri[2][1]),(0,255,0),1)

# Draw match with smallest radii in red
# Draw match with 2nd smallest radii in orange and slighty bigger
if len(matches) > 1:
    for c in matches[0]:
        cv2.circle(cimg,(c[0],c[1]),c[2],(0,0,255),2)
    for c in matches[1]:
        cv2.circle(cimg,(c[0],c[1]),c[2]+10,(0,128,255),2)
#print circles
for triangle in matches:
    print '+++++++'
    for c in triangle:
        print "x %d y %d r %d" % (c[0], c[1], c[2])


#print "circles " + str(len(good[0]))
print len(circles[0])

print len(matches)

#print matches

#cv2.imshow('detected circles',img)
cv2.imshow('circles',cimg)
#cv2.imwrite('circles1.jpg',cimg)
cv2.waitKey(0)
cv2.destroyAllWindows()
