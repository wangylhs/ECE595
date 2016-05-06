#delay_graph2.py delay_graph2
#Guanshi He (he95)
#Plot the delay data with respect to different time slice

import random
import matplotlib.pyplot as plt
import sys
from datetime import date
import calendar

websites = []
with open('traceable_cn') as websitefile:
	counter = 0
	readbox = websitefile.readline()
	while readbox:
		websites.append(readbox.split()[0].rstrip())
		print 'websites[',counter,'] =====',websites[counter]
		readbox =websitefile.readline()
		counter = counter  + 1

index = 0
unusual_count = 0

delayarray = dict()
delayarrayam = dict()
delayarraypm = dict()
delayarrayweekday = dict()
delayarrayweekend = dict()
delayarrayweekdayam = dict()
delayarrayweekdaypm = dict()
delayarrayweekendam = dict()
delayarrayweekendpm = dict()
while index < counter:
	hubnum_am = 0
	hubnum_pm = 0
	delaynum_am = 0
	delaynum_pm = 0
	delay_avg = 0
	delay_weekday = 0
	delay_weekend = 0
	delay_weekend_am = 0
	delay_weekend_pm = 0
	delay_weekday_am = 0
	delay_weekday_pm = 0

	targetwebsite = websites[index]
	print 'targetwebsite = ',targetwebsite
	with open ('ecn_delay_data') as f:
		f.seek(0,0)
		databox = []
		databoxline1 = f.readline()
		databoxline2 = f.readline()
		databox.append(databoxline1)
		databox.append(databoxline2)

		found_count_am = 0
		found_count_pm = 0
		found_count = 0
		found_weekday = 0
		found_weekend = 0
		found_weekdayam = 0
		found_weekdaypm = 0
		found_weekendam = 0
		found_weekendpm = 0

		while databoxline1 and databoxline2:
			time = databoxline1.split()[3]
			#print time 
			hour = int(time.split(':')[0])
			#print 'hour = ',hour 
			day = databoxline1.split()[0]
			#print day
			site = databoxline2.split()[0]
			#print 'site = ',site
			hubno = int(databoxline2.split()[1])
			#print 'hubnumber = ',hubno
			delay = float(databoxline2.split()[2])
			#print 'delay = ',delay

			if site == targetwebsite:
				# print databoxline1
				# print databoxline2
				# #print "found targetwebsite"
				if hour >= 8 and hour <=20:
					print 'bbb'
					hubnum_pm = hubnum_pm + hubno
					delaynum_pm = delaynum_pm + delay
					found_count_pm = found_count_pm + 1
				else:
					print 'aaa'
					hubnum_am = hubnum_am + hubno
					delaynum_am = delaynum_am + delay
					found_count_am = found_count_am + 1
				if day == 'Mon' or day == 'Tue' or day == 'Wed' or day == 'Thu' or day == 'Fri':
					delay_weekday = delay_weekday + delay
					found_weekday = found_weekday + 1
				else:
					delay_weekend = delay_weekend + delay
					found_weekend = found_weekend + 1
				if (day == 'Mon' or day == 'Tue' or day == 'Wed' or day == 'Thu' or day == 'Fri') and (hour >= 8 and hour <=20):
					delay_weekday_am = delay_weekday_am + delay
					found_weekdayam = found_weekdayam + 1
				elif (day == 'Sat' or day == 'Sun') and (hour >= 8 and hour <=20):
					delay_weekend_am = delay_weekend_am + delay
					found_weekendam = found_weekendam + 1
				elif (day == 'Mon' or day == 'Tue' or day == 'Wed' or day == 'Thu' or day == 'Fri') and (hour < 8 or hour >20):
					delay_weekday_pm = delay_weekday_pm + delay
					found_weekdaypm = found_weekdaypm + 1
				else:# (day == 'Sat' or day == 'Sun') and (hour < 8 and hour > 20):
					delay_weekend_pm = delay_weekend_pm + delay
					found_weekendpm = found_weekendpm + 1
					


				found_count = found_count + 1
				delay_avg = delay_avg + delay


			databoxline1 = f.readline()
			databoxline2 = f.readline()
		
	hubnum_am = hubnum_am / found_count_am
	hubnum_pm = hubnum_pm / found_count_pm
	delaynum_am = delaynum_am / found_count_am
	delaynum_pm	= delaynum_pm / found_count_pm
	delay_avg = delay_avg / found_count
	delay_weekday = delay_weekday / found_weekday
	delay_weekend = delay_weekend / found_weekend
	delay_weekend_am = delay_weekend_am / found_weekendam
	delay_weekend_pm = delay_weekend_pm / found_weekendpm
	delay_weekday_am = delay_weekday_am / found_weekdayam
	delay_weekday_pm = delay_weekday_pm / found_weekdaypm
	delayarray[targetwebsite] = delay_avg
	delayarraypm[targetwebsite] = delaynum_pm
	delayarrayam[targetwebsite] = delaynum_am
	delayarrayweekday[targetwebsite] = delay_weekday
	delayarrayweekend[targetwebsite] = delay_weekend
	delayarrayweekendam[targetwebsite] = delay_weekend_am
	delayarrayweekendpm[targetwebsite] = delay_weekend_pm
	delayarrayweekdayam[targetwebsite] = delay_weekday_am
	delayarrayweekdaypm[targetwebsite] = delay_weekday_pm

	index = index + 1

