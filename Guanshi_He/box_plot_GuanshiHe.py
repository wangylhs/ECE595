# box_plot.py - box_plot
# Guanshi He (he95)
# Website Vs. Delay in boxplot

import random
import matplotlib.pyplot as plt
import sys


#read the list of websites from file
websites = []
with open('USWebsites.txt') as websitefile:
	counter = 0
	readbox = websitefile.readline()
	while readbox:
		websites.append(readbox.rstrip())
		print 'websites[',counter,'] =====',websites[counter]
		readbox =websitefile.readline()
		counter = counter  + 1


index = 0
data = []
listindex = []
while index < counter:
	delay = []
	targetwebsite = websites[index]
	print 'targetwebsite = ',targetwebsite
	with open ('final_delay_data.txt') as f:
		f.seek(0,0)
		databox = []
		databoxline1 = f.readline()
		databoxline2 = f.readline()
		databox.append(databoxline1)
		databox.append(databoxline2)

		while databoxline1 and databoxline2:
			site = databoxline2.split()[0]
			delaynum = float(databoxline2.split()[2])
			if site == targetwebsite:
				#get all the delay value corresponding to the target website
				delay.append(delaynum)

			databoxline1 = f.readline()
			databoxline2 = f.readline()

	print delay
	#append the array of delay value to the data set
	data.append(delay)
	index = index + 1
	listindex.append(index)
print data
#plot the boxplot
plt.boxplot(data)
plt.xticks(rotation=90)
plt.xticks(listindex,websites)
plt.ylim([0,500])
plt.xlabel('Websites')
plt.ylabel('Delay')
plt.title('Website Vs. Delay in boxplot')
plt.show()