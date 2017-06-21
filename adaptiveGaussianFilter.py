import cv2
import numpy as np
import sys
import pdb

#load image
image = cv2.imread('asteroid.jpg') #.astype(np.float32)

# Width and Height of Image
height, width, channels = image.shape

blurred = cv2.GaussianBlur(image, (21, 21), 0)
# Show Before Images
cv2.imshow('Image', image)
cv2.waitKey()

cv2.imshow('Blurred', blurred)
cv2.waitKey()