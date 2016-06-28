import cv2
import numpy as np
import sys

name = sys.argv[1].split('.')[0]

# import in photo
photo = cv2.imread(sys.argv[1])

# GaussianBlur
blur = cv2.GaussianBlur(photo, (0,0), 15)

cv2.imwrite("blur.jpg", blur)

# threshold for dark areas
threshold = cv2.adaptiveThreshold(cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY),255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,35,2)
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
    if area > 600 and area < 3000 and aspect_ratio > .5 and aspect_ratio < 2:
        potential_contours.append(c)


cv2.drawContours(photo, potential_contours, -1, (200,180,72), -1)

cv2.imwrite("out_{}.jpg".format(name), photo)
