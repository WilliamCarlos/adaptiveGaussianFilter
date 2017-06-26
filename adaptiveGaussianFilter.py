# import cv2
# import cv3
import math
import seaborn as sns
import matplotlib.pyplot as plt

import sys
import numpy as np
# sys.path.append('/usr/local/opt/opencv3/lib/python2.7/site-packages/')


import cv2

from collections import defaultdict

log = open('eValues.txt', 'w')

np.zeros(3)

import sys
import pdb

# load image
image = cv2.imread('croppedAsteroid.jpg', cv2.IMREAD_GRAYSCALE)  #.astype(np.float32)

# Width and Height of Image
# height, width, channels = image.shape
height, width = image.shape

print(image)

j = 9
halfJ = int(j/2)
eValues = []

np.set_printoptions(threshold='nan')

# returns optimal filter size s where 0<s<j
# TODO: can heavily optimize this. Kernel slides over by one. Look at the delta in columns (1 column gained, 1 lost).
# TODO: can update frequencyArray in 2*j operations instead of j^2 operations.
def getFilterSize(row, col, j):
    # initialize frequencyArray with 0s
    frequencyArray = []
    for i in range(0, 256):
        frequencyArray.append(0);

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
            continue  # this was break before!
        else:
            # print("non-zero pv {0} which leads to a pv*ld(pv) of {1}").format(pv, (pv*math.log(pv,2)))
            Et += pv*math.log(pv, 2)  # maybe memoize this later

    Et = -1 * Et
    if Et == 0:
        # print("0 kernel")
        # print image[0:20, 0:20]  # why isn't it [0:20][0:20]?
        print("frequencyArray")
        print(frequencyArray)

    # print("new eValue {0}").format(Et)
    log.write(str(Et))
    log.write('\n')
    eValues.append(Et)


for col in range(halfJ, width-halfJ):
    for row in range(halfJ, height-halfJ):
        getFilterSize(row, col, j)

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

sns.distplot(eValues)



# break;
# def getFilterSize(row, col, j):
#     # initialize frequencyArray with 0s
#     frequencyArray = []
#     for i in range(0, 256):
#         frequencyArray.append(0);
#
#     #TODO: implement j
#     for x in range(-halfJ, halfJ+1):
#         for y in range(-halfJ, halfJ+1):
#             greyValue = image[row + y][col + x]
#             # print "indexing [{0},{1}] from center pixel [{2},{3}]".format(row+y, col+x, row, col)
#             frequencyArray[greyValue] += 1
#
#     Et = 0
#     for i in range(0, 256):
#         pv = frequencyArray[i]/(j**2)
#         Et += pv*math.log(pv, 2)
#     Et = -1 * Et
#
#     Et_threshold = 0.5
#     if j < 2:
#         return None
#     elif Et < Et_threshold:
#         return j
#     else:
#         return getFilterSize(row, col, j-2)



# sns.lmplot(x="eValue", y="Frequency", data=eValues)

#frequncyArray now holds the correct histogram


# normalized centered 2d gaussian within ranges +- 2sigma

# Threshold value E_t = sigma_j * p_v * ld * p_v (in bit)

# pv = relative frequency of gray value v in test window size j (fraction of pixels w/ grey value v in test window j)
# ld = dyadic logarithm

# 2 pixel stepsize decreasing window size

#dyadic logarithm = logarithm base 2





blurred = cv2.GaussianBlur(image, (21, 21), 0)
# Show Before Images
cv2.imshow('Image', image)
cv2.waitKey()

cv2.imshow('Blurred', blurred)
cv2.waitKey()