l1 = []
l2 = []
l3 = []
l4 = []
l5 = []
l6 = []
l7 = []
l8 = []
l9 = []
for x in range(0,len(delayarray.keys())):
	l1.append(x)
for x in range(0,len(delayarrayam.keys())):
	l2.append(x)
for x in range(0,len(delayarraypm.keys())):
	l3.append(x)	
for x in range(0,len(delayarrayweekday.keys())):
	l4.append(x)	
for x in range(0,len(delayarrayweekend.keys())): 
	l5.append(x)		
for x in range(0,len(delayarrayweekendam.keys())): 
	l6.append(x)		
for x in range(0,len(delayarrayweekendpm.keys())): 
	l7.append(x)		
for x in range(0,len(delayarrayweekdayam.keys())): 
	l8.append(x)	
for x in range(0,len(delayarrayweekdaypm.keys())): 
	l9.append(x)	
	

plt.figure(1)
plt.plot(l1,delayarray.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l1,delayarray.keys())
plt.title('ALL DATA PLOT')
plt.ylabel('delay in ms')
plt.show()

plt.figure(2)
plt.title('am plot')
plt.ylabel('delay in ms')
plt.plot(l2,delayarrayam.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l2,delayarrayam.keys())
plt.show()

plt.figure(3)
plt.title('pm plot')
plt.ylabel('delay in ms')
plt.plot(l3,delayarraypm.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l3,delayarraypm.keys())
plt.show()

plt.figure(4)
plt.title('Mon-Fri plot')
plt.ylabel('delay in ms')
plt.plot(l4,delayarrayweekday.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l4,delayarrayweekday.keys())
plt.show()

plt.figure(5)
plt.title('Sat-Sun plot')
plt.ylabel('delay in ms')
plt.plot(l5,delayarrayweekend.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l5,delayarrayweekend.keys())
plt.show()

plt.figure(6)
plt.title('Sat-Sun AM plot')
plt.ylabel('delay in ms')
plt.plot(l6,delayarrayweekendam.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l6,delayarrayweekendam.keys())
plt.show()

plt.figure(7)
plt.title('Sat-Sun PM plot')
plt.ylabel('delay in ms')
plt.plot(l7,delayarrayweekendpm.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l7,delayarrayweekendpm.keys())
plt.show()

plt.figure(8)
plt.title('Mon-Fri AM plot')
plt.ylabel('delay in ms')
plt.plot(l8,delayarrayweekdayam.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l8,delayarrayweekdayam.keys())
plt.show()

plt.figure(9)
plt.title('Mon-Fri PM plot')
plt.ylabel('delay in ms')
plt.plot(l9,delayarrayweekdaypm.values(),'b')
plt.xticks(rotation = 90)
plt.xticks(l9,delayarrayweekdaypm.keys())
plt.show()
