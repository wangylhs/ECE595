# delay_graph.py delay_graph
# Guanshi He (he95)
# Plot 2 types of graph
# 	i.  bar graph of usual cases vs. unusal cases
#		usual: avg delay value in the night is higher than in the daytime
#	ii. bar graph of different websites vs. hub number in different time slice


import random
import matplotlib.pyplot as plt
import sys

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
unusual_count = 0

hubs_am = dict()
hubs_pm = dict()

while index < counter:
	hubnum_am = 0
	hubnum_pm = 0
	delaynum_am = 0
	delaynum_pm = 0

	targetwebsite = websites[index]
	print 'targetwebsite = ',targetwebsite
	with open ('final_delay_data.txt') as f:
		f.seek(0,0)
		databox = []
		databoxline1 = f.readline()
		databoxline2 = f.readline()
		databox.append(databoxline1)
		databox.append(databoxline2)

		found_count_am = 0
		found_count_pm = 0
		while databoxline1 and databoxline2:
			time = databoxline1.split()[3]
			#print time 
			hour = int(time.split(':')[0])
			#print 'hour = ',hour 

			site = databoxline2.split()[0]
			#print 'site = ',site
			hubno = int(databoxline2.split()[1])
			#print 'hubnumber = ',hubno
			delay = float(databoxline2.split()[2])
			#print 'delay = ',delay

			if site == targetwebsite:
				#print "found targetwebsite"
				if hour >= 6 and hour <=18:
					hubnum_pm = hubnum_pm + hubno
					delaynum_pm = delaynum_pm + delay
					found_count_pm = found_count_pm + 1
				else:
					hubnum_am = hubnum_am + hubno
					delaynum_am = delaynum_am + delay
					found_count_am = found_count_am + 1

			databoxline1 = f.readline()
			databoxline2 = f.readline()
		
	hubnum_am = hubnum_am / found_count_am
	hubnum_pm = hubnum_pm / found_count_pm
	delaynum_am = delaynum_am / found_count_am
	delaynum_pm	= delaynum_pm / found_count_pm
	print 'hubnum_am = ',hubnum_am
	print 'hubnum_pm = ',hubnum_pm
	print 'delaynum_am = ',delaynum_am
	print 'delaynum_pm = ',delaynum_pm
	hubs_am[targetwebsite] = hubnum_am
	hubs_pm[targetwebsite] = hubnum_pm

	if delaynum_am < delaynum_pm:
		print '======UNUSUAL CASE======'
		unusual_count = unusual_count + 1

	index = index + 1
print 'count = ',found_count_am + found_count_pm
print 'unusual_count = ',unusual_count


plt.figure(1)
plt.bar([0,1],[found_count_am+found_count_pm, unusual_count],align='center',tick_label = ['Usual case','Unusual case'] )
plt.ylabel('Times of cases')
plt.title('Delay analysis for different websites')
plt.show()

barwidth = 0.35
x1 = len(hubs_am.keys())
l1 = []
l2 = []
opacity = 0.4
for y in range(0,x1):l1.append(y)
for y in range(0,x1):l2.append(y+barwidth)
plt.figure(2)
rect1 = plt.bar(l1,hubs_am.values(),barwidth,alpha = opacity,color = 'b',label = 'AM')
rect2 = plt.bar(l2,hubs_pm.values(),barwidth,alpha = opacity,color = 'r',label = 'PM')
plt.xticks(rotation = 90)
plt.xticks(l1,hubs_am.keys())
plt.legend()
plt.ylabel('# of hubs')
plt.xlabel('Websites')
plt.title('Website vs. # of hubs')
plt.show()












