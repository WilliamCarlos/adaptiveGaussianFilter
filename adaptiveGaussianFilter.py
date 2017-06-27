# import cv2
# import cv3
import math
import seaborn as sns
import matplotlib.pyplot as plt
import sys
import numpy as np
# sys.path.append('/usr/local/opt/opencv3/lib/python2.7/site-packages/')
import cv2
import time
from collections import defaultdict


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

print(image)

# j = 9
# halfJ = int(j/2)

maxJ = 27
halfMaxJ = int(maxJ/2)
eValues = []

np.set_printoptions(threshold='nan')


def getPixel(row, col, kernelSize):  # better practice to use case switch here?
    if kernelSize == 1:
        # no blur
        print("kernelsize: 1")
        return image[row][col]
    elif kernelSize == 3:
        print("kernelsize: 3")
        return imageBlurred3[row][col]
    elif kernelSize == 5:
        print("kernelsize: 5")
        return imageBlurred5[row][col]
    elif kernelSize == 7:
        print("kernelsize: 7")
        return imageBlurred7[row][col]
    elif kernelSize == 9:
        print("kernelsize: 9")
        return imageBlurred9[row][col]
    elif kernelSize == 11:
        print("kernelsize: 11")
        return imageBlurred11[row][col]
    elif kernelSize == 13:
        print("kernelsizse: 13")
        return imageBlurred13[row][col]
    elif kernelSize == 15:
        print("kernelsize: 15")
        return imageBlurred15[row][col]
    elif kernelSize == 17:
        print("kernelsize: 17")
        return imageBlurred17[row][col]
    elif kernelSize == 19:
        print("kernelsize: 19")
        return imageBlurred19[row][col]
    elif kernelSize == 21:
        print("kernelsize: 21")
        return imageBlurred21[row][col]
    elif kernelSize == 23:
        print("kernelsize: 23")
        return imageBlurred23[row][col]
    elif kernelSize == 25:
        print("kernelsize: 25")
        return imageBlurred25[row][col]
    elif kernelSize == 27:
        print("kernelsize: 27")
        return imageBlurred27[row][col]
    else:
        print("Uh oh. Unexpected kernel size passed to getPixel")
        return
# # returns optimal filter size s where 0<s<j
# # TODO: can heavily optimize this. Kernel slides over by one. Look at the delta in columns (1 column gained, 1 lost).
# # TODO: can update frequencyArray in 2*j operations instead of j^2 operations.
# def getFilterSize(row, col, j):
#     # initialize frequencyArray with 0s
#     frequencyArray = []
#     for i in range(0, 256):
#         frequencyArray.append(0);
#
#     for x in range(-halfJ, halfJ+1):
#         for y in range(-halfJ, halfJ+1):
#             greyValue = image[row + y][col + x]
#             # print "indexing [{0},{1}] from center pixel [{2},{3}]".format(row+y, col+x, row, col)
#             frequencyArray[greyValue] += 1
#
#     Et = 0
#     totalPixels = j**2
#     for i in range(0, 256):
#         pv = frequencyArray[i]/float(totalPixels)
#         if pv == 0:
#             continue  # this was break before!
#         else:
#             # print("non-zero pv {0} which leads to a pv*ld(pv) of {1}").format(pv, (pv*math.log(pv,2)))
#             Et += pv*math.log(pv, 2)  # maybe memoize this later
#
#     Et = -1 * Et
#     if Et == 0:
#         # print("0 kernel")
#         # print image[0:20, 0:20]  # why isn't it [0:20][0:20]?
#         print("frequencyArray")
#         print(frequencyArray)
#
#     # print("new eValue {0}").format(Et)
#     log.write(str(Et))
#     log.write('\n')
#     eValues.append(Et)


# global variable wat
# global nonZeroEt
# nonZeroEt = 0



def getFilterSize(row, col, j):
    halfJ = int(j/2)

    # initialize frequencyArray with 0s
    frequencyArray = [0] * 256

    for x in range(-halfJ, halfJ+1):
        for y in range(-halfJ, halfJ+1):
            greyValue = image[row + y][col + x]
            # print "indexing [{0},{1}] from center pixel [{2},{3}]".format(row+y, col+x, row, col)
            frequencyArray[greyValue] += 1

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
    # if j < 2:
    #     print("REACHED BOTTOM OF RECURSIVE STACK WITHOUT GETTING BELOW THRESHOLD, RETURNING 1")  # e.g. no blur
    #     return 1
    if Et < Et_threshold:
        print("kernel size: {0} for eValue {1}".format(j, Et))
        return j
    else:
        return getFilterSize(row, col, j-2)  # TODO:hardcode


totalPixels = width*height
currentPixel = 0
adaptiveBlurred = np.zeros((height, width))
for col in range(halfMaxJ, width-halfMaxJ):
    for row in range(halfMaxJ, height-halfMaxJ):
        kernelSize = getFilterSize(row, col, maxJ)
        print("kernelSize {0}".format(kernelSize))
        # adaptiveBlurred[row][col] = getPixel(row, col, kernelSize)
        adaptiveBlurred[row][col] = imageBlurredDictionary[kernelSize][row][col]

        # print("calculated {0}".format(height*col + row))
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