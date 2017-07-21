import math
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
import cv2
import time
import pdb
from collections import defaultdict

np.set_printoptions(threshold='nan')
startTime = time.time()
log = open('eValues.txt', 'w')

# load image
image = cv2.imread('croppedAsteroid.jpg', cv2.IMREAD_GRAYSCALE)  #.astype(np.float32)

# Width and Height of Image
# height, width, channels = image.shape
height, width = image.shape

maxJ = 7
halfMaxJ = int(maxJ/2)
eValues = []

# imageBlurredDictionary[j] stores a copy of image blurred with a jxj gaussian kernel (used for memoization)
imageBlurredDictionary = [0] * (maxJ+1)
imageBlurredDictionary[1] = image
for j in range(3, maxJ+2, 2):
    imageBlurredDictionary[j] = cv2.GaussianBlur(image, (j, j), 0)


# returns vertical distance to closest top/bottom edge of the image (in number of rows)
# where vertical distance = number of cells in between the current row and the edge
def getRowDistanceToEdge(row):
    dist = min(row, height-row-1)

    if dist < 0:  # is this necessary?
        dist = 0

    return dist

# returns horizontal distance to closest left/right edge of the image (in number of colors)
# where horizontal distance = number of cells in between the current col and the edge
def getColDistanceToEdge(col):
    dist = min(col, height-col-1)

    if dist < 0:  # is this necessary?
        dist = 0

    return dist

Et_dictionary = {}
# Return Et score given p_v. Dictionary used for memoization.
def calcEt(pv):
    if pv in Et_dictionary:
        return Et_dictionary[pv]
    else:
        Et_dictionary[pv] = pv * math.log(pv, 2)
        return Et_dictionary[pv]

# Now getFilterSize scales linearly with j, not quadratically.
# Should be able to use bigger filters a lot more efficiently now if needed
def getFilterSize(row, col, j, prevFrequencyArrays):
    halfJ = int(j/2)

    frequencyArray = [0] * 256   # initialize frequencyArray with 0s
    if j==1:
        pass
    elif prevFrequencyArrays[j][1] == row-1 and prevFrequencyArrays[j][2] == col:  # if prev window was 1 row above us, same col
        # then we can use the adjacent memoized window frequency array + delta/change in rows
        # (1 row added, 1 subtracted) to calculate the new window
        oldFrequencyArray = prevFrequencyArrays[j][0]

        # get delta columns
        addedRow = image[row+halfJ, col-halfJ:col+halfJ+1]
        removedRow = image[row-halfJ-1, col-halfJ:col+halfJ+1]

        # update frequency array
        for add in addedRow:
            oldFrequencyArray[add] += 1
        for remove in removedRow:
            oldFrequencyArray[remove] -= 1
        frequencyArray = oldFrequencyArray

    else: # otherwise compute the window from scratch
        for x in range(-halfJ, halfJ + 1):
            for y in range(-halfJ, halfJ + 1):
                greyValue = image[row + y][col + x]
                frequencyArray[greyValue] += 1

    # memoize current window
    if j != 1:
        prevFrequencyArrays[j][0] = frequencyArray
        prevFrequencyArrays[j][1] = row
        prevFrequencyArrays[j][2] = col

    # compute the E_t score for the current j x j window
    Et = 0
    totalPixels = j**2
    for i in range(0, 256):
        pv = frequencyArray[i]/float(totalPixels)
        if pv == 0:
            continue
        else:
            Et += calcEt(pv)  # calculates E_t given pv, memoizes as well
    Et = -1 * Et
    if Et < 0:
        print("pv")
        print(pv)
        print("Et")
        print(Et)
        sys.exit()

    Et_threshold = 3.0
    if Et < Et_threshold:
        # print("kernel size: {0} for eValue {1}".format(j, Et))
        return j
    else:
        return getFilterSize(row, col, j-2, prevFrequencyArrays)


prevFrequencyArrays = [0] * (maxJ + 1)

for j in range(3, maxJ+2, 2):
    prevFrequencyArrays[j] = [None,0,0] # store Array, row, col

totalPixels = width*height
currentPixel = 0
adaptiveBlurred = np.zeros((height, width))  # TODO: col-row + change above in memoization part

for col in range(0, width):
    for row in range(0, height):
        # We correct maxJ for edge cases (constrained by the edge of the image)
        constrainedMaxJ = min(maxJ, 2*getRowDistanceToEdge(row)+1, 2*getColDistanceToEdge(col)+1)
        kernelSize = getFilterSize(row, col, constrainedMaxJ, prevFrequencyArrays)

        # print("kernelSize {0}".format(kernelSize))
        adaptiveBlurred[row][col] = imageBlurredDictionary[kernelSize][row][col]

        currentPixel += 1
        print("% Calculated: {0}".format(float(currentPixel*100)/totalPixels))

print("eValues")
print(eValues)
print("sum of evalues")
print(sum(eValues))
# plt.hist(eValues, bins='auto')
# plt.title("HISTOGRAM BB")
# plt.show()


dict = defaultdict(int)
for value in eValues:
    dict[value] += value
print("histogram dict")
print(dict)

endTime = time.time()
print("PROGRAM EXECUTION TIME: {0} seconds".format(endTime - startTime))

blurred = cv2.GaussianBlur(image, (21, 21), 0)
# Show Before Images
cv2.imshow('Image', image)
cv2.waitKey()

cv2.imshow('Blurred', blurred)
cv2.imwrite('cv2_gaussianBlur.jpg', blurred)
cv2.waitKey()

cv2.imwrite('adaptiveBlur.jpg', adaptiveBlurred)
