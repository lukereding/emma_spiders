import cv2
import numpy as np
import sys
from math import sqrt
from os.path import basename

def pairwise_distance(locations):
    """Return pairwise distances between all (x,y) points in locations."""
    loc = locations
    # returns None if there's only one location.
    if len(loc) == 1:
        return None
    else:
        distances = []
        while len(loc) >= 2:
            last_location = loc.pop()
            # probably a better way to do this that doesn't require nesting a list
            distances.append([distance(last_location, i) for i in loc])
        distances = sum(distances, [])
        return distances
        # return reduce(lambda x, y: x + y, distances) / len(distances)


# function to find distance in two dimensions
def distance(x,y):
    """Return distance between x and y."""
    d = sqrt((y[0] - x[0])**2 + (y[1] - x[1])**2)
    return round(d, 3)

name = basename(sys.argv[1].split('.')[0])
print "name : {}".format(name)

# import in photo
photo = cv2.imread(sys.argv[1])

# GaussianBlur
blur = cv2.GaussianBlur(photo, (0,0), 15)

cv2.imwrite("blur.jpg", blur)

# threshold for dark areas
threshold = cv2.adaptiveThreshold(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,31,1)
# ret, threshold = cv2.threshold(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY), 80, 255, cv2.THRESH_BINARY)
cv2.imwrite("threshold.jpg", threshold)

# get blobs of a certain size
contours = cv2.findContours(threshold, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[0]

potential_contours = []
for c in contours:
    # find area, extent
    area = cv2.contourArea(c)
    x,y,w,h = cv2.boundingRect(c)
    aspect_ratio = float(w)/h
    if area > 500 and area < 3000 and aspect_ratio > .5 and aspect_ratio < 2:
        potential_contours.append(c)

largest = sorted(potential_contours, key=cv2.contourArea, reverse=True)[:6]

# get centroids:
centroids = []
for c in largest:
    m = cv2.moments(c)
    centroids.append((int(m['m10'] / m['m00']), int(m['m01'] / m['m00'])))

# draw contours, centroids on image
cv2.drawContours(photo, largest, -1, (50,50,200), -1)
for center in centroids:
    cv2.circle(photo, center, 6, (200,180,72), -1)

# get distances
distances = pairwise_distance(centroids)
cv2.putText(photo, str(round(sum(distances) / len(distances),2)), (200,200), cv2.FONT_HERSHEY_SIMPLEX, 4, (50,50,200))

cv2.imwrite("out_{}.jpg".format(name), photo)
