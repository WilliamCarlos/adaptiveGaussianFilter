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


imageBlurredDictionary = [0] * 28  # initialize imageBlurredDictionary with 28 indices set to 0
imageBlurredDictionary[1] = image
imageBlurredDictionary[3] = cv2.GaussianBlur(image, (3, 3), 0)
imageBlurredDictionary[5] = cv2.GaussianBlur(image, (5, 5), 0)
imageBlurredDictionary[7] = cv2.GaussianBlur(image, (7, 7), 0)
imageBlurredDictionary[9] = cv2.GaussianBlur(image, (9, 9), 0)
imageBlurredDictionary[11] = cv2.GaussianBlur(image, (11, 11), 0)
imageBlurredDictionary[13] = cv2.GaussianBlur(image, (13, 13), 0)
imageBlurredDictionary[15] = cv2.GaussianBlur(image, (15, 15), 0)
imageBlurredDictionary[17] = cv2.GaussianBlur(image, (17, 17), 0)
imageBlurredDictionary[19] = cv2.GaussianBlur(image, (19, 19), 0)
imageBlurredDictionary[21] = cv2.GaussianBlur(image, (21, 21), 0)
imageBlurredDictionary[23] = cv2.GaussianBlur(image, (23, 23), 0)
imageBlurredDictionary[25] = cv2.GaussianBlur(image, (25, 25), 0)
imageBlurredDictionary[27] = cv2.GaussianBlur(image, (27, 27), 0)

# Width and Height of Image
# height, width, channels = image.shape
height, width = image.shape

maxJ = 7
halfMaxJ = int(maxJ/2)
eValues = []


# Now getFilterSize scales linearly with j, not quadratically. Should be able to use bigger filters a lot more efficiently now if needed
def getFilterSize(row, col, j, prevFrequencyArrays):
    halfJ = int(j/2)

    frequencyArray = [0] * 256   # initialize frequencyArray with 0s
    if j==1:
        pass
    elif prevFrequencyArrays[j][1] == row-1 and prevFrequencyArrays[j][2] == col:  # if prev window was 1 row above us, same col
        # then we can use the adjacent memoized window frequency array + delta in rows (1 row added, 1 subtracted) to calculate the new window
        # print("J is {0}".format(j))
        oldFrequencyArray = prevFrequencyArrays[j][0]

        # TODO: check array slicing --Looks good
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
    if j!=1:
        prevFrequencyArrays[j][0] = frequencyArray
        prevFrequencyArrays[j][1] = row
        prevFrequencyArrays[j][2] = col

    Et = 0
    totalPixels = j**2
    for i in range(0, 256):
        pv = frequencyArray[i]/float(totalPixels)
        if pv == 0:
            continue
        else:
            Et += pv*math.log(pv, 2)  # maybe memoize this later
    Et = -1 * Et  # TODO: how is this sometimes outputting negative numbers?

    Et_threshold = 3.0
    if Et < Et_threshold:
        # print("kernel size: {0} for eValue {1}".format(j, Et))
        return j
    else:
        return getFilterSize(row, col, j-2, prevFrequencyArrays)  # TODO:hardcode


prevFrequencyArrays = [0] * (maxJ + 1)
prevFrequencyArrays[3] = [None,0,0]  # store Array, row, col
prevFrequencyArrays[5] = [None,0,0]
prevFrequencyArrays[7] = [None,0,0]  # TODO: hardcoded

totalPixels = width*height
currentPixel = 0
adaptiveBlurred = np.zeros((height, width))  # TODO: col-row + change above in memoization part

for col in range(halfMaxJ, width-halfMaxJ):
    for row in range(halfMaxJ, height-halfMaxJ):
        kernelSize = getFilterSize(row, col, maxJ, prevFrequencyArrays)

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