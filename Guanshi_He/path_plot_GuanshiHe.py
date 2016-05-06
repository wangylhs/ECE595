#Guanshi He (he95)
#Plot the input data server vs. paths number

import random
import matplotlib.pyplot as plt
import sys

targetwebsite = []
pathnum = []
with open('path_us') as f:
	databox = f.readline()
	while databox:

		targetwebsite.append(databox.split()[0])
		print databox.split()[1]
		pathnum.append(int(databox.split()[1]))

		databox = f.readline()

print targetwebsite
print pathnum
l1 = []
for i in range(0,len(targetwebsite)): l1.append(i)
plt.figure(1)
plt.plot(l1,pathnum)
plt.xticks(l1,targetwebsite,rotation = 90)
plt.ylabel('# of paths')
plt.title('Servers(US) vs. # of paths')
plt.show()

targetwebsite1 = []
pathnum1 = []
with open('path_eu') as f:
	databox = f.readline()
	while databox:
		targetwebsite1.append(databox.split()[0])
		print databox.split()[1]
		pathnum1.append(int(databox.split()[1]))

		databox = f.readline()

print targetwebsite1
print pathnum1
l1 = []
for i in range(0,len(targetwebsite1)): l1.append(i)
plt.figure(2)
plt.plot(l1,pathnum1)
plt.xticks(l1,targetwebsite1,rotation = 90)
plt.ylabel('# of paths')
plt.title('Servers(EU) vs. # of paths')
plt.show()


targetwebsite2 = []
pathnum2 = []
with open('path_cn') as f:
	databox = f.readline()
	while databox:

		targetwebsite2.append(databox.split()[0])
		print databox.split()[1]
		pathnum2.append(int(databox.split()[1]))

		databox = f.readline()

print targetwebsite2
print pathnum2
l1 = []
for i in range(0,len(targetwebsite2)): l1.append(i)
plt.figure(3)
plt.plot(l1,pathnum2)
plt.xticks(l1,targetwebsite2,rotation = 90)
plt.ylabel('# of paths')
plt.title('Servers(CN) vs. # of paths')
plt.show()


targetwebsite3 = []
pathnum3 = []
with open('path_combined') as f:
	databox = f.readline()
	while databox:

		targetwebsite3.append(databox.split()[0])
		print databox.split()[1]
		pathnum3.append(int(databox.split()[1]))

		databox = f.readline()

print targetwebsite3
print pathnum3
l1 = []
for i in range(0,len(targetwebsite3)): l1.append(i)
plt.figure(4)
plt.plot(l1,pathnum3)
plt.xticks(l1,targetwebsite3,rotation = 90)
plt.ylabel('# of paths')
plt.title('Servers(combined) vs. # of paths')
plt.show()



