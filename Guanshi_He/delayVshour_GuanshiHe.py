#delayVshour.py delayVshour
#Guanshi He (he95)
#Plot the hour vs delay for specific server

import random
import matplotlib.pyplot as plt
import sys
import pylab as pl

targetwebsite = raw_input("Please input the target website: \n")

delay_cal = dict()
delay_counter = dict()

with open ('final_delay_data.txt') as f:
	databoxline1 = f.readline()
	databoxline2 = f.readline()
	databox = []
	databox.append(databoxline1)
	databox.append(databoxline2)

	while databoxline1 and databoxline2:
		time = databoxline1.split()[3]
		hour = int(time.split(':')[0])

		site = databoxline2.split()[0]
		delay = float(databoxline2.split()[2])

		if site == targetwebsite:
			print delay
			if delay_cal.has_key(hour):
				print delay_cal.get(hour)
				delay_counter[hour] = delay_counter.get(hour) + 1
				delay_cal[hour] = (delay_cal.get(hour)*delay_counter.get(hour) + delay) / delay_counter.get(hour)
				
			else:
				delay_cal[hour] = delay
				delay_counter[hour] = 1
		databoxline1 = f.readline()
		databoxline2 = f.readline()

	length = len(delay_counter.keys())
	print delay_cal.keys()
	print delay_cal.values()
	print delay_counter.keys()
	print delay_counter.values()


	pl.plot(delay_cal.keys(),delay_cal.values(),'r')
	pl.title(targetwebsite)
	pl.ylabel('delay')
	pl.xlabel('hour')
	plt.xlim([0,24])
	pl.show()