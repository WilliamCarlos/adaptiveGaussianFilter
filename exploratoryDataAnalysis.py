import numpy as np
import matplotlib.pyplot as plt
import sys

j = 9

eValuesFile = open("eValues_{0}.txt".format(j), 'r')
# print(eValuesFile.readline())

data = []
for line in eValuesFile:
    line = line[:-2]
    data.append(float(line))

# print("data")
# print(data)

plt.hist(data, bins=20)
plt.title("Distribution of eValues for j={0}".format(j))
plt.ylim([0, 170000])
plt.xlim([3, 7.5])
plt.show()