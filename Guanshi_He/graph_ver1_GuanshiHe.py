#graph_ver1.py graph_ver1
#Guanshi He (he95)
#Plot the visit time Vs. corresponding hour
#Plot the delay avg Vs. corresponding hour

import random
import matplotlib.pyplot as plt
import sys

targetwebsite = raw_input("Please input the target website: \n")
targettimeslotflag = raw_input("Please choose the time slot\n1 for 6:00am to 6:00pm\n2 for 6:00pm to 6:00am\n3 for graph of comparison in different time slot\n")
targettimeslotflag = int(targettimeslotflag)
# 1 for 6am to 6pm
# 2 for 6pm to 6am
# Process the txt data file
timecount = dict()
avgdelay = dict()
avgdelay1 = dict()
avgdelay2 = dict()
databox = []
i = 1
with open('final_ecn_data_cn') as f:
	databoxline1 = f.readline()
	#print databoxline1
	databoxline2 = f.readline()
	#print databoxline2
	databox.append(databoxline1)
	databox.append(databoxline2)
	while databoxline2:
		while(len(databoxline2.split())!=6):
			i = i + 1
			databoxline2 = f.readline()
			databox.append(databoxline2)
			if(databoxline2 == ''):
				break
		#get one chunk of traceroute info
		#for j in range (0,i):
			#print j
			#print j,databox[j]
		if databox[1].split()[0] == targetwebsite:
			time = databox[0].split()[3]
			webip = databox[1].split()[1]
			webip = webip[0:len(webip)-1]
			k = 2
			hour = int(time[0:2])
			if ((targettimeslotflag == 1) and (hour >= 6 and hour <= 18)):
				while len(databox[k].split()) == 3:
					if databox[k].split()[1] != '*':
						key = databox[k].split()[1]
						key = key[1:len(key)-1]
						delay = databox[k].split()[2]
						k = k + 1
						# check if the hour has been counted before
						if timecount.has_key(key):
							visittime = timecount.get(key) + 1
							timecount[key] = visittime
						else:
							visittime = 1
							timecount[key] = visittime
						# check if the hour for delay has been counted before
						if avgdelay.has_key(key):
							delaytime  = avgdelay.get(key)
							avgnew = (float(delaytime)*(timecount.get(key)-1)+float(delay))/timecount.get(key)
							avgdelay[key] = avgnew
						else:
							delaytime = delay
							avgdelay[key] = float(delaytime)
					else:
						k = k + 1
			elif targettimeslotflag == 2 and (hour < 6 or hour > 18):
				while len(databox[k].split()) == 3:
					if databox[k].split()[1] != '*':
						key = databox[k].split()[1]
						key = key[1:len(key)-1]
						delay = databox[k].split()[2]
						#print key
						#print delay
						k = k + 1
					
						if timecount.has_key(key):
							visittime = timecount.get(key) + 1
							timecount[key] = visittime
						else:
							visittime = 1
							timecount[key] = visittime
						if avgdelay.has_key(key):
							delaytime  = avgdelay.get(key)
							avgnew = (float(delaytime)*(timecount.get(key)-1)+float(delay))/timecount.get(key)
							avgdelay[key] = avgnew
						else:
							delaytime = delay
							avgdelay[key] = float(delaytime)
					else:
						k = k + 1
			else:
				while len(databox[k].split()) == 3:
					if databox[k].split()[1] != '*':
						key = databox[k].split()[1]
						key = key[1:len(key)-1]
						delay = databox[k].split()[2]
						k = k + 1
					
						if timecount.has_key(key):
							visittime = timecount.get(key) + 1
							timecount[key] = visittime
						else:
							visittime = 1
							timecount[key] = visittime
						if hour >= 6 and hour <= 18:
							if avgdelay1.has_key(key):
								delaytime  = avgdelay1.get(key)
								avgnew = (float(delaytime)*(timecount.get(key)-1)+float(delay))/timecount.get(key)
								avgdelay1[key] = avgnew
							else:
								delaytime = delay
								avgdelay1[key] = float(delaytime)
						else:
							if avgdelay2.has_key(key):
								delaytime  = avgdelay2.get(key)
								avgnew = (float(delaytime)*(timecount.get(key)-1)+float(delay))/timecount.get(key)
								avgdelay2[key] = avgnew
							else:
								delaytime = delay
								avgdelay2[key] = float(delaytime)
					else:
						k = k + 1

		databoxline1 = databoxline2
		databoxline2 = f.readline()
		
		i = 1
		databox = []
		databox.append(databoxline1)
		databox.append(databoxline2)
	if targettimeslotflag == 1 or targettimeslotflag == 2:
		print timecount.keys()
		print timecount.values()
		print avgdelay.keys()
		print avgdelay.values()
		x = len(timecount.keys())
		l = []
		for y in range(0,x):
			l.append(y)
		print l
		
		fig1 = plt.figure(1)
		plt.xticks(rotation=90)
		fig1 = plt.bar(l,timecount.values(), alpha = 0.5, color = 'b',align='center',tick_label = timecount.keys())
		fig1 = plt.ylabel('Times')
		plt.xlabel('Nodes')
		plt.title('Time of visiting')
		fig1 = plt.show()
		
		
		plt.figure(2)
		plt.xticks(rotation=90)
		x = len(avgdelay.values())
		l = []
		for y in range(0,x):
			l.append(y)
		plt.bar(l,avgdelay.values(), alpha = 0.5, color = 'b',align='center',tick_label = avgdelay.keys())
		plt.ylabel('Delay in ms')
		plt.xlabel('Nodes')
		plt.title('Delay time for different nodes')
		plt.show()
	else: 
		print timecount.keys()
		print timecount.values()
		#print avg
		l1 = []
		l2 = []
		x1 = len(avgdelay1.keys())
		x2 = len(avgdelay2.keys())
		
		barwidth = 0.35
		for y in range(0,x1):
			l1.append(y)
		for y in range(0,x2):
			l2.append(y+barwidth)

		print avgdelay1.keys()
		print avgdelay1.values()
		print avgdelay2.keys()
		print avgdelay2.values()
		
		opacity = 0.4
		rects1 = plt.bar(l1,avgdelay1.values(),barwidth,
						alpha = opacity,
						color = 'b',
						label = '6pmTo6am')#,barwidth,'b',label = '6:00am to 6:00pm')
		rects2 = plt.bar(l2,avgdelay2.values(),barwidth,
						alpha = opacity,
						color = 'r',
						label = '6amTo6pm')
		plt.xticks(rotation=90)
		plt.xticks(l1,avgdelay1.keys())
		plt.legend()
		plt.ylabel('Delay in ms')
		plt.xlabel('Nodes')
		plt.title('Delay time in different time slot')
		plt.show()